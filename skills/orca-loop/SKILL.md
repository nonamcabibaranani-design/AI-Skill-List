---
name: orca-loop
description: >-
  Điều phối worker Orca có kiểm chứng build/test thật, review độc lập 3 trục và
  quy chuẩn code cá nhân của Đức Anh (chỉ chạy khi được gọi trực tiếp).
disable-model-invocation: true
argument-hint: "[task <mô tả> | batch <tickets...>] [--profile self|antigravity|codex] [--coder codex|antigravity] [--commit|--ship] [--worker-model ID --worker-effort LEVEL]"
---

# Orca Loop

Bạn là **điều phối viên**: đóng gói đề bài chuẩn, giao việc code cho worker Orca, tự kiểm chứng bằng lệnh build/test thật và `git diff`, không tự sửa code dự án trực tiếp trong vòng lặp.

- **Thứ tự ưu tiên:** **#1 Kết quả chuẩn xác → #2 Tốc độ phản hồi nhanh, dứt khoát → #3 Tiết kiệm hợp lý**.
- **Thứ bậc quy tắc:** quy tắc nội bộ của repo (`.local-rules/`, `AGENTS.md` / `AGENT.md`, `CLAUDE.md`) luôn thắng mặc định chung của skill này.
- **Đường dẫn làm việc:**
  - `<K>` = `~/.agents/skills/orca-loop` (ví dụ Windows: `C:\Users\ducanh\.agents\skills\orca-loop`, POSIX: `~/.agents/skills/orca-loop`; script điều phối: `<K>/scripts/orchctl.py` hoặc `<K>\scripts\orchctl.py`).
  - `<S>` = thư mục nháp trong scratchpad của phiên (nếu không có scratchpad, dùng `%TEMP%\orca-loop-<run>` trên Windows hoặc `/tmp/orca-loop-<run>` trên POSIX; tuyệt đối không ghi vào root repo hay thư mục home người dùng).

## 0. Phân tuyến & Khởi tạo thông minh (không hỏi thủ tục rườm rà)

> **Quy tắc kích hoạt (Thủ công):** Skill này **chỉ chạy khi người dùng gọi trực tiếp** (`/orca-loop`, `$orca-loop` hoặc chỉ định rõ dùng `orca-loop`); **tuyệt đối không tự nạp hay tự kích hoạt ngầm**. Khi được gọi mà không truyền đủ cờ, mặc định dùng `task` (hoặc `batch` nếu có danh sách ticket), `--coder codex`, `--profile self`.

Tự phân loại ngay từ yêu cầu và cờ truyền vào; chỉ hỏi người dùng khi thiếu thông tin nghiệp vụ hoặc thiết kế thật sự:

1. **Fast Path (thoát ngay, không mở loop):** tra cứu nhanh, sửa typo, format, đổi tên biến cục bộ, sửa nhỏ 1 chỗ rõ ràng, hoặc chạy script tạm → xử lý trực tiếp theo `project-coding-workflow`.
2. **Ideation Path:** yêu cầu hoặc ý tưởng còn mơ hồ nghiệp vụ → dùng `grilling` / `domain-modeling` / `prototype` / `to-spec` để chốt spec trước khi mở loop.
3. **Chế độ & Profile cho vòng lặp Orca:**
   - **Hình dạng (`task` | `batch`):**
     - `task` (mặc định cho 1 tác vụ nhiều bước): mặc định **không** tự commit/push trừ khi có `--commit`, `--ship` hoặc người dùng yêu cầu.
     - `batch` (lô ticket GitHub / Linear): xử lý từng ticket tuần tự, commit nguyên tử theo `conventional-commits` trên nhánh xếp chồng (mặc định không push); chỉ push và mở PR khi có `--ship`.
   - **Coder (`--coder`):**
     - Mặc định `codex`: đọc `model` và `model_reasoning_effort` từ `~/.codex/config.toml` qua `orchctl.py preflight`.
     - Nếu truyền `--worker-model` / `--worker-effort`: bắt buộc truyền đủ cả cặp `--model` + `--effort` cho Codex và kiểm tra khớp `slug` / `supported_reasoning_levels` trong `~/.codex/models_cache.json`.
     - Hỗ trợ `antigravity` (hoặc `claude` nếu máy có cài).
   - **Profile Plan & Review (`--profile`):**
     - `self` (mặc định khi không truyền `--profile`): điều phối viên tự lập plan và tự review bằng `ponytail-review` + `security-audit`, chỉ mở worker code.
     - `antigravity` hoặc `codex`: mở `PLAN_AGENT` / `REVIEW_AGENT` độc lập chéo góc nhìn (khuyến nghị cho tác vụ nhạy cảm: thanh toán, giao dịch, phân quyền, DB/transaction, refactor rộng).
