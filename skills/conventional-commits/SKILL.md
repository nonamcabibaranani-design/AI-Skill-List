---
name: conventional-commits
description: "Quy chuẩn viết commit message theo Conventional Commits 1.0.0 (feat, fix, refactor, perf, chore, build, ci, docs...). Tuân thủ nguyên tắc commit nguyên tử (Atomic Commit), thể mệnh lệnh (imperative mood), scope rõ ràng và đánh dấu Breaking Changes chuẩn chỉ."
---

# Conventional Commits Specification

Skill chuẩn hóa cách viết Git Commit Message cho toàn bộ các tác vụ lập trình và quản lý phiên bản.

---

## 1. Cấu trúc chuẩn của một Commit Message

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

* **Ví dụ đơn giản:**
  ```text
  feat(auth): add refresh token rotation mechanism
  fix(payment): resolve race condition during wallet balance deduction
  refactor(order): simplify status transition state machine
  perf(user): optimize customer lookup query using composite index
  chore(deps): upgrade spring-boot to 3.4.1
  ```

---

## 2. Các Type được phép sử dụng

| Type | Ý nghĩa và trường hợp áp dụng |
| :--- | :--- |
| **`feat`** | Một tính năng hoặc API mới cho người dùng / hệ thống. |
| **`fix`** | Sửa một lỗi / bug trong code đang chạy. |
| **`refactor`** | Thay đổi code mà không làm đổi hành vi bên ngoài (không thêm tính năng, không sửa bug). |
| **`perf`** | Cải thiện hiệu năng (tăng tốc độ query, giảm dùng RAM, tối ưu loop). |
| **`docs`** | Chỉ thay đổi tài liệu (README, GLOSSARY, ADR, hướng dẫn). |
| **`style`** | Thay đổi format, căn dòng, xóa khoảng trắng thừa (không ảnh hưởng tới logic chạy). |
| **`test`** | Bổ sung hoặc sửa đổi các file test (khi người dùng yêu cầu). |
| **`build`** | Thay đổi hệ thống build hoặc dependency (`pom.xml`, `build.gradle`, `package.json`). |
| **`ci`** | Thay đổi cấu hình CI/CD (GitHub Actions, GitLab CI, Dockerfile, pipeline). |
| **`chore`** | Các công việc phụ trợ, cập nhật công cụ, dọn dẹp file cấu hình nhỏ. |
| **`revert`** | Hoàn tác một commit trước đó. |

---

## 3. Quy tắc bắt buộc khi soạn Description & Body

1. **Thể mệnh lệnh (Imperative Mood):**
   *  `add mechanism`, `fix issue`, `refactor service`, `remove deprecated field`.
   * ❌ Không dùng quá khứ hoặc ngôi thứ 3: `added mechanism`, `fixes issue`, `refactored service`.
2. **Quy ước ký tự:**
   * Viết thường toàn bộ phần description sau dấu `:` (trừ danh từ riêng/tên class).
   * **Không có dấu chấm `.` ở cuối dòng đầu tiên.**
3. **Scope (Phạm vi):**
   * Đặt trong dấu ngoặc đơn: `<type>(<scope>):`.
   * Nên dùng tên feature, module, domain hoặc layer: `(auth)`, `(order)`, `(db)`, `(api)`, `(dto)`.
4. **Nguyên tắc Commit nguyên tử (Atomic Commit):**
   * Mỗi commit chỉ giải quyết **một mục đích logic duy nhất**. Không gộp một đống thay đổi không liên quan (ví dụ vừa refactor auth vừa sửa bug order) vào chung 1 commit.

---

## 4. Khai báo Breaking Changes (Thay đổi phá vỡ tương thích)

Nếu thay đổi làm hỏng tương thích ngược (đổi signature API, xóa trường DTO, đổi kiểu dữ liệu DB):
* **Cách 1:** Thêm dấu chấm than `!` ngay sau type/scope:
  ```text
  feat(api)!: drop support for legacy v1 user endpoint
  ```
* **Cách 2:** Thêm đoạn `BREAKING CHANGE:` ở footer giải thích lý do và cách migration:
  ```text
  refactor(auth): migrate token payload structure

  BREAKING CHANGE: The `sub_id` claim in JWT has been replaced with `user_uuid`.
  ```

---

## 5. Thói quen trước khi Commit trong Repo
Trước khi commit, hãy liếc nhanh 10 commit gần nhất của repo để bắt chước phong cách đặt scope của team:
```bash
git log --no-merges -n 10 --format="%s"
```
