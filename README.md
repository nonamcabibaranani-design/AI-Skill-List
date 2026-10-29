# AI-Skill-List

Danh mục skill dùng cho các AI coding agent. Repo lưu **skill tự tạo** trong `skills/`; skill từ dự án khác chỉ có link nguồn và hướng dẫn cài, không dùng submodule hay sao chép cả repo bên ngoài.

## Skill tự tạo

| Skill | Nội dung | Tệp chính |
|-------|----------|-----------|
| `ducanh-code-rule` | Viết, sửa và refactor Java theo project hiện tại; rà code để tái sử dụng trước khi tạo hàm chung mới, giữ code đơn giản, dễ mở rộng và package đúng trách nhiệm. Chỉ thêm test khi người dùng yêu cầu. | [SKILL.md](skills/ducanh-code-rule/SKILL.md) |

`ducanh-code-rule` có kèm metadata cho Codex trong `agents/openai.yaml` và các quy tắc Java dùng chung trong `references/project-conventions.md`. Áp dụng theo code, build và kiến trúc của project hiện tại, không cố định framework hoặc mô hình nghiệp vụ.

Skill đã đổi tên từ `java-code` sang `ducanh-code-rule`. Các agent cần cập nhật tên gọi thành `$ducanh-code-rule` và đường dẫn thành `skills/ducanh-code-rule/`. Khi cập nhật bản cài, thay thư mục `java-code` cũ bằng toàn bộ thư mục mới, gồm cả `agents/` và `references/`, để tránh giữ hai bản skill trùng nhau.

### Cài ducanh-code-rule

Cần Node.js/npm để chạy `npx`. Cài trực tiếp từ repo này cho Codex:

```bash
npx skills add nonamcabibaranani-design/AI-Skill-List --skill ducanh-code-rule -a codex -g
```