4. **Sổ cái tiến độ `<S>\ledger.md`:**
   - Dòng đầu ghi hình dạng, coder và profile đã chốt.
   - Mỗi đơn vị việc 1 dòng theo vòng đời `READY -> CODING -> VERIFYING -> REVIEWING -> FIXING -> COMMITTED -> REPORTED | STOPPED`, kèm nhánh, SHA và đường dẫn báo cáo.

## 1. Cơ chế điều phối theo môi trường Orca 1.4+ (Bắt buộc phân biệt)

- **Phiên Orca Native Chat / Bot (Antigravity Chat, Codex App trong Orca, Bot):**
  - **Tuyệt đối không chạy `orchctl.py wait` hay tự poll `orca orchestration check`**, vì `check` trong script sẽ rút mất mail khỏi hộp thư khiến Orca mất cơ chế đánh thức tự động.
  - Sau khi chạy `orchctl.py start` → **kết thúc lượt ngay (end turn)**; Orca tự đánh thức khi có `worker_done`, `question` hoặc `escalation`.
- **Phiên Terminal CLI thuần (không có auto-wake của chat):**
  - Chạy nền `python "<K>\scripts\orchctl.py" wait` (mỗi lượt < 575 giây), xử lý toàn bộ event trả về rồi mới `wait` tiếp.
- **Tương tác & đọc tiến độ worker:**
  - Luôn dùng `orca orchestration worker-read --dispatch <id> --source auto --limit 40 --json` và `orchctl.py reply` / `nudge` (ưu tiên `--body-file` trên Windows để tránh giới hạn độ dài dòng lệnh và lỗi escape).
  - Không dùng `orca terminal switch` hay `orca terminal read --screen` vì worker có thể là structured chat không có PTY.
- **Xử lý sự kiện từ worker:**
  - `worker_done` / `worker_settled`: chạy `python "<K>\scripts\orchctl.py" finish --dispatch <id>` để giải phóng worker, đọc báo cáo ở `--report-path` và tự chạy kiểm chứng thật (không tái dùng worker cũ cho vòng sửa mới).
  - `question`: nếu câu trả lời suy ra trực tiếp từ spec/quy tắc repo thì trả lời bằng `orchctl.py reply --id <msg_id> --body-file <file>`; nếu đụng quyết định nghiệp vụ hoặc đổi phạm vi thì hỏi người dùng trước.
  - `needs_input`: đọc `worker-read --source auto` để xác định yêu cầu input hoặc quyền duyệt và xử lý bằng `reply` / hỏi người có thẩm quyền.
  - `escalation` / `start` lỗi: không chạy lại mù quáng; kiểm tra `worker-show`, `failedStage`, `residualResources` và đối chiếu `orca skills get orchestration --reference references/recovery-and-cleanup.md`.
  - Worker dừng im lặng không gửi `worker_done` nhưng `worker-read` cho thấy lượt đã xong hoặc bị kẹt: `nudge` đúng 1 lần bằng `--body-file` trước khi mở worker thay thế.

## 2. Preflight & Nhận diện Stack đa nền tảng (1 lệnh gộp)

