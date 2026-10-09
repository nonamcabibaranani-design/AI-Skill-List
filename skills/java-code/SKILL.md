---
name: java-code
description: "Viết, sửa và refactor code Java theo cấu trúc project đang mở; ưu tiên code đơn giản, package đúng trách nhiệm và design pattern phù hợp. Dùng cho yêu cầu triển khai Java, không cố định phiên bản Java hay framework. Chỉ thêm test khi người dùng yêu cầu rõ ràng."
---

# Java Code

Áp dụng khi triển khai, sửa lỗi hoặc refactor Java. Dùng các quy tắc chung theo yêu cầu, cấu hình và kiến trúc của project hiện tại; không mặc định phiên bản Java, framework hoặc mô hình nghiệp vụ.

## Yêu cầu của người dùng

- **Đề xuất trước khi thay đổi logic.** Trước khi thay đổi nghiệp vụ hoặc hành vi xử lý, phải trình bày vấn đề và bằng chứng, phương án sửa và phạm vi, ưu/nhược điểm, ảnh hưởng/rủi ro và cách kiểm chứng. Đặc biệt áp dụng cho async, transaction, locking, retry, chuyển trạng thái, validation và refactor làm thay đổi hành vi. Chờ người dùng chọn hoặc chấp thuận phương án rồi mới sửa code. Nếu người dùng đã chỉ rõ phương án/phạm vi hoặc đã chấp thuận chúng, thực hiện đúng phần đó và không hỏi lại cho cùng phương án.
- **Không tự mở rộng phạm vi sửa lỗi.** Yêu cầu rà soát, kiểm tra, sửa một lỗi hoặc "sửa code thôi" không tự động cho phép bổ sung logic, validation, thay đổi kiến trúc hay cơ chế thực thi ngoài lỗi đã chỉ định. Phân biệt nguyên nhân đã kiểm chứng với rủi ro chỉ suy luận từ code; nêu các đề xuất bổ sung riêng để người dùng quyết định, không dùng rủi ro giả định làm lý do tự thay đổi luồng đang chạy.
- **Giữ bản sửa đúng phạm vi đã chốt.** Khi sửa trường dữ liệu hoặc mapping đã xác định, giữ các cơ chế async/transaction và workflow hiện tại trừ khi người dùng chấp thuận thay đổi chúng. Tái sử dụng hook và cấu trúc hiện có, không tự thêm tầng kiểm tra hoặc lớp điều phối. Đọc code, phân tích, kiểm tra build và dọn import không thay đổi hành vi có thể thực hiện trực tiếp.

- **Chỉ tạo file test hoặc bổ sung test khi người dùng yêu cầu rõ ràng.** Yêu cầu code, sửa bug, refactor, kiểm tra hay build không tự động cho phép thêm test. Không tự sinh test class, test fixture hoặc thêm dependency phục vụ test. Giữ nguyên các test đang có, trừ khi người dùng yêu cầu chỉnh sửa chúng.
- **Không gắn skill với phiên bản cụ thể.** Xác định Java, framework, dependency, namespace và build tool từ project đang mở. Dùng cú pháp/API tương thích với cấu hình đó; chỉ nâng cấp khi nằm trong yêu cầu của người dùng.
- **Ưu tiên code đơn giản, dễ đọc và đúng nghiệp vụ.** Chọn cách triển khai nhỏ nhất đáp ứng đầy đủ yêu cầu. Không thêm lớp trung gian, interface, generic framework hoặc dependency để phục vụ nhu cầu giả định.
- **Tận dụng class và code hiện có trước khi tạo mới.** Trước khi thêm class, DTO, subclass, converter, wrapper hoặc helper, kiểm tra cấu trúc, caller và cách dùng hiện tại để tái sử dụng trực tiếp. Chỉ tạo mới khi có trách nhiệm, hành vi hoặc contract thực sự khác mà code hiện có không đáp ứng hợp lý; không tạo class để phục vụ cách tách luồng hoặc chuyển đổi dữ liệu không cần thiết.
- **DTO dùng chung có thể có trường không áp dụng cho một luồng.** Tiếp tục dùng DTO chung và bỏ qua trường đó trong xử lý của luồng tương ứng nếu vẫn đáp ứng nghiệp vụ. Không tạo DTO/subclass riêng chỉ để ẩn hoặc bỏ một trường, không làm thay đổi các luồng vẫn sử dụng trường đó. Nếu API hiện tại đã trả trực tiếp được giá trị đúng kiểu người dùng yêu cầu, dùng luôn cấu trúc hiện có.
- **Chỉ comment khi cần thiết.** Comment giải thích lý do, quy tắc nghiệp vụ khó suy ra, giới hạn tích hợp hoặc quyết định có chủ đích. Ưu tiên tên rõ nghĩa và tách hàm hợp lý. Không comment diễn giải lại từng dòng, thêm thông tin tác giả/ngày tạo, sinh Javadoc hình thức hay giữ code đã comment out.

