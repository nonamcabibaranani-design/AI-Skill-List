---
name: ducanh-code-rule
description: "Viết, sửa và refactor code Java theo cấu trúc project đang mở; ưu tiên tái sử dụng code hiện có, code đơn giản, dễ mở rộng, package đúng trách nhiệm và design pattern phù hợp. Dùng cho yêu cầu triển khai Java, không cố định phiên bản Java hay framework. Chỉ thêm test khi người dùng yêu cầu rõ ràng."
---

# Ducanh Code Rule

Skill này thay thế `java-code`. Khi cập nhật cấu hình hoặc hướng dẫn cho agent, dùng tên và đường dẫn `ducanh-code-rule`, gọi bằng `$ducanh-code-rule`.

Áp dụng khi triển khai, sửa lỗi hoặc refactor Java. Dùng các quy tắc chung theo yêu cầu, cấu hình và kiến trúc của project hiện tại; không mặc định phiên bản Java, framework hoặc mô hình nghiệp vụ.

## Yêu cầu của người dùng

- **Đề xuất trước khi thay đổi logic.** Trước khi thay đổi nghiệp vụ hoặc hành vi xử lý, phải trình bày vấn đề và bằng chứng, phương án sửa và phạm vi, ưu/nhược điểm, ảnh hưởng/rủi ro và cách kiểm chứng. Đặc biệt áp dụng cho async, transaction, locking, retry, chuyển trạng thái, validation và refactor làm thay đổi hành vi. Chờ người dùng chọn hoặc chấp thuận phương án rồi mới sửa code. Nếu người dùng đã chỉ rõ phương án/phạm vi hoặc đã chấp thuận chúng, thực hiện đúng phần đó và không hỏi lại cho cùng phương án.
- **Không tự mở rộng phạm vi sửa lỗi.** Yêu cầu rà soát, kiểm tra, sửa một lỗi hoặc "sửa code thôi" không tự động cho phép bổ sung logic, validation, thay đổi kiến trúc hay cơ chế thực thi ngoài lỗi đã chỉ định. Phân biệt nguyên nhân đã kiểm chứng với rủi ro chỉ suy luận từ code; nêu các đề xuất bổ sung riêng để người dùng quyết định, không dùng rủi ro giả định làm lý do tự thay đổi luồng đang chạy.
- **Giữ bản sửa đúng phạm vi đã chốt.** Khi sửa trường dữ liệu hoặc mapping đã xác định, giữ các cơ chế async/transaction và workflow hiện tại trừ khi người dùng chấp thuận thay đổi chúng. Tái sử dụng hook và cấu trúc hiện có, không tự thêm tầng kiểm tra hoặc lớp điều phối. Đọc code, phân tích, kiểm tra build và dọn import không thay đổi hành vi có thể thực hiện trực tiếp.

