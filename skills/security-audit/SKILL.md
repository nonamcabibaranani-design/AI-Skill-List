---
name: security-audit
description: "Rà soát bảo mật & lỗ hổng an toàn ứng dụng (Security Audit & Vulnerability Scanning) dựa trên chuẩn OWASP Top 10 và ECC AgentShield. Quét và ngăn chặn SQL Injection, BOLA/IDOR (truy cập trái phép đối tượng), lộ lọt Secret/Credential, XSS, Path Traversal, ReDoS và rò rỉ dữ liệu nhạy cảm trong log."
---

# Security Audit & Vulnerability Scanning

Skill kiểm tra an toàn và bảo mật mã nguồn trước khi tích hợp vào nhánh chính hoặc đưa lên production.

---

## 1. Phòng chống SQL Injection (SQLi) - Tuyệt đối không khoan nhượng

* **Bắt buộc tham số hóa (Parameterized Queries / Prepared Statements):**
  * ❌ Nghiêm cấm mọi hình thức nối chuỗi (string concatenation, template literal, string interpolation, `String.format`) để đưa biến vào câu query SQL.
  *  Bắt buộc dùng bind variables (`?`, `:param`, `$1`), hoặc các hàm an toàn của ORM/Query Builder.
* **Cẩn trọng với Dynamic Order By / Column Names:**
  * Nếu tên cột sắp xếp lấy từ client, bắt buộc phải dùng **Whitelist mapping** (đối chiếu tên cột với một tập giá trị hợp lệ cố định), không đưa trực tiếp chuỗi từ request vào mệnh đề `ORDER BY`.

---

## 2. Kiểm soát truy cập đối tượng (BOLA / IDOR Protection)

Lỗ hổng phổ biến nhất trong các ứng dụng: Người dùng A sửa/xem dữ liệu của Người dùng B chỉ bằng cách đổi ID trên URL.

* **Luôn xác thực quyền sở hữu (Ownership Check):**
  * Không bao giờ tin tưởng client. Khi truy vấn hoặc cập nhật theo `entity_id`, bắt buộc phải kèm theo điều kiện định danh của người dùng hiện tại:
    * ❌ `SELECT * FROM orders WHERE id = :orderId;` ➔ ai đoán được ID cũng xem được đơn!
    *  `SELECT * FROM orders WHERE id = :orderId AND user_id = :currentUserId;`
* **Phân quyền tại Service/Endpoint (RBAC/ABAC):**
  * Kiểm tra đầy đủ annotation/middleware phân quyền (`@PreAuthorize`, `@RolesAllowed`, middleware auth) tại mọi endpoint nhạy cảm (admin, cấu hình, thanh toán).

---

## 3. Quản lý Secret & Ngăn ngừa rò rỉ dữ liệu nhạy cảm

* **Không bao giờ hardcode bí mật trong mã nguồn:**
  * Tuyệt đối không để API key, token bí mật, JWT secret, private key, mật khẩu database trong file code hay file test. Toàn bộ phải nạp qua Environment Variables hoặc Secret Manager.
* **Ngăn rò rỉ thông tin trong Logs:**
  * ❌ Nghiêm cấm ghi log mật khẩu thô, số thẻ tín dụng, mã CVV, chuỗi JWT token, hoặc thông tin định danh cá nhân nhạy cảm (PII).
  * Che mờ (masking) dữ liệu trước khi log nếu cần trace request (ví dụ: `0987***321`, `**** **** **** 1234`).
* **Không để lộ stack trace ra phía client:**
  * Xử lý lỗi tập trung qua Global Exception Handler, chỉ trả về mã lỗi và thông báo thân thiện; không quăng nguyên Exception stack trace (chứa thông tin nội bộ table/code) cho người dùng cuối.

---

## 4. Kiểm tra đầu vào & Khử độc (Input Validation & Sanitization)

* **Phòng chống Path Traversal (Leo thang đường dẫn):**
  * Khi đọc/ghi file từ tên do client truyền lên: Kiểm tra và cấm các ký tự `../`, `..\\`, giải quyết đường dẫn tuyệt đối bằng `Path.normalize()` và kiểm tra đường dẫn phải nằm trọn trong thư mục gốc cho phép.
* **Phòng chống ReDoS (Regular Expression Denial of Service):**
  * Tránh các biểu thức chính quy lồng nhau không an toàn (ví dụ: `(a+)+$`). Cân nhắc timeout khi chạy regex trên chuỗi đầu vào tùy ý từ client.
* **XSS (Cross-Site Scripting):**
  * HTML encoding toàn bộ dữ liệu do người dùng nhập trước khi render lên trình duyệt. Thiết lập Content-Security-Policy (CSP) nếu có tầng frontend.

---

## 5. An toàn thay đổi trạng thái (State & Financial Operations)

* **Khóa chống trùng lặp (Idempotency):**
  * Với các thao tác trừ tiền, tạo đơn, gửi thông báo: bắt buộc có cơ chế Idempotency Key (hoặc Unique Constraint) để chặn click đúp hoặc client retry làm trừ tiền 2 lần.
* **Transaction Rollback rõ ràng:**
  * Đảm bảo mọi nhánh xử lý lỗi trong nghiệp vụ ghi dữ liệu đều kích hoạt Rollback, tránh tình trạng dữ liệu nửa chừng (ví dụ: trừ ví thành công nhưng lưu đơn thất bại).