## Đọc ngữ cảnh trước khi sửa

1. Đọc hướng dẫn áp dụng cho repository, trạng thái thay đổi hiện tại và file build liên quan (`pom.xml`, cấu hình Gradle hoặc tương đương).
2. Xác định domain/use case cần sửa; lần theo một luồng tương tự từ đầu vào đến service, repository và dữ liệu trả về. Đọc thêm các caller khi thay đổi contract dùng chung.
3. Đọc các phần liên quan trong [quy tắc chung cho project Java](references/project-conventions.md), rồi đối chiếu với cấu hình và mã nguồn hiện tại trước khi áp dụng.
4. Theo cách tổ chức package, dependency injection, xử lý lỗi và persistence của module đang sửa. Áp dụng nguyên tắc và sở thích của người dùng trong phạm vi yêu cầu; không áp đặt kiến trúc hoặc công nghệ khác lên project.

## Chia package theo trách nhiệm

- Đặt code riêng của nghiệp vụ trong feature/domain tương ứng. Khi thêm module vào kiến trúc dạng domain, theo mẫu đang có: `domain.<feature>.controller`, `.service`, `.repository`, `.entity`, `.dto.request`, `.dto.response`; thêm `.mapper` nếu có nhu cầu mapping riêng. Chỉ tạo những package thật sự có code.
- Controller nhận/validate đầu vào và chuyển tiếp use case. Service xử lý nghiệp vụ và điều phối transaction. Repository chứa truy cập dữ liệu. DTO mô tả hợp đồng vào/ra; mapper chuyển đổi dữ liệu.
- Đặt implementation trong `service.impl` hoặc `repository.impl` khi module hiện tại sử dụng cách tổ chức đó. Không bắt mọi class phải có interface đi kèm.
- Code dùng chung giữa nhiều domain mới đưa vào package chung. Helper chỉ phục vụ một feature ở trong feature đó; tránh dồn nghiệp vụ vào `utils`, `common` hoặc một service quá lớn.
- Giữ chiều phụ thuộc rõ ràng: controller → service → repository/client. Khi nhiều domain phối hợp, dùng service điều phối hoặc hợp đồng hiện có; tránh phụ thuộc vòng và gọi controller từ tầng nghiệp vụ.
- Theo quy tắc đặt tên và bố trí hiện tại khi sửa code cũ. Không di chuyển hàng loạt file hoặc đổi package ngoài phạm vi yêu cầu.

## Áp dụng design pattern có mục đích

Ưu tiên pattern đã có trong luồng đang sửa. Chọn pattern khi có tình huống thực tế phù hợp, không cố đưa tất cả pattern vào một thay đổi.

| Pattern | Khi phù hợp | Cách giữ đơn giản |
| --- | --- | --- |
| Strategy | Cùng một thao tác có nhiều cách xử lý theo domain, loại giao dịch hoặc nhà cung cấp | Mỗi implementation có trách nhiệm rõ; giữ đúng điều kiện chọn strategy. |
| Factory / Registry | Cần chọn implementation từ các strategy/service đã đăng ký | Tái sử dụng dependency injection và registry hiện có; xử lý khóa không hợp lệ hoặc đăng ký trùng một cách rõ ràng. |
| Adapter | Cần chuyển hợp đồng của thư viện hoặc hệ thống bên ngoài sang hợp đồng nội bộ | Giới hạn chuyển đổi ở biên tích hợp; tránh để chi tiết bên ngoài lan vào nghiệp vụ. |
| Template Method | Nhiều luồng có thứ tự bước ổn định và chỉ khác một vài bước | Mở rộng hook có sẵn nếu phù hợp; chỉ tạo base class mới khi có phần dùng chung thực tế và quan hệ kế thừa hợp lý. |
| Builder | Khởi tạo đối tượng có nhiều trường tùy chọn khiến constructor khó đọc | Dùng builder đang có hoặc thư viện project đã sử dụng; constructor/factory đơn giản vẫn phù hợp với đối tượng ít trường. |