- **Chỉ tạo file test hoặc bổ sung test khi người dùng yêu cầu rõ ràng.** Yêu cầu code, sửa bug, refactor, kiểm tra hay build không tự động cho phép thêm test. Không tự sinh test class, test fixture hoặc thêm dependency phục vụ test. Giữ nguyên các test đang có, trừ khi người dùng yêu cầu chỉnh sửa chúng.
- **Không gắn skill với phiên bản cụ thể.** Xác định Java, framework, dependency, namespace và build tool từ project đang mở. Dùng cú pháp/API tương thích với cấu hình đó; chỉ nâng cấp khi nằm trong yêu cầu của người dùng.
- **Ưu tiên code đơn giản, dễ đọc và đúng nghiệp vụ.** Chọn cách triển khai nhỏ nhất đáp ứng đầy đủ yêu cầu. Không thêm lớp trung gian, interface, generic framework hoặc dependency để phục vụ nhu cầu giả định.
- **Luôn code để dễ mở rộng về sau.** Trong phạm vi đã chốt, tổ chức code để có thể bổ sung nghiệp vụ, loại xử lý hoặc tích hợp mới bằng thay đổi cục bộ, hạn chế sửa luồng dùng chung. Đây là tiêu chí thiết kế cho phần đang làm, không phải cho phép triển khai trước tính năng tương lai hoặc tự thay đổi kiến trúc.
- **Trước khi tạo hàm dùng chung mới, phải rà code có thể tái sử dụng.** Tìm hàm, helper, service và hook tương đương trong module đang sửa và các module dùng chung liên quan; đọc implementation và caller để đối chiếu contract, hành vi null và tác dụng phụ. Ưu tiên gọi lại hoặc mở rộng code hiện có khi phù hợp và không làm sai hành vi của caller hiện tại. Chỉ tạo hàm dùng chung mới khi code hiện có không đáp ứng hợp lý; nêu ngắn phần khác biệt trong báo cáo thay đổi, không sao chép logic rồi chỉ đổi tên. Áp dụng cùng bước rà soát trước khi thêm class, DTO, subclass, converter hoặc wrapper; không tạo cấu trúc mới chỉ để tách luồng hoặc chuyển đổi dữ liệu không cần thiết. Nếu việc mở rộng làm thay đổi logic, tuân thủ quy tắc đề xuất và chấp thuận ở trên.
- **DTO dùng chung có thể có trường không áp dụng cho một luồng.** Tiếp tục dùng DTO chung và bỏ qua trường đó trong xử lý của luồng tương ứng nếu vẫn đáp ứng nghiệp vụ. Không tạo DTO/subclass riêng chỉ để ẩn hoặc bỏ một trường, không làm thay đổi các luồng vẫn sử dụng trường đó. Nếu API hiện tại đã trả trực tiếp được giá trị đúng kiểu người dùng yêu cầu, dùng luôn cấu trúc hiện có.
- **Chỉ comment khi cần thiết.** Comment giải thích lý do, quy tắc nghiệp vụ khó suy ra, giới hạn tích hợp hoặc quyết định có chủ đích. Ưu tiên tên rõ nghĩa và tách hàm hợp lý. Không comment diễn giải lại từng dòng, thêm thông tin tác giả/ngày tạo, sinh Javadoc hình thức hay giữ code đã comment out.

## Chọn cách triển khai gọn trước khi viết code

- Trước khi sửa, rà luồng dữ liệu, caller và code có sẵn; chọn cách ít bước, ít truy vấn và ít chuyển đổi trung gian nhất mà vẫn đúng nghiệp vụ, dễ đọc và dễ debug. Không viết cách vòng vèo trước rồi mới tính chuyện tối ưu.
- Với thông tin có thể lấy hợp lý ngay trong SQL hiện tại, ưu tiên projection, JOIN hoặc EXISTS tại repository; tránh query thêm rồi gom Map/List và đối chiếu lại bằng Java. Kiểm tra tính duy nhất của khóa, null, phân trang, count và chi phí truy vấn trước khi chọn; không mặc định đẩy mọi nghiệp vụ xuống SQL.
- Chỉ thêm class, hàm con, wrapper, collection hoặc bước mapping khi có trách nhiệm hay lợi ích rõ ràng. Không tách vụn luồng hoặc thêm cấu trúc trung gian chỉ để phục vụ cách triển khai do mình tạo ra; tận dụng DTO và trường dữ liệu đã có.
- Ngắn gọn phải đi cùng dễ hiểu: không nén thành stream, ternary lồng nhau hoặc SQL khó đọc để giảm số dòng. Đưa điều kiện bất biến ra ngoài vòng lặp và bỏ bước xử lý lặp, chuyển đổi qua lại, biến trung gian không cần thiết.
- Trước khi bàn giao, tự rà từng phần mới: có thể dùng code hiện có, tính trực tiếp ở nơi đã có dữ liệu hoặc bỏ hẳn bước nào không? Giữ nguyên hợp đồng API và điều kiện nghiệp vụ khi rút gọn; không tuyên bố nhanh hơn nếu chưa đo.
## Đọc ngữ cảnh trước khi sửa