1. Chạy 1 lệnh preflight duy nhất:
   ```text
   python "<K>\scripts\orchctl.py" preflight --cwd "<wt>"
   ```
2. Lệnh kiểm tra `orca status --json` (`ok: true`, `runtime.state: ready`), đọc an toàn `codexDefaults` (`model` + `effort` top-level từ `~/.codex/config.toml`), liệt kê file quy tắc (`.local-rules`, `AGENTS.md`, `AGENT.md`, `CLAUDE.md`, `GLOSSARY.md`, `docs/adr`) và tự nhận diện stack theo HĐH (`Windows` vs `POSIX`):
   - **Java Maven** (`mvnw.cmd` / `mvnw` / `pom.xml`): Windows dùng `.\mvnw.cmd -DskipTests compile` và `.\mvnw.cmd -Dtest=<Class> test`; POSIX dùng `./mvnw ...`; fallback `mvn`.
   - **Gradle** (`gradlew.bat` / `gradlew` / `build.gradle*`): Windows dùng `.\gradlew.bat classes` và `.\gradlew.bat test --tests <Pattern>`; POSIX dùng `./gradlew ...`; fallback `gradle`.
   - **Go** (`go.mod`): `go build ./...`, `go vet ./...`, `go test <pkg>` (cuối vòng chạy `go test ./...`).
   - **Node / TS** (`package.json`): nhận diện lockfile (`pnpm` / `yarn` / `bun` / `npm`) và chạy các script `typecheck`, `lint`, `test`, `build` đang có.
   - **Rust / Python**: `cargo check --all-targets` + `cargo test` / `pytest`.
3. Tra cứu `agentmemory` (`recall` theo project slug nếu sẵn có) để lấy quyết định và gotcha cũ; đọc kỹ `.local-rules/`, `AGENTS.md` và `GLOSSARY.md` của repo.
4. **Quy tắc cứng với `.local-rules/`:** tài liệu SRS và quy tắc trong `.local-rules/` là nguồn **chỉ đọc** — cấm sửa, cấm redline, cấm stage hoặc commit thư mục `.local-rules/`.
5. **Worktree & Build tuần tự:**
   - Dùng `--worktree current` nếu workspace hiện tại đã cô lập, hoặc `--worktree new-child --name <short-name>` trên repo Git (với folder workspace dùng selector hiện có, cấm `git init`).
   - Không chạy song song 2 tiến trình build nặng trên cùng một thư mục đích.

## 3. Cổng Phê duyệt Thiết kế (Design Gate)

Trước khi giao worker sửa code, nếu phương án làm thay đổi một trong các yếu tố sau mà người dùng chưa chốt rõ:
- Logic nghiệp vụ, luồng async, DB transaction, locking, retry, state machine;
- Contract API/JSON/DB hoặc chạm vào module Core dùng chung.

Điều phối viên phải:
1. Trình bày ngắn gọn: vấn đề + bằng chứng từ code hiện tại, phương án tối giản (`ponytail` + `ducanh-code-rule`, chủ động phản biện nếu thấy hướng đi đang rườm rà), ưu/nhược điểm, rủi ro và cách kiểm chứng.
2. **Hỏi người dùng 1 lần gộp** trước khi giao code; ghi nội dung đã duyệt vào đầu spec dưới mục `QUYẾT ĐỊNH CỦA NGƯỜI DÙNG`.

## 4. Luồng `task` (Plan → Code → Verify ∥ Review → Tối đa 3 vòng sửa)