Với ít nhánh xử lý ổn định, một hàm rõ ràng hoặc điều kiện trực tiếp có thể đủ. Khi dùng pattern, có thể giải thích ngắn trong phần báo cáo thay đổi; không cần thêm comment vào code chỉ để nêu tên pattern.

## Triển khai trong phạm vi yêu cầu

- Dùng tên class, hàm và biến thể hiện ý nghĩa nghiệp vụ. Tách hàm theo trách nhiệm, dùng guard clause khi giúp giảm lồng điều kiện; chọn vòng lặp hoặc stream theo mức độ dễ đọc.
- Theo cách dependency injection của module; ưu tiên constructor injection cho code mới khi phù hợp. Tái sử dụng Lombok, mapper và helper nếu project đã có.
- Giữ hợp đồng API/JSON, mã lỗi, trạng thái HTTP, phân trang và hành vi null hiện tại, trừ khi yêu cầu thay đổi chúng. Tái sử dụng DTO, response wrapper, enum lỗi và exception handler của project.
- Với ghi dữ liệu, xác định persistence unit và transaction manager thực tế từ repository/entity/config. Tên package chưa đủ để xác định datasource. Không giả định transaction của một datasource sẽ rollback dữ liệu ở datasource khác.
- Giữ quy tắc quyền truy cập, người xử lý, trạng thái giao dịch, lịch sử và thông báo của use case đang sửa. Kiểm tra các điều kiện này trước khi ghi dữ liệu hoặc gọi tác vụ có tác dụng phụ.
- Giữ kiểu dữ liệu, đơn vị tiền, scale, quy tắc làm tròn và định dạng thời gian theo contract hiện tại. Không thay kiểu dữ liệu hàng loạt; tránh chuyển tiền sang số thực gây mất độ chính xác.
- Dùng parameter binding cho dữ liệu đầu vào trong truy vấn; không nối trực tiếp giá trị người dùng vào SQL. Giữ đồng nhất điều kiện lọc giữa truy vấn dữ liệu và truy vấn đếm.
- Log thông tin cần để theo dõi luồng và chẩn đoán lỗi; không log credential, token hoặc toàn bộ payload chứa dữ liệu nhạy cảm.

## Kiểm tra và bàn giao

- Xem diff và kiểm tra compile/build phù hợp với phần thay đổi bằng wrapper/công cụ đã có. Kiểm tra import, caller, mapping, branch nghiệp vụ và dependency injection liên quan.
- Nếu project dùng Maven wrapper, có thể kiểm tra production code bằng `./mvnw -DskipTests compile` hoặc PowerShell `./mvnw.cmd -DskipTests compile`. Với build system khác, chọn lệnh tương ứng từ cấu hình và wrapper hiện có; không sửa build chỉ để áp dụng lệnh mẫu.
- Có thể chạy test đã tồn tại nếu cần xác minh hoặc có yêu cầu của project; việc đó không cho phép tự tạo hoặc sửa test. Khi người dùng yêu cầu thêm test, chỉ thêm phạm vi test đã được yêu cầu.
- Nếu thiếu JDK, dependency nội bộ hoặc tài nguyên môi trường, nêu đúng nguyên nhân và phần chưa xác minh. Không tự nâng phiên bản hoặc thay thư viện nội bộ để làm build chạy qua.
- Báo cáo ngắn gọn thay đổi chính, cách đã kiểm tra và giới hạn còn lại. Không khẳng định đã kiểm tra thành công nếu chưa chạy hoặc lệnh thất bại.
