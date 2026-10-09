# Quy tắc chung cho project Java

Áp dụng các quy tắc dưới đây theo yêu cầu và kiến trúc của project hiện tại. Đọc cấu hình build, code liên quan và quy ước của repository trước khi sửa; không mặc định phiên bản Java, framework, tên package hay mô hình nghiệp vụ.

## Cấu trúc và trách nhiệm

- Đặt class trong package hoặc module sở hữu trách nhiệm của nó. Theo cách tổ chức hiện có theo domain hoặc theo tầng; tránh đưa code riêng của một nghiệp vụ vào package dùng chung.
- Với ứng dụng phân tầng, controller hoặc entry point tiếp nhận đầu vào và chuyển cho tầng xử lý nghiệp vụ; repository hoặc lớp truy cập dữ liệu phụ trách persistence. Với kiến trúc khác, giữ ranh giới tương ứng của project.
- Tái sử dụng component và cơ chế dependency injection đang có. Khi có nhiều implementation, kiểm tra cách chọn dependency, vòng đời và cấu hình đăng ký; không dựa vào tên class để suy đoán implementation thực tế.
- Chỉ tách interface, base class hoặc module dùng chung khi có nhu cầu cụ thể. Ưu tiên cấu trúc nhỏ nhất giải quyết được yêu cầu.

## Chọn và mở rộng design pattern

- Bắt đầu bằng cách triển khai trực tiếp. Dùng pattern khi nó giải quyết sự lặp lại hoặc biến thể đã tồn tại; không thêm pattern chỉ để chuẩn bị cho nhu cầu giả định.
- Với Strategy, xác định điều kiện chọn và cách xử lý trường hợp không khớp hoặc khớp nhiều implementation theo hợp đồng nghiệp vụ. Không tự đổi thứ tự ưu tiên hoặc fallback của cơ chế hiện có.
- Với Factory hoặc registry, kiểm tra khóa tra cứu, quy tắc đăng ký và xử lý khóa không hợp lệ. Giữ cấu hình nhất quán với nơi sử dụng.
- Với Template Method, chỉ mở rộng khi luồng mới phù hợp hợp đồng, thứ tự xử lý và các hook của base class. Nếu không phù hợp, chọn cách triển khai độc lập thay vì ép kế thừa.

## Persistence và transaction

- Lần theo entity, repository và cấu hình để xác định dữ liệu thuộc nguồn nào. Trong ứng dụng có nhiều datasource, chọn đúng persistence context và transaction manager; không suy ra từ tên API hoặc domain gọi vào.
- Xác định ranh giới transaction theo thao tác cần nhất quán. Kiểm tra hành vi commit, rollback, propagation và lời gọi qua proxy nếu framework sử dụng chúng.
- Không giả định một transaction cục bộ bao phủ nhiều datasource hoặc dịch vụ bên ngoài. Khi yêu cầu cần phối hợp các tài nguyên đó, xác minh cơ chế hiện có và đề xuất thay đổi trong phạm vi được chấp thuận.
- Bind parameter khi tạo truy vấn. Với tìm kiếm và phân trang, giữ điều kiện lọc nhất quán giữa truy vấn dữ liệu và truy vấn đếm; kiểm tra thứ tự sắp xếp, số trang, kích thước trang và tổng bản ghi theo contract.
- Giữ các ràng buộc và cơ chế xử lý đồng thời mà nghiệp vụ đang dựa vào. Chỉ thêm hoặc đổi locking, retry và cơ chế chống xử lý trùng khi đã có yêu cầu hoặc phương án được chấp thuận.

## DTO, response, exception và mapping

- Theo hợp đồng dữ liệu đang được caller sử dụng: tên trường, kiểu dữ liệu, nullability, giá trị mặc định, serialization và cấu trúc phân trang. Xem cả nơi tạo và nơi đọc dữ liệu trước khi sửa.
- Dùng cơ chế response và xử lý lỗi của project. Khi refactor, giữ ý nghĩa mã lỗi, HTTP status nếu có, thông điệp và cách ánh xạ exception; thay đổi hành vi phải nằm trong phạm vi được chấp thuận.
- Đặt validation ở ranh giới phù hợp với trách nhiệm của module. Phân biệt đầu vào không hợp lệ, lỗi nghiệp vụ và lỗi hạ tầng theo quy ước hiện có.
- Khi dùng thư viện sinh mapper hoặc code, sửa nguồn khai báo và cấu hình; không sửa trực tiếp file sinh ra trong thư mục build.
- Đọc cấu hình build để xác định dependency, annotation processor và namespace đang dùng. Không tự nâng phiên bản hoặc migration framework trong một thay đổi không yêu cầu việc đó.

## Kiểu dữ liệu và tính đúng nghiệp vụ

- Với tiền, số lượng và tỷ lệ, xác định đơn vị, độ chính xác, scale và quy tắc làm tròn. Dùng kiểu phù hợp với contract, như số nguyên theo đơn vị nhỏ nhất hoặc `BigDecimal`; tránh sai số dấu phẩy động trong phép tính yêu cầu độ chính xác thập phân.
- Với ngày giờ, làm rõ đó là thời điểm tuyệt đối, ngày lịch hay giờ địa phương. Giữ format, timezone và ranh giới khoảng lọc nhất quán giữa API, xử lý nghiệp vụ và nơi lưu trữ.
- Lấy danh tính và quyền từ cơ chế xác thực được project tin cậy. Kiểm tra điều kiện chuyển trạng thái và quyền thao tác ở nơi thực thi nghiệp vụ.
- Khi sửa một luồng, rà cả các tác động liên quan như lịch sử, audit, sự kiện và thông báo. Giữ tính nhất quán của các bước đã có; không tự bổ sung tác động mới ngoài yêu cầu.
- Log đủ để chẩn đoán và theo dõi luồng. Không ghi credential, token hoặc payload chứa dữ liệu nhạy cảm vào log.

## Kiểm tra và bàn giao

- Đọc build file và dùng wrapper hoặc công cụ đã có để kiểm tra phần thay đổi. Chọn lệnh theo module, build system và môi trường thực tế.
- Nếu thiếu JDK, dependency hoặc tài nguyên môi trường, báo rõ phần chưa kiểm chứng. Không thay thư viện hoặc nâng phiên bản chỉ để làm build thành công.
- Chỉ thêm file test hoặc bổ sung test khi người dùng yêu cầu rõ ràng. Có thể chạy test hiện có để xác minh theo yêu cầu của project; xem đầy đủ quy tắc tại [SKILL.md](../SKILL.md).
- Kiểm tra diff, caller và các hợp đồng bị ảnh hưởng; báo ngắn thay đổi, cách đã kiểm tra và giới hạn còn lại.
