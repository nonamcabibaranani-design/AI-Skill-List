# AI-Skill-List

Danh mục skill dùng cho các AI coding agent. Repo lưu **skill tự tạo** trong `skills/`; skill từ dự án khác chỉ có link nguồn và hướng dẫn cài, không dùng submodule hay sao chép cả repo bên ngoài.

## Skill tự tạo

| Skill | Nội dung | Tệp chính |
|-------|----------|-----------|
| `java-code` | Viết, sửa và refactor Java theo project hiện tại; ưu tiên code đơn giản, package đúng trách nhiệm. Chỉ thêm test khi người dùng yêu cầu. | [SKILL.md](skills/java-code/SKILL.md) |

`java-code` có kèm metadata cho Codex trong `agents/openai.yaml` và các quy tắc Java dùng chung trong `references/project-conventions.md`. Áp dụng theo code, build và kiến trúc của project hiện tại, không cố định framework hoặc mô hình nghiệp vụ.

### Cài java-code

Cần Node.js/npm để chạy `npx`. Cài trực tiếp từ repo này cho Codex:

```bash
npx skills add nonamcabibaranani-design/AI-Skill-List --skill java-code -a codex -g
```

Thay `codex` bằng agent muốn dùng, ví dụ `claude-code` hoặc `cursor`. Bỏ `-g` nếu muốn cài ở phạm vi project. Xem danh sách agent và tùy chọn trong [tài liệu Skills CLI](https://github.com/vercel-labs/skills#readme).

Nếu muốn lấy repo về máy:

```bash
git clone https://github.com/nonamcabibaranani-design/AI-Skill-List.git
cd AI-Skill-List
```

Sau đó cài từ thư mục hiện tại:

```bash
npx skills add . --skill java-code -a codex -g
```

Hoặc chép **toàn bộ** `skills/java-code/` vào thư mục skills mà agent hỗ trợ; giữ cả `agents/` và `references/`.

## Skill từ nguồn bên ngoài

Chọn nguồn và skill cần dùng rồi cài trực tiếp từ upstream. Các link dưới đây dẫn tới tài liệu chính chủ để theo dõi cách cài và cập nhật của từng dự án.

| Nguồn | Skill tiêu biểu | Hướng dẫn cài chính chủ |
|-------|----------------|------------------------|
| [caveman](https://github.com/JuliusBrussee/caveman) | `caveman`, `caveman-commit`, `caveman-compress`, ... | [README](https://github.com/JuliusBrussee/caveman#readme) |
| [ponytail](https://github.com/DietrichGebert/ponytail) | `ponytail`, `ponytail-audit`, `ponytail-debt`, ... | [README](https://github.com/DietrichGebert/ponytail#readme) |
| [superpowers](https://github.com/obra/superpowers) | `brainstorming`, `systematic-debugging`, `test-driven-development`, ... | [README](https://github.com/obra/superpowers#readme) · [Cài cho Codex](https://github.com/obra/superpowers/blob/main/.codex/INSTALL.md) |
| [impeccable](https://github.com/pbakaus/impeccable) | Thiết kế, review và cải thiện giao diện | [README](https://github.com/pbakaus/impeccable#readme) |
| [vercel-skills](https://github.com/vercel-labs/skills) | `find-skills`; CLI khám phá và cài skill | [README](https://github.com/vercel-labs/skills#readme) |

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

## Cập nhật và đóng góp

- Cập nhật skill tự tạo: sửa nội dung trong `skills/<tên-skill>/`, gồm `SKILL.md` và tài liệu cần thiết.
- Bổ sung skill bên ngoài: thêm link upstream và hướng dẫn cài vào bảng; không thêm submodule, bản fork hoặc cả thư mục nguồn.
- `git pull` cập nhật danh mục và skill tự tạo. Skill bên ngoài được cập nhật bằng công cụ cài của từng nguồn.