1. Đọc hướng dẫn áp dụng cho repository, trạng thái thay đổi hiện tại và file build liên quan (`pom.xml`, cấu hình Gradle hoặc tương đương).
2. Xác định domain/use case cần sửa; lần theo một luồng tương tự từ đầu vào đến service, repository và dữ liệu trả về. Đọc thêm các caller khi thay đổi contract dùng chung.
3. Đọc các phần liên quan trong [quy tắc chung cho project Java](references/project-conventions.md), rồi đối chiếu với cấu hình và mã nguồn hiện tại trước khi áp dụng.
4. Theo cách tổ chức package, dependency injection, xử lý lỗi và persistence của module đang sửa. Áp dụng nguyên tắc và sở thích của người dùng trong phạm vi yêu cầu; không áp đặt kiến trúc hoặc công nghệ khác lên project.
5. Xác định phần xử lý ổn định và phần có thể thay đổi theo từng nghiệp vụ; tìm điểm mở rộng hiện có trước khi chọn cách triển khai. Nếu cần đổi kiến trúc hoặc contract để mở rộng, đề xuất và chờ chấp thuận theo quy tắc ở trên.

## Chia package theo trách nhiệm

- Đặt code riêng của nghiệp vụ trong feature/domain tương ứng. Khi thêm module vào kiến trúc dạng domain, theo mẫu đang có: `domain.<feature>.controller`, `.service`, `.repository`, `.entity`, `.dto.request`, `.dto.response`; thêm `.mapper` nếu có nhu cầu mapping riêng. Chỉ tạo những package thật sự có code.
- Controller nhận/validate đầu vào và chuyển tiếp use case. Service xử lý nghiệp vụ và điều phối transaction. Repository chứa truy cập dữ liệu. DTO mô tả hợp đồng vào/ra; mapper chuyển đổi dữ liệu.
- Đặt implementation trong `service.impl` hoặc `repository.impl` khi module hiện tại sử dụng cách tổ chức đó. Không bắt mọi class phải có interface đi kèm.
- Code dùng chung giữa nhiều domain mới đưa vào package chung. Helper chỉ phục vụ một feature ở trong feature đó; tránh dồn nghiệp vụ vào `utils`, `common` hoặc một service quá lớn.
- Giữ chiều phụ thuộc rõ ràng: controller → service → repository/client. Khi nhiều domain phối hợp, dùng service điều phối hoặc hợp đồng hiện có; tránh phụ thuộc vòng và gọi controller từ tầng nghiệp vụ.
- Theo quy tắc đặt tên và bố trí hiện tại khi sửa code cũ. Không di chuyển hàng loạt file hoặc đổi package ngoài phạm vi yêu cầu.

## Tái sử dụng code và quản lý constants

- Trước khi viết logic mới, tìm và tái sử dụng hàm, class hoặc constants phù hợp đã có. Với xử lý cần dùng ở nhiều nơi như chuyển đổi ngày giờ, đưa phần chung vào một hàm hoặc class đúng trách nhiệm (ví dụ DateUtils), nhận tham số cần thiết thay vì copy code giữa các service.
- Tập trung các hằng số dùng lại như đường dẫn API, định dạng ngày giờ và mã quy ước vào class constants hoặc class sở hữu chúng theo cấu trúc project; không rải literal ở nhiều nơi. Tái sử dụng hằng hiện có. Giá trị thay đổi theo môi trường vẫn lấy từ cấu hình.
- Giữ helper dùng chung độc lập với nghiệp vụ của một luồng. Ví dụ, DateUtils chỉ chuyển đổi ngày giờ; service quyết định giới hạn thời hạn và thông báo lỗi nghiệp vụ. Code chỉ thuộc một feature đặt trong feature đó; chỉ đưa vào package chung khi nhiều nơi thực sự dùng.
- Chọn hàm hoặc class nhỏ, tham số rõ ràng và cách gọi đơn giản. Chỉ tách phần có thể tái sử dụng thực tế; không thêm interface, base class hoặc framework chỉ để dự phòng.