Thay `codex` bằng agent muốn dùng, ví dụ `claude-code` hoặc `cursor`. Bỏ `-g` nếu muốn cài ở phạm vi project. Xem danh sách agent và tùy chọn trong [tài liệu Skills CLI](https://github.com/vercel-labs/skills#readme).

Nếu muốn lấy repo về máy:

```bash
git clone https://github.com/nonamcabibaranani-design/AI-Skill-List.git
cd AI-Skill-List
```

Sau đó cài từ thư mục hiện tại:

```bash
npx skills add . --skill ducanh-code-rule -a codex -g
```

Hoặc chép **toàn bộ** `skills/ducanh-code-rule/` vào thư mục skills mà agent hỗ trợ; giữ cả `agents/` và `references/`.

## Skill từ nguồn bên ngoài

Chọn nguồn và skill cần dùng rồi cài trực tiếp từ upstream. Các link dưới đây dẫn tới tài liệu chính chủ để theo dõi cách cài và cập nhật của từng dự án.

| Nguồn | Skill tiêu biểu | Hướng dẫn cài chính chủ |
|-------|----------------|------------------------|
| [caveman](https://github.com/JuliusBrussee/caveman) | `caveman`, `caveman-commit`, `caveman-compress`, ... | [README](https://github.com/JuliusBrussee/caveman#readme) |
| [ponytail](https://github.com/DietrichGebert/ponytail) | `ponytail`, `ponytail-audit`, `ponytail-debt`, ... | [README](https://github.com/DietrichGebert/ponytail#readme) |
| [superpowers](https://github.com/obra/superpowers) | `brainstorming`, `systematic-debugging`, `test-driven-development`, ... | [README](https://github.com/obra/superpowers#readme) · [Cài cho Codex](https://github.com/obra/superpowers/blob/main/.codex/INSTALL.md) |
| [impeccable](https://github.com/pbakaus/impeccable) | Thiết kế, review và cải thiện giao diện | [README](https://github.com/pbakaus/impeccable#readme) |
| [vercel-skills](https://github.com/vercel-labs/skills) | `find-skills`; CLI khám phá và cài skill | [README](https://github.com/vercel-labs/skills#readme) |
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | Engineering và productivity: `domain-modeling`, `retro`, `code-review`, `tdd`, lập kế hoạch và triển khai | [Hướng dẫn chính chủ](https://github.com/mattpocock/skills#readme) |
| [Agent Memory](https://github.com/rohitg00/agentmemory) | Bộ nhớ lâu dài qua MCP; `memory-discipline`, `recall`, `remember`, `forget` | [Cài dịch vụ](https://github.com/rohitg00/agentmemory#install) · [Cài skills và kết nối agent](https://github.com/rohitg00/agentmemory#other-agents) |
| [graphify](https://github.com/Graphify-Labs/graphify) | Biến codebase, docs, schema thành knowledge graph; skill `/graphify` cho Claude Code, Cursor, Codex, Gemini CLI | [README](https://github.com/Graphify-Labs/graphify#readme) |
| [Context7](https://context7.com) | Tra cứu tài liệu và code example mới nhất theo phiên bản qua MCP (giảm hallucination) | [Tài liệu chính chủ](https://context7.com) |
| [Chrome DevTools MCP](https://github.com/ChromeDevTools/devtools-mcp) | MCP Server kết nối Chrome DevTools: inspect DOM, console logs, network cho Web/Frontend | [README](https://github.com/ChromeDevTools/devtools-mcp#readme) |
| [Playwright MCP](https://github.com/microsoft/playwright) | MCP Server tự động hóa browser: test E2E user flows, tương tác UI tự động | [Tài liệu npm](https://www.npmjs.com/package/@playwright/mcp) |

### Cài từng skill bằng Skills CLI

Liệt kê trước khi chọn:

```bash
npx skills add JuliusBrussee/caveman --list
npx skills add DietrichGebert/ponytail --list
npx skills add obra/superpowers --list
```

Ví dụ cài riêng một skill cho Codex:

```bash
npx skills add JuliusBrussee/caveman --skill caveman -a codex -g
npx skills add DietrichGebert/ponytail --skill ponytail -a codex -g
npx skills add obra/superpowers --skill systematic-debugging -a codex -g
npx skills add vercel-labs/skills --skill find-skills -a codex -g
```

Các lệnh này cài skill đã chọn vào nơi agent sử dụng; repo danh mục này không lưu bản sao upstream. Nếu cần cả plugin, hook hoặc thành phần đi kèm, làm theo hướng dẫn chính chủ ở bảng trên.

Impeccable có trình cài riêng. Chạy tại thư mục project:

```bash
npx impeccable install --providers=codex --scope=project
```

Sau đó chạy `/impeccable init` trong AI coding tool theo [hướng dẫn Impeccable](https://github.com/pbakaus/impeccable#readme).

### Matt Pocock: engineering và productivity

Bộ skill hỗ trợ hiểu codebase, làm rõ yêu cầu, lập kế hoạch, triển khai, review và rút kinh nghiệm. Các skill phát hành chính thức nằm trong `skills/engineering/` và `skills/productivity/`, được liệt kê trong [manifest của tác giả](https://github.com/mattpocock/skills/blob/main/.claude-plugin/plugin.json).

Liệt kê trước, rồi chọn lệnh cài cho Codex hoặc Antigravity. Trong màn chọn skills, chọn các skill thuộc hai nhóm trên; `in-progress` và `misc` là các phần ngoài bộ phát hành chính.

```bash
npx skills add mattpocock/skills --list
npx skills add mattpocock/skills -a codex -g
npx skills add mattpocock/skills -a antigravity -g
```

`-g` cài ở phạm vi người dùng. Để chỉ cài một vài skill, thêm tên cụ thể, ví dụ `--skill domain-modeling --skill retro --skill code-review`. Nếu dùng Antigravity CLI, thay `antigravity` bằng `antigravity-cli`.

Sau khi cài, mở phiên agent mới để nhận skills. Chạy `/setup-matt-pocock-skills` một lần trong project muốn áp dụng theo [hướng dẫn thiết lập](https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md); bước này thiết lập issue tracker, nhãn triage và nơi lưu glossary/ADR cho project đó.

### Agent Memory: dịch vụ MCP và skills

Agent Memory lưu và tìm lại quyết định, bối cảnh và bài học giữa các phiên làm việc. Cần **dịch vụ bộ nhớ đang chạy**, **kết nối MCP của agent** và **skills hướng dẫn cách đọc/lưu**; chỉ cài skills không thay thế hai phần đầu.

Cần Node.js **20 trở lên** cùng npm/npx. Chạy trình thiết lập chính thức:

```bash
npx -y @agentmemory/agentmemory@latest
```

Làm theo [hướng dẫn upstream](https://github.com/rohitg00/agentmemory#other-agents) để kết nối MCP cho agent đang dùng. Trên Windows native, cần cài thủ công `iii-engine` đúng phiên bản upstream chỉ định; xem [điều kiện cài đặt](https://github.com/rohitg00/agentmemory#install) trước khi chạy.

Liệt kê skills rồi cài riêng bộ cơ bản cho Codex hoặc Antigravity:

```bash
npx skills add rohitg00/agentmemory --list
npx skills add rohitg00/agentmemory --skill memory-discipline --skill recall --skill remember --skill forget -a codex -g
npx skills add rohitg00/agentmemory --skill memory-discipline --skill recall --skill remember --skill forget -a antigravity -g
```

`memory-discipline` hướng dẫn đọc bộ nhớ trước khi làm việc và lưu quyết định đã xác minh; `recall` tìm lại, `remember` lưu thêm, `forget` xóa ghi chú theo yêu cầu. Nếu dùng Antigravity CLI, thay `antigravity` bằng `antigravity-cli` theo [danh sách agent của Skills CLI](https://github.com/vercel-labs/skills#supported-agents).

Để Codex và Antigravity dùng chung bộ nhớ, cấu hình cả hai kết nối cùng một dịch vụ và dùng mã project nhất quán. Việc tự ghi/đọc còn phụ thuộc cấu hình và hooks của từng agent; kiểm tra bằng cách lưu một ghi chú rồi đọc lại từ agent còn lại. Repo này chỉ lưu hướng dẫn, không chứa dữ liệu bộ nhớ hay cấu hình riêng của máy.

### Graphify: knowledge graph cho codebase

Graphify phân tích mã nguồn, tài liệu, schema thành đồ thị tri thức (knowledge graph) chạy local hoàn toàn (AST parsing, không dùng vector store). Hỗ trợ Claude Code, Cursor, Codex, Gemini CLI và GitHub Copilot.

Cài đặt CLI bằng `uv` hoặc `pipx` (gói tên `graphifyy`):

```bash
uv tool install graphifyy
# hoặc: pipx install graphifyy
```

Tự động nhận diện trợ lý và đăng ký skill:

```bash
graphify install
```

Sử dụng trực tiếp trong AI coding tool:

```text
/graphify .
```

Kết quả sinh ra thư mục `graphify-out/` gồm `graph.html` (trực quan hóa tương tác), `GRAPH_REPORT.md` (tóm tắt liên kết và khái niệm chính) và `graph.json` (đồ thị cấu trúc).

### Context7: tra cứu tài liệu và code example mới nhất qua MCP

Context7 (phát triển bởi Upstash) giải quyết vấn đề AI bị lỗi thời kiến thức (stale training data) và sinh mã theo API cũ hoặc sai lệch (hallucination). Khi lập trình với các thư viện thay đổi liên tục (như Next.js, Tailwind, Supabase, LangChain...), Context7 tự động truy xuất tài liệu và ví dụ chính xác theo phiên bản đưa vào bối cảnh của agent.

Hỗ trợ đồng thời cho cả **Antigravity** và **Codex** (cũng như Claude Code, Cursor) qua chuẩn MCP:

1. **Thiết lập tự động qua CLI**:
   ```bash
   npx ctx7 setup
   ```

2. **Cấu hình thủ công cho Antigravity** (`~/.gemini/config/mcp_config.json`):
   ```json
   {
     "mcpServers": {
       "context7": {
         "command": "npx",
         "args": ["-y", "@upstash/context7-mcp"]
       }
     }
   }
   ```
   *(Hoặc dùng trực tiếp endpoint remote HTTP: `"url": "https://mcp.context7.com/mcp"`)*

3. **Cấu hình thủ công cho Codex** (`~/.codex/config.toml`):
   ```toml
   [mcp_servers.context7]
   command = "npx"
   args = ["-y", "@upstash/context7-mcp"]
   ```

---

### Bộ công cụ MCP cho Web / Frontend: Chrome DevTools & Playwright

> **Khuyến nghị**: Nên cài nếu anh làm **Web / Frontend**. Giúp AI theo phong cách *vibe coding* tự kiểm tra giao diện, bắt lỗi console/network và tự động sửa lỗi ngay trong chu trình lập trình.

Hai công cụ bổ trợ nhau:
- **Chrome DevTools MCP**: Cho phép agent kết nối vào trình duyệt Chrome qua DevTools Protocol để đọc log console, theo dõi network requests lỗi và soi cấu trúc DOM khi web đang chạy.
- **Playwright MCP**: Cho phép agent mở browser, tương tác click, nhập form, chụp ảnh màn hình và chạy kiểm thử E2E mô phỏng hành vi người dùng thật.

**Cấu hình cho Antigravity** (`~/.gemini/config/mcp_config.json`):
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

**Cấu hình cho Codex** (`~/.codex/config.toml`):
```toml
[mcp_servers.chrome-devtools]
command = "npx"
args = ["-y", "chrome-devtools-mcp"]

[mcp_servers.playwright]
command = "npx"
args = ["-y", "@playwright/mcp@latest"]
```

Sau khi cấu hình, khởi động lại phiên làm việc của Antigravity hoặc Codex để agent tự nhận diện và nạp các công cụ này.

## Cập nhật và đóng góp

- Cập nhật skill tự tạo: sửa nội dung trong `skills/<tên-skill>/`, gồm `SKILL.md` và tài liệu cần thiết.
- Bổ sung skill bên ngoài: thêm link upstream và hướng dẫn cài vào bảng; không thêm submodule, bản fork hoặc cả thư mục nguồn.
- `git pull` cập nhật danh mục và skill tự tạo. Skill bên ngoài được cập nhật bằng công cụ cài của từng nguồn.