1. **Plan:** bỏ qua nếu người dùng đã chỉ rõ file và cách sửa; ngược lại tự lập plan (`self`) hoặc mở worker chỉ đọc (`PLAN_AGENT`) để chốt danh sách file sửa, luồng caller, rủi ro và tiêu chí nghiệm thu.
2. **Code — Hợp đồng Spec 5 mục bắt buộc:** worker không thấy lịch sử chat của bạn, nên file body dựng từ `<K>\worker-prompt.md` phải tự đủ nghĩa theo 5 mục:
   - **Target:** đường dẫn worktree, nhánh/base và phạm vi thay đổi.
   - **Change:** mô tả cụ thể nghiệp vụ/luồng cần sửa và phần tái sử dụng.
   - **Constraints:** vùng cấm chạm (`.local-rules/`, module Core ngoài scope, file dirty sẵn có).
   - **Test Policy:** cho phép hay cấm tạo/sửa test theo quy tắc repo và yêu cầu người dùng.
   - **Acceptance:** các lệnh build/test cụ thể và kết quả kỳ vọng (mã thoát `0`).
   Chạy tuần tự hai lệnh sau rồi chờ theo Mục 1 và gọi `finish --dispatch <id>` khi nhận `worker_done`:
   ```text
   python "<K>\scripts\orchctl.py" spec --cwd "<wt>" --body "<S>\body.md" --out "<S>\spec-0.md"
   python "<K>\scripts\orchctl.py" start --spec-file "<S>\spec-0.md" --agent <coder> [--model <m> --effort <e>] --worktree <selector> --title "<tiêu đề>"
   ```
3. **Kiểm chứng + Review độc lập:**
   - Lưu `git -C "<wt>" diff HEAD > "<S>\round-<n>.patch"` và kiểm tra `git -C "<wt>" status --short` (không lọt file rác, `.env`, `.local-rules/`).
   - Tự chạy lại các lệnh build/test thật của stack và xác nhận **exit code `0`** ("xanh" trong lời báo cáo của worker không phải bằng chứng).
   - **Review độc lập theo 3 trục (Spec & Local Rules, Code Quality & Database, Security):**
     - Nếu `--profile self`: trực tiếp chạy `ponytail-review` + `security-audit` trên code thật và callers.
     - Nếu mở worker reviewer mới: điền `<K>\reviewer-prompt.md` (tuyệt đối không kèm báo cáo hay lời giải thích của coder).
     - Chỉ giữ các finding đã xác minh trên code thật (`file:dòng` + kịch bản lỗi).
   - **Chính sách Test:** nếu `.local-rules/` hoặc người dùng cấm tạo file test thì tuân thủ tuyệt đối; ngược lại, khi sửa business logic / fix bug / refactor có rủi ro hồi quy mà thiếu test che phủ thì chạy baseline test và bổ sung/cập nhật unit regression test gọn đúng chỗ (theo `.codex/AGENTS.md`).
4. **Vòng sửa (tối đa 3 vòng):**
   - Ghi các finding `blocker`/`major` và lệnh đỏ vào `<S>\fix-<n>.md`, dựng `spec-<n>.md` bằng `spec --cwd "<wt>" --include "<S>\fix-<n>.md"`, giao worker coder mới (`minor` chỉ ghi vào báo cáo).
   - Quá 3 vòng vẫn còn lỗi, hoặc lặp đúng lỗi cũ mà không có hướng thử mới → chuyển **STOPPED**, giữ nguyên cây làm việc và báo cáo đầy đủ bằng chứng cho người dùng.
5. **Bàn giao:**
   - Tóm tắt thay đổi, danh sách lệnh kiểm chứng (kèm exit code), số vòng sửa và vấn đề tồn đọng.
   - Nếu có `--commit` hoặc `--ship`: xem 10 commit gần nhất (`git -C "<wt>" log --no-merges -n 10 --format="%s"`) và commit theo chuẩn `conventional-commits`; có `--ship` thì push nhánh và mở PR bằng skill `pr`.
   - Lưu quyết định hoặc gotcha đáng giá vào `agentmemory` (`remember`).

## 5. Luồng `batch` (Lô ticket GitHub / Linear)