## Thiết kế để dễ mở rộng

- Tách phần dùng chung khỏi quy tắc đặc thù tại đúng ranh giới trách nhiệm; không trộn điều phối, lựa chọn biến thể và chi tiết xử lý vào một hàm lớn. Giữ API, DTO và hành vi hiện tại khi yêu cầu không thay đổi chúng.
- Ưu tiên hook, strategy, registry hoặc cơ chế dependency injection đã có để thêm cách xử lý mới. Tránh rải cùng điều kiện theo loại, mã nghiệp vụ hoặc nhà cung cấp ở nhiều nơi khiến mỗi lần mở rộng phải sửa đồng loạt.
- Đặt cấu hình và quy tắc thay đổi tại nơi sở hữu rõ ràng, thay vì hard-code phân tán. Chỉ tách interface, implementation hoặc lớp trừu tượng mới khi có biến thể thực tế hoặc nhu cầu mở rộng đã được xác nhận; vài nhánh ổn định vẫn có thể dùng hàm và điều kiện trực tiếp.
- Trước khi bàn giao, rà xem thêm một trường hợp tương tự sẽ phải sửa những chỗ nào và liệu có làm ảnh hưởng các luồng hiện có. Nếu cách triển khai buộc sửa nhiều phần không liên quan, thu hẹp điểm thay đổi trong phạm vi được phép; không tự viết thêm trường hợp tương lai để minh họa.

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
- **Luôn log dữ liệu request và response khi gọi ra ngoài.** Với mỗi lời gọi external API hoặc hệ thống bên ngoài trong phần code đang triển khai/chỉnh sửa, log payload request trước khi gửi và payload response sau khi nhận; không chỉ log thông báo bắt đầu/kết thúc. Kèm endpoint/hệ thống đích, trạng thái phản hồi và requestId/correlationId hiện có để đối chiếu. Khi timeout hoặc lỗi không nhận được response, log lỗi tương ứng cùng thông tin nhận diện request. Che hoặc loại bỏ credential, token, mật khẩu và các trường nhạy cảm trước khi ghi log; vẫn log các trường nghiệp vụ còn lại. Tái sử dụng cơ chế logging/masking chung của project, tránh log trùng ở nhiều tầng.

## Kiểm tra và bàn giao

- Xem diff và kiểm tra compile/build phù hợp với phần thay đổi bằng wrapper/công cụ đã có. Kiểm tra import, caller, mapping, branch nghiệp vụ và dependency injection liên quan.
- Nếu project dùng Maven wrapper, có thể kiểm tra production code bằng `./mvnw -DskipTests compile` hoặc PowerShell `./mvnw.cmd -DskipTests compile`. Với build system khác, chọn lệnh tương ứng từ cấu hình và wrapper hiện có; không sửa build chỉ để áp dụng lệnh mẫu.
- Có thể chạy test đã tồn tại nếu cần xác minh hoặc có yêu cầu của project; việc đó không cho phép tự tạo hoặc sửa test. Khi người dùng yêu cầu thêm test, chỉ thêm phạm vi test đã được yêu cầu.
- Nếu thiếu JDK, dependency nội bộ hoặc tài nguyên môi trường, nêu đúng nguyên nhân và phần chưa xác minh. Không tự nâng phiên bản hoặc thay thư viện nội bộ để làm build chạy qua.
- Báo cáo ngắn gọn thay đổi chính, cách đã kiểm tra và giới hạn còn lại. Không khẳng định đã kiểm tra thành công nếu chưa chạy hoặc lệnh thất bại.
