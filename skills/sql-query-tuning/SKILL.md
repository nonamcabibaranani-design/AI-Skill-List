---
name: sql-query-tuning
description: "Quy chuẩn tối ưu truy vấn Database & SQL (Performance & Query Tuning) lấy cảm hứng từ ECC database-reviewer và các best practice chuẩn công nghiệp. Nhận diện và diệt triệt để N+1 queries, tối ưu Indexing (B-Tree, Composite, Covering), Keyset pagination, tối giản transaction và batching."
---

# SQL & Database Query Tuning

Skill chuyên sâu về tối ưu hiệu năng cơ sở dữ liệu và truy vấn SQL (tương thích cả SQL thuần, JPA/Hibernate, MyBatis, Prisma hay các ORM/Query Builder).

---

## 1. Triệt tiêu vấn đề N+1 Query (Critical)

N+1 là nguyên nhân số 1 làm chậm ứng dụng khi load danh sách:
* **Dấu hiệu:** Chạy 1 query lấy danh sách cha (N phần tử), sau đó chạy N query con trong vòng lặp để lấy dữ liệu liên quan.
* **Quy tắc xử lý:**
  * **JPA/Hibernate:** Luôn dùng `JOIN FETCH` (hoặc `@EntityGraph`) khi cần lấy dữ liệu quan hệ; không để ORM tự lazy load trong loop.
  * **SQL thuần / MyBatis:** Dùng `JOIN` kết hợp projection, hoặc gom danh sách ID rồi query 1 lần với mệnh đề `IN (:ids)` / `ANY(ARRAY[...])`.
  * **Batch Fetching:** Cấu hình batch size hợp lý (ví dụ: `default_batch_fetch_size: 50-100`) để gom query tự động nếu dùng ORM.

---

## 2. Chiến lược thiết kế & sử dụng Index

Index là con dao hai lưỡi (tăng tốc đọc, làm chậm ghi). Chỉ thêm index khi có căn cứ:

* **Nguyên tắc tiền tố bên trái (Leftmost Prefix Rule) với Composite Index:**
  * Với composite index `(colA, colB, colC)`, query phải filter theo `colA` thì index mới hoạt động. Sắp xếp thứ tự cột trong index theo: Cột có độ chọn lọc cao nhất (high cardinality) ➔ Cột dùng trong `WHERE =` ➔ Cột dùng trong `ORDER BY` / `GROUP BY` ➔ Cột dùng trong khoảng `<, >, BETWEEN`.
* **Covering Index (Tận dụng mệnh đề INCLUDE hoặc gom cột):**
  * Gom các cột cần `SELECT` vào index để Database lấy dữ liệu trực tiếp từ cây index (Index-Only Scan), không cần tốn IO đọc lại table data page.
* **Tránh triệt tiêu Index trong mệnh đề `WHERE`:**
  * ❌ `WHERE YEAR(created_at) = 2026` ➔ Database buộc phải Full Table Scan.
  *  `WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'`.
  * ❌ `WHERE LOWER(email) = 'abc@test.com'` (trừ khi có Functional Index).
* **Luôn đánh Index cho Khóa ngoại (Foreign Keys):**
  * Các trường liên kết (như `user_id`, `order_id`) thường xuyên xuất hiện trong `JOIN` và `WHERE`, bắt buộc phải có index để tránh lock bảng và scan chậm.

---

## 3. Tối ưu phân trang dữ liệu lớn (Pagination)

* **Hạn chế `OFFSET` lớn (Deep Paging):**
  * ❌ `LIMIT 20 OFFSET 500000` khiến Database phải đọc và bỏ qua 500.000 dòng trước khi lấy 20 dòng.
* **Thay thế bằng Keyset Pagination (Cursor-based):**
  *  `WHERE id < :last_seen_id ORDER BY id DESC LIMIT 20`.
  * Hoặc dùng Deferred Join: Chỉ tìm ID qua index trước, rồi JOIN lại bảng chính để lấy chi tiết.

---

## 4. Tối ưu Transaction & Concurrency

* **Giữ Transaction ngắn nhất có thể:**
  * Tuyệt đối **không gọi HTTP/API bên ngoài, gửi email, đọc file hoặc xử lý tính toán nặng** bên trong một DB Transaction. Mở connection muộn nhất và commit sớm nhất.
* **Ngăn chặn Deadlock:**
  * Luôn cập nhật/khóa các tài nguyên theo cùng một thứ tự nhất quán giữa các tiến trình (ví dụ: luôn sort danh sách ID theo thứ tự tăng dần trước khi `SELECT FOR UPDATE`).
* **Chọn đúng Transaction Isolation Level:**
  * Dùng `READ COMMITTED` cho hầu hết các tác vụ thông thường. Chỉ nâng lên `REPEATABLE READ` hoặc `SERIALIZABLE` khi thật sự có nguy cơ phantom read / write skew nguy hiểm và đã đo lường chi phí retry.

---

## 5. Giảm thiểu Data Transfer & Batching

* **Không dùng `SELECT *` trong code nghiệp vụ:**
  * Chỉ SELECT các cột cần thiết. Dùng DTO Projection để tiết kiệm băng thông mạng và bộ nhớ JVM/Node.
* **Batching cho tác vụ ghi khối lượng lớn (Bulk Writes):**
  * ❌ Insert/Update từng dòng trong vòng for.
  *  Dùng Batch Insert (`INSERT INTO table VALUES (...), (...)`) với batch size từ 500 – 1000 dòng mỗi batch.