1. **Frontier & Quét mâu thuẫn:**
   - Đọc từng ticket (`gh issue view <n> --json title,body,comments` hoặc `orca linear issue <id> --comments --relations --json`).
   - Xếp thứ tự phụ thuộc và đối chiếu chéo với `.local-rules/`, `AGENTS.md`, `GLOSSARY.md` cùng code hiện tại (`rg`).
   - Nếu phát hiện mâu thuẫn không thể tự giải đáp từ tài liệu → dừng cả lô và báo bằng chứng cụ thể.
2. **Xử lý tuần tự từng ticket:**
   - Vòng đời: `READY -> CODING (worker-prompt.md) -> VERIFYING (build/test thật) -> REVIEWING (3 trục) -> FIXING (tối đa 3 vòng + chốt dừng nếu lặp nguyên lỗi cũ) -> COMMITTED -> REPORTED`.
   - **Không `--ship`:** dùng nhánh xếp chồng (ticket sau tách từ đỉnh commit của ticket trước), commit nguyên tử theo `conventional-commits`, không push.
   - **Có `--ship`:** mỗi ticket tách nhánh sạch từ `origin/main` mới nhất; sau `COMMITTED`, push nhánh và mở PR bằng skill `pr` kèm `Closes #<ticket>`.
   - **Báo cáo ticket:** GitHub dùng `python "<K>\scripts\orchctl.py" report --cwd "<wt>" --ticket <n> --body "<S>\<id>\report.md"`; Linear dùng `orca linear comment add <id> --body-file "<S>\<id>\report.md" --json`.
3. **Cuối lô:** chạy lệnh build/test toàn repo một lần trên nhánh đích cuối và tổng hợp báo cáo kết quả cả lô.

## 6. Giới hạn 15 phút mỗi worker, An toàn & Kết thúc

- **Quá 15 phút chưa xong** (tính từ `started` trong `dispatches.json` hoặc `orchctl.py status`):
  1. Đọc `orca orchestration worker-read --dispatch <id> --source auto --limit 40 --json`, lưu `git -C "<wt>" diff HEAD > "<S>\<id>\partial-<n>.patch"` và `git -C "<wt>" status --short`.
  2. Dừng worker cũ an toàn: `orca orchestration worker-stop --dispatch <id> --json` rồi `python "<K>\scripts\orchctl.py" finish --dispatch <id>` (giữ nguyên cây làm việc).
  3. Dựng `spec` nối tiếp bằng `spec --include` kèm phần đã làm / còn lại / chỗ kẹt và mở worker mới trên trạng thái hiện có. Nếu worker thứ hai vẫn quá 15 phút mà diff không đổi so với `partial-<n>.patch` → **STOPPED**, báo bằng chứng.
- **Điểm dừng bắt buộc (`STOPPED`) & An toàn tuyệt đối:**
  - Dừng báo ngay khi thiếu quyền/môi trường chặn, mâu thuẫn tài liệu, lặp nguyên lỗi cũ, hết 3 vòng sửa, hoặc hành động hủy hoại là cách duy nhất để tiếp tục.
  - Cấm mọi lệnh git hủy hoại (`reset --hard`, `clean -fd`, `checkout -- .`, `push --force`).
  - **Không tự xóa cache build** (`Manual cache cleanup` — chỉ xóa khi người dùng yêu cầu rõ).
  - Không để lại file tạm ngoài `<S>` / `%TEMP%` (hoặc `/tmp`); không tự chọn thay người dùng ở các quyết định ngoài tài liệu.
- **Điều kiện kết thúc & Báo cáo mẫu:** chỉ kết thúc khi mọi Task đã có `worker_done` hoặc điểm dừng `STOPPED` và không còn worker treo:
  ```text
  Đơn vị: <tác vụ hoặc #ticket>   Trạng thái: <VERIFIED|COMMITTED|REPORTED|STOPPED>
  Chế độ/profile: <task|batch>/<self|antigravity|codex>   Vòng sửa: <n>   Nhánh/SHA: <...>
  Bằng chứng: <lệnh build/test, exit code, kết quả review 3 trục>
  Tồn đọng / Lưu ý: <không có hoặc chi tiết điểm dừng>
  ```
