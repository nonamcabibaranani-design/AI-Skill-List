#!/usr/bin/env python3
"""Điều phối viên đa nền tảng cho skill orca-loop (Windows + POSIX, Orca 1.4+).

Lưu ý môi trường bắt buộc:
- Phiên Orca Native Chat / Bot (Antigravity Chat, Codex App, Bot): dùng cơ chế
  end-turn auto-wake của Orca; TUYỆT ĐỐI KHÔNG gọi `wait` hay tự poll `check`.
- Phiên Terminal CLI thuần: chạy nền `wait` để hứng sự kiện dispatch.

Trạng thái lưu ở PIPELINE_DIR (mặc định <temp>/pipeline-state):
dispatches.json, pending.json, reports.json.

Lệnh:
  preflight [--cwd DIR]                                kiểm tra Orca, stack, rules và Codex defaults
  spec      --body FILE --out FILE [--cwd DIR] [--include FILE ...]  dựng spec cho worker
  start     --spec-file FILE (--agent A | --terminal H) [...]        tạo task + worker-start
  wait      [--seconds N]                              [Terminal CLI only] chờ sự kiện dispatch
  finish    --dispatch D [--retain]                    release/retain worker và ack delivery
  reply     --id MSG (--body TEXT | --body-file FILE)  trả lời câu hỏi của worker
  nudge     --dispatch D (--body TEXT | --body-file FILE) [--subject S]  nhắn cho worker
  status                                               liệt kê trạng thái worker của Run
  report    --ticket N --body FILE [--repo OWNER/REPO] [--cwd DIR]   tạo/sửa comment GitHub issue
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(os.path.dirname(HERE), "templates")
DIR = os.environ.get("PIPELINE_DIR") or os.path.join(tempfile.gettempdir(), "pipeline-state")
TYPES = "worker_done,escalation,question"
IGNORED_SUBDIRS = {".git", ".idea", ".mvn", ".vscode", "node_modules", "target", "build", "dist", "vendor"}
RULE_CANDIDATES = [".local-rules", "AGENTS.md", "AGENT.md", "CLAUDE.md", "GLOSSARY.md", "docs/adr"]


def configure_utf8():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def ensure_state_dir():
    os.makedirs(DIR, exist_ok=True)


def out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=1))


def fail(msg, **kw):
    out({"ok": False, "error": msg, **kw})
    sys.exit(1)


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def write_text(path, content):
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def load(name, default):
    try:
        return json.loads(read_text(os.path.join(DIR, name)))
    except Exception:
        return default


def save(name, data):
    ensure_state_dir()
    write_text(os.path.join(DIR, name), json.dumps(data, ensure_ascii=False, indent=1))


def resolve_bin(name):
    if name == "orca":
        env_cmd = os.environ.get("ORCA_CLI_COMMAND")
        if env_cmd:
            return env_cmd
    found = shutil.which(name)
    if not found:
        fail(f"Không tìm thấy lệnh `{name}` trong PATH")
    return found


def run_proc(cmd, cwd=None, input_text=None, timeout=None):
    return subprocess.run(
        cmd,
        cwd=cwd,
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def orca(args, timeout=None):
    p = run_proc([resolve_bin("orca")] + args, timeout=timeout)
    lines = [l for l in p.stdout.splitlines() if '"_keepalive"' not in l and '"_heartbeat"' not in l]
    text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except Exception:
        return {"ok": False, "error": {"message": (text or p.stderr).strip()[:2000]}}


def read_codex_defaults():
    path = os.path.expanduser("~/.codex/config.toml")
    if not os.path.isfile(path):
        return {"exists": False, "model": None, "effort": None}
    head = re.split(r"(?m)^\s*\[", read_text(path), maxsplit=1)[0]
    m_model = re.search(r'(?m)^\s*model\s*=\s*["\']([A-Za-z0-9._:@/-]+)["\']\s*(?:#.*)?$', head)
    m_effort = re.search(r'(?m)^\s*model_reasoning_effort\s*=\s*["\']([A-Za-z0-9._-]+)["\']\s*(?:#.*)?$', head)
    return {
        "exists": True,
        "model": m_model.group(1) if m_model else None,
        "effort": m_effort.group(1) if m_effort else None,
    }


def detect_stacks_in_dir(root, rel_path="."):
    is_win = os.name == "nt"
    stacks = []
    has = lambda name: os.path.exists(os.path.join(root, name))

    if has("pom.xml") or has("mvnw.cmd") or has("mvnw"):
        if is_win and has("mvnw.cmd"):
            cmds = [".\\mvnw.cmd -DskipTests compile", ".\\mvnw.cmd -Dtest=<Class> test"]
        elif not is_win and has("mvnw"):
            cmds = ["./mvnw -DskipTests compile", "./mvnw -Dtest=<Class> test"]
        else:
            cmds = ["mvn -DskipTests compile", "mvn -Dtest=<Class> test"]
        stacks.append({"stack": "maven", "path": rel_path, "verifyCommands": cmds})

    if has("build.gradle") or has("build.gradle.kts") or has("gradlew.bat") or has("gradlew"):
        if is_win and has("gradlew.bat"):
            cmds = [".\\gradlew.bat classes", ".\\gradlew.bat test --tests <Pattern>"]
        elif not is_win and has("gradlew"):
            cmds = ["./gradlew classes", "./gradlew test --tests <Pattern>"]
        else:
            cmds = ["gradle classes", "gradle test --tests <Pattern>"]
        stacks.append({"stack": "gradle", "path": rel_path, "verifyCommands": cmds})

    if has("go.mod"):
        stacks.append({
            "stack": "go",
            "path": rel_path,
            "verifyCommands": ["go build ./...", "go vet ./...", "go test ./..."],
        })

    if has("package.json"):
        pm = "npm"
        if has("pnpm-lock.yaml"):
            pm = "pnpm"
        elif has("yarn.lock"):
            pm = "yarn"
        elif has("bun.lockb") or has("bun.lock"):
            pm = "bun"
        try:
            scripts = (json.loads(read_text(os.path.join(root, "package.json"))).get("scripts") or {})
        except Exception:
            scripts = {}
        cmds = [f"{pm} run {s}" for s in ("typecheck", "lint", "test", "build") if s in scripts]
        stacks.append({
            "stack": "node",
            "packageManager": pm,
            "path": rel_path,
            "verifyCommands": cmds or [f"{pm} test"],
        })

    if has("Cargo.toml"):
        if not is_win and os.path.exists(os.path.join(root, "scripts", "cargo.sh")):
            cmds = ["./scripts/cargo.sh check --all-targets", "./scripts/cargo.sh test"]
        else:
            cmds = ["cargo check --all-targets", "cargo test"]
        stacks.append({"stack": "rust", "path": rel_path, "verifyCommands": cmds})

    if has("pyproject.toml") or has("requirements.txt"):
        stacks.append({"stack": "python", "path": rel_path, "verifyCommands": ["pytest"]})

    return stacks


def detect_project(cwd):
    stacks = detect_stacks_in_dir(cwd, ".")
    if not stacks:
        try:
            for entry in sorted(os.scandir(cwd), key=lambda e: e.name):
                if entry.is_dir() and not entry.name.startswith(".") and entry.name not in IGNORED_SUBDIRS:
                    stacks.extend(detect_stacks_in_dir(entry.path, entry.name))
        except OSError:
            pass
    rules = [rel for rel in RULE_CANDIDATES if os.path.exists(os.path.join(cwd, *rel.split("/")))]
    return stacks, rules


def cmd_preflight(a):
    cwd = os.path.abspath(a.cwd)
    if not os.path.isdir(cwd):
        fail("Thư mục --cwd không tồn tại", cwd=cwd)
    st = orca(["status", "--json"])
    if not st.get("ok"):
        fail("orca status thất bại", detail=st.get("error"))
    res = st.get("result") or {}
    runtime = res.get("runtime") or {}
    if runtime.get("state") != "ready":
        fail("Orca runtime chưa sẵn sàng", state=runtime.get("state"), detail=res)
    stacks, rules = detect_project(cwd)
    out({
        "ok": True,
        "os": "windows" if os.name == "nt" else sys.platform,
        "cwd": cwd,
        "orca": {
            "appVersion": runtime.get("appVersion"),
            "state": runtime.get("state"),
            "caller": (res.get("caller") or {}).get("orcaSessionId"),
        },
        "stacks": stacks,
        "rules": rules,
        "codexDefaults": read_codex_defaults(),
    })


def cmd_spec(a):
    cwd = os.path.abspath(a.cwd)
    if not os.path.isdir(cwd):
        fail("Thư mục --cwd không tồn tại", cwd=cwd)
    body = read_text(a.body)
    git_res = run_proc([resolve_bin("git"), "-C", cwd, "status", "--short"])
    git_dirty = git_res.stdout.strip() if git_res.returncode == 0 else "(không phải repo git hoặc không đọc được git status)"
    parts = [
        body.rstrip(),
        read_text(os.path.join(TPL, "constraints.txt")).rstrip(),
        "Danh sách file modified/untracked trước bước này (đừng revert):\n" + (git_dirty or "(trống)"),
    ]
    for inc in a.include or []:
        parts.append("===== " + os.path.basename(inc) + " =====\n" + read_text(inc).rstrip())
    parts.append(read_text(os.path.join(TPL, "protocol.txt")).rstrip())
    write_text(a.out, "\n\n".join(parts) + "\n")
    out({"ok": True, "spec": a.out, "bytes": os.path.getsize(a.out)})


def cmd_start(a):
    if a.effort and not a.model:
        fail("--effort bắt buộc phải đi kèm --model")
    spec_path = os.path.abspath(a.spec_file)
    if not os.path.isfile(spec_path):
        fail("Không tìm thấy file --spec-file", spec_file=spec_path)

    env_args = [] if a.on else ["--environment", "local"]
    title_args = ["--task-title", a.title] if a.title else []
    t = orca(["orchestration", "task-create", "--spec-file", spec_path, "--json"] + env_args + title_args)
    if not t.get("ok"):
        fail("task-create thất bại", detail=t.get("error"))
    task = t.get("result") or {}
    task_id = task.get("taskId") or (task.get("task") or {}).get("id")
    if not task_id:
        fail("task-create thiếu id; kiểm tra task-list trước khi thử lại", detail=t)

    placement = ["--on", a.on] if a.on else ["--environment", "local"]
    worktree = a.worktree or (None if a.terminal else "current")
    wt_args = ["--worktree", worktree] if worktree else []
    who = ["--terminal", a.terminal] if a.terminal else ["--agent", a.agent]
    if a.model and not a.terminal:
        who += ["--model", a.model] + (["--effort", a.effort] if a.effort else [])

    extra = []
    if a.repo:
        extra += ["--repo", a.repo]
    if a.name:
        extra += ["--name", a.name]
    if a.item is not None:
        extra += ["--item", str(a.item)]
    if a.keep_open:
        extra.append("--keep-open")

    try:
        w = orca(["orchestration", "worker-start", "--task", task_id] + placement + wt_args + extra + who + ["--json"])
    except (OSError, subprocess.SubprocessError) as exc:
        fail("worker-start thất bại; kiểm tra worker-list trước khi dùng lại task", task=task_id, detail=str(exc))
    if not w.get("ok"):
        fail(
            "worker-start thất bại: không chạy lại start; đọc failedStage/residualResources và recovery-and-cleanup, dùng lại task đã tạo",
            task=task_id,
            detail=w.get("error") or w.get("result"),
        )
    r = w.get("result") or {}
    dispatch_id = r.get("dispatchId")
    if not dispatch_id:
        fail("worker-start thiếu dispatchId; kiểm tra worker-list trước khi dùng lại task", task=task_id, detail=w)

    d = load("dispatches.json", {})
    d[dispatch_id] = {
        "task": task_id,
        "agent": a.agent or ("terminal:" + a.terminal),
        "title": a.title or "",
        "started": int(time.time()),
    }
    try:
        save("dispatches.json", d)
    except OSError as exc:
        fail("không lưu được dispatch; không tạo task mới", task=task_id, dispatch=dispatch_id, detail=str(exc))

    handle = next((e.get("id") for e in r.get("effects", []) if e.get("kind") == "terminal"), None)
    out({"ok": True, "dispatch": dispatch_id, "task": task_id, "state": r.get("state"), "terminal": handle})


def summarize(m):
    p = m.get("payload") or {}
    if isinstance(p, str):
        try:
            p = json.loads(p)
        except (TypeError, ValueError):
            p = {}
    if not isinstance(p, dict):
        p = {}
    return {
        "type": m["type"],
        "id": m["id"],
        "dispatch": p.get("dispatchId") or m.get("from_handle") or m.get("from"),
        "outcome": p.get("outcome"),
        "body": m.get("body"),
        "report": p.get("reportPath"),
        "files": p.get("filesModified"),
        "question": p.get("question"),
    }


def delivery_state(result):
    messages = result.get("messages") or []
    events = [summarize(m) for m in messages if m["type"] != "heartbeat"]
    pending = {}
    if messages:
        pending = {"unresolved": [e["dispatch"] for e in events if e["type"] == "worker_done"]}
        if result.get("deliveryId"):
            pending["delivery"] = result["deliveryId"]
    return pending, events


def worker_events():
    events = []
    for dispatch in load("dispatches.json", {}):
        response = orca(["orchestration", "worker-show", "--dispatch", dispatch, "--json", "--full"])
        if not response.get("ok"):
            fail("worker-show thất bại", dispatch=dispatch, detail=response.get("error"))
        result = response.get("result") or {}
        worker = result.get("worker") or result
        state = worker.get("state")
        attention = (result.get("projection") or {}).get("attention", worker.get("attention")) or []
        if isinstance(attention, dict):
            attention = attention.get("categories") or []
        if isinstance(attention, str):
            attention = [attention]
        if state in ("succeeded", "failed"):
            events.append({"type": "worker_settled", "dispatch": dispatch, "state": state})
        elif any("input" in category for category in attention):
            events.append({"type": "needs_input", "dispatch": dispatch, "state": state})
    return events


def cmd_wait(a):
    pend = load("pending.json", {})
    if pend.get("unresolved"):
        fail("còn worker chưa xử lý: chạy `finish --dispatch <id>` cho " + ",".join(pend["unresolved"]))
    deadline = time.time() + min(a.seconds, 575)
    ack = pend.get("delivery")
    events = []
    delivery = None
    while time.time() < deadline:
        remaining = int((deadline - time.time()) * 1000)
        if remaining < 2000:
            break
        args = ["orchestration", "check"] + (["--ack", ack] if ack else []) + [
            "--wait", "--types", TYPES, "--timeout-ms", str(remaining), "--json",
        ]
        r = orca(args, timeout=remaining / 1000 + 30)
        if not r.get("ok"):
            fail("check thất bại", detail=r.get("error"))
        pending, events = delivery_state(r["result"])
        save("pending.json", pending)
        delivery = pending.get("delivery")
        ack = delivery
        if events:
            break
    if not events:
        events = worker_events()
        if events:
            pending = load("pending.json", {})
            pending["unresolved"] = [e["dispatch"] for e in events if e["type"] == "worker_settled"]
            save("pending.json", pending)
    if not events:
        out({"ok": True, "result": "timeout", "note": "chưa có sự kiện; gọi lại wait"})
        return
    out({
        "ok": True,
        "result": "events",
        "delivery": delivery,
        "events": events,
        "next": "worker_done/worker_settled → finish --dispatch <id> [--retain]; question/escalation → reply rồi wait; needs_input → worker-read",
    })


def cmd_finish(a):
    pend = load("pending.json", {})
    action = "worker-retain" if a.retain else "worker-release"
    r = orca(["orchestration", action, "--dispatch", a.dispatch, "--json"])
    if not r.get("ok"):
        fail(action + " thất bại", detail=r.get("error"))
    dispatches = load("dispatches.json", {})
    dispatches.pop(a.dispatch, None)
    save("dispatches.json", dispatches)
    pend["unresolved"] = [x for x in pend.get("unresolved", []) if x != a.dispatch]
    if not pend["unresolved"] and not pend.get("delivery"):
        pend = {}
    save("pending.json", pend)
    acked = None
    events = []
    if pend.get("delivery") and not pend["unresolved"]:
        k = orca(["orchestration", "check", "--ack", pend["delivery"], "--types", TYPES, "--timeout-ms", "1000", "--json"])
        if not k.get("ok"):
            fail("ack thất bại; gọi lại wait để thử lại", detail=k.get("error"))
        acked = pend["delivery"]
        pend, events = delivery_state(k["result"])
        save("pending.json", pend)
    out({
        "ok": True,
        "dispatch": a.dispatch,
        "state": (r.get("result") or {}).get("state"),
        "acked": acked,
        "still_unresolved": pend.get("unresolved", []),
        "events": events,
    })


def body_args(a):
    if a.body_file:
        path = os.path.abspath(a.body_file)
        if not os.path.isfile(path):
            fail("Không tìm thấy file --body-file", body_file=path)
        return ["--body-file", path]
    return ["--body", a.body]


def cmd_reply(a):
    r = orca(["orchestration", "reply", "--id", a.id] + body_args(a) + ["--json"])
    if not r.get("ok"):
        fail("reply thất bại", detail=r.get("error"))
    out({"ok": True, "result": r.get("result")})


def cmd_nudge(a):
    r = orca(["orchestration", "send", "--to", "dispatch:" + a.dispatch, "--subject", a.subject] + body_args(a) + ["--json"])
    if not r.get("ok"):
        fail("nudge thất bại", detail=r.get("error"))
    out({"ok": True, "result": r.get("result"), "note": "đã gửi vào hàng đợi; theo dõi bằng auto-wake hoặc worker-read"})


def cmd_status(a):
    r = orca(["orchestration", "worker-list", "--json"])
    if not r.get("ok"):
        fail("worker-list thất bại", detail=r.get("error"))
    rows = []
    for w in (r.get("result") or {}).get("workers", []):
        pr = w.get("projection") or {}
        rows.append({
            "dispatch": w.get("dispatchId"),
            "worker": w.get("workerState"),
            "terminal": w.get("terminalState"),
            "outcome": pr.get("outcome"),
            "liveness": (pr.get("liveness") or {}).get("verdict"),
        })
    out({"ok": True, "workers": rows})


def resolve_repo(cwd):
    res = run_proc([resolve_bin("gh"), "repo", "view", "--json", "nameWithOwner"], cwd=cwd)
    if res.returncode != 0:
        fail("Không tự lấy được --repo từ gh repo view; hãy truyền --repo OWNER/REPO", detail=res.stderr.strip())
    try:
        name = json.loads(res.stdout).get("nameWithOwner")
    except Exception:
        name = None
    if not name:
        fail("gh repo view không trả về nameWithOwner")
    return name


def cmd_report(a):
    """Tạo hoặc cập nhật đúng 1 comment báo cáo theo repo/ticket trong reports.json."""
    cwd = os.path.abspath(a.cwd)
    repo = a.repo or resolve_repo(cwd)
    key = f"{repo}#{a.ticket}"
    reports = load("reports.json", {})
    if not isinstance(reports, dict):
        fail("report: reports.json không hợp lệ")
    previous = reports.get(key)
    body = read_text(a.body)
    endpoint = (
        f"repos/{repo}/issues/comments/{previous['id']}"
        if previous
        else f"repos/{repo}/issues/{a.ticket}/comments"
    )
    response = run_proc(
        [resolve_bin("gh"), "api", "--method", "PATCH" if previous else "POST", endpoint, "--input", "-"],
        cwd=cwd,
        input_text=json.dumps({"body": body}, ensure_ascii=False),
    )
    if response.returncode != 0:
        fail("report: gh api thất bại", detail=response.stderr.strip())
    comment = json.loads(response.stdout)
    reports[key] = {"id": comment["id"], "url": comment["html_url"]}
    save("reports.json.tmp", reports)
    os.replace(os.path.join(DIR, "reports.json.tmp"), os.path.join(DIR, "reports.json"))
    out({"ok": True, "repo": repo, "comment": reports[key], "updated": previous is not None})


def add_body_source(parser):
    bg = parser.add_mutually_exclusive_group(required=True)
    bg.add_argument("--body")
    bg.add_argument("--body-file")


def main():
    configure_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("preflight", help="Kiểm tra Orca, stack dự án, file rules và Codex defaults")
    s.add_argument("--cwd", default=".")
    s.set_defaults(f=cmd_preflight)

    s = sp.add_parser("spec", help="Dựng spec cho worker kèm ràng buộc và danh sách file dirty")
    s.add_argument("--body", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--cwd", default=".")
    s.add_argument("--include", action="append")
    s.set_defaults(f=cmd_spec)

    s = sp.add_parser("start", help="Tạo task (--spec-file) và worker-start")
    s.add_argument("--spec-file", required=True)
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--agent")
    g.add_argument("--terminal")
    s.add_argument("--worktree", default=None)
    s.add_argument("--title")
    s.add_argument("--model")
    s.add_argument("--effort")
    s.add_argument("--on")
    s.add_argument("--repo")
    s.add_argument("--name")
    s.add_argument("--item", type=int)
    s.add_argument("--keep-open", action="store_true")
    s.set_defaults(f=cmd_start)

    s = sp.add_parser("wait", help="Chờ sự kiện dispatch (CHỈ dùng ở Terminal CLI; Native Chat/Bot dùng auto-wake)")
    s.add_argument("--seconds", type=int, default=575)
    s.set_defaults(f=cmd_wait)

    s = sp.add_parser("finish", help="Release hoặc retain worker và ack delivery")
    s.add_argument("--dispatch", required=True)
    s.add_argument("--retain", action="store_true")
    s.set_defaults(f=cmd_finish)

    s = sp.add_parser("reply", help="Trả lời câu hỏi của worker (--body hoặc --body-file)")
    s.add_argument("--id", required=True)
    add_body_source(s)
    s.set_defaults(f=cmd_reply)

    s = sp.add_parser("nudge", help="Nhắn cho worker (--body hoặc --body-file)")
    s.add_argument("--dispatch", required=True)
    add_body_source(s)
    s.add_argument("--subject", default="Cập nhật từ coordinator")
    s.set_defaults(f=cmd_nudge)

    s = sp.add_parser("status", help="Xem trạng thái các worker của Run")
    s.set_defaults(f=cmd_status)

    s = sp.add_parser("report", help="Tạo hoặc sửa comment báo cáo trên GitHub issue")
    s.add_argument("--ticket", required=True, type=int)
    s.add_argument("--body", required=True)
    s.add_argument("--repo")
    s.add_argument("--cwd", default=".")
    s.set_defaults(f=cmd_report)

    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
