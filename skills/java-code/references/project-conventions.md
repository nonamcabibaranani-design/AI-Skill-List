# Quy ước tham khảo từ payment-merchant-management

Chỉ đọc các phần liên quan khi làm việc với project này. Mã nguồn hiện tại là nguồn xác nhận cuối cùng; các ví dụ dưới đây không phải cấu trúc bắt buộc cho mọi project Java và không cố định phiên bản công nghệ.

Các đường dẫn Java bên dưới tính từ `src/main/java/com/epayjsc/merchantmanagement/` của repository gốc.

## Cấu trúc và luồng nghiệp vụ

- Các domain chính: `domain/payment_core`, `domain/qr_gateway`, `domain/bill_service_hub`. Có cả controller, service, DTO và mapper dùng chung ở package gốc. Đặt thay đổi gần nghiệp vụ sở hữu nó và theo vị trí của các lớp liên quan đang có.
- Luồng đơn giản để tham khảo: `domain/bill_service_hub/controller/BshTransactionController.java` → `domain/bill_service_hub/service/BshTransactionService.java` → `domain/bill_service_hub/service/impl/BshTransactionServiceImpl.java`. Controller dùng constructor injection và chuyển xử lý sang service.
- Luồng xử lý QR: `domain/qr_gateway/controller/QrProcessTransactionController.java` dùng service được chọn bằng qualifier; `domain/qr_gateway/service/processTransaction/QrProcessTransactionServiceImpl.java` mở rộng các hook của service xử lý chung. Kiểm tra implementation và bean name khi thêm hoặc thay service.
- Repository tùy biến triển khai ở package `repository/impl`. Ví dụ `domain/qr_gateway/repository/impl/QrProcessTransactionCustomRepoImpl.java` đọc truy vấn dữ liệu/truy vấn đếm, bind parameter và trả kết quả phân trang. Theo đường dẫn resource trong code để tìm SQL liên quan.

## Pattern đang có

- `service/process_transaction/IProcessTransactionStrategy.java`: hợp đồng của strategy, gồm điều kiện hỗ trợ và các nhánh xử lý payment/refund.
- `service/process_transaction/ProcessTransactionStrategyFactory.java`: nhận danh sách strategy qua constructor injection. Chọn theo `serviceCode`, `type` và ở overload liên quan có thêm `proxyTransactionType`. Kết quả phải khớp đúng một strategy; không khớp hoặc khớp nhiều đều là lỗi. Giữ nguyên ý nghĩa hai overload khi sửa luồng chọn.
- `service/process_transaction/ProcessTransPlanRegistry.java`: đăng ký service theo `serviceCode`. Luồng hiện tại có fallback khi service code thiếu và báo lỗi khi không tìm được domain hỗ trợ. Chỉ thay fallback khi nghiệp vụ yêu cầu.
- Các strategy của từng domain ở `domain/<domain>/service/processTransaction/`. Khi thêm một cách xử lý thật sự mới vào luồng này, cân nhắc mở rộng strategy hiện có thay vì bổ sung nhiều điều kiện ở controller.
- Các hook của service xử lý chung là ví dụ Template Method. Chỉ mở rộng base class khi thao tác mới vẫn phù hợp hợp đồng và thứ tự xử lý của nó.

## Persistence và transaction

| Domain cấu hình | Persistence unit | Transaction manager |
| --- | --- | --- |
| Payment core | `paymentCore` | `merchantManagementPlatformTransactionManager` |
| QR gateway | `qrGateway` | `qrGatewayPlatformTransactionManager` |
| Bill service hub | `billServiceHub` | `billServiceHubPlatformTransactionManager` |

Kiểm tra lại `config/datasource/PaymentCoreDBConfig.java`, `QrGatewayDBConfig.java` và `BillServiceHubDBConfig.java` khi thay đổi persistence. Payment core được cấu hình primary; điều đó không có nghĩa mọi thao tác ghi đều thuộc payment core.

`domain/qr_gateway/repository/impl/QrProcessTransactionCustomRepoImpl.java` dùng `@PersistenceContext(unitName = "paymentCore")`. Đây là ví dụ cho thấy package QR và nơi lưu dữ liệu có thể khác nhau. Lần theo repository và entity trước khi chọn transaction manager cho use case.

`domain/bill_service_hub/repository/BaseBshCustomRepository.java` chứa cách bind parameter và tính phân trang theo request của module. Đọc cả cặp truy vấn dữ liệu/đếm khi sửa bộ lọc; giữ quy ước page number của contract hiện tại.

## DTO, response, exception và mapping

- Project sử dụng `Ret`, `Rets` từ thư viện nội bộ `com.epayjsc.lib`. Tái sử dụng cách trả kết quả của luồng đang sửa thay vì thêm response envelope mới.
- `common/SearchResult.java` có `data` và `totalData`; giữ hợp đồng đếm tổng khi sửa tìm kiếm/phân trang.
- `exception/BusinessException.java`, `ExceptionEnum.java` và `GlobalExceptionHandler.java` là điểm kiểm tra mã lỗi. Handler hiện tại trả response nghiệp vụ/bean validation với HTTP OK, còn lỗi upload quá dung lượng có trạng thái riêng. Không thay trạng thái HTTP như một phần phụ của refactor.
- DTO có cả dạng dùng chung ở `dto/` và dạng nằm trong domain. Ví dụ `dto/processTrans/ProcessTransCreateReq.java` chứa các trường phân biệt loại giao dịch và thông tin đối soát. Theo caller và JSON contract khi thay trường.
- `mapper/MapperStruct.java`, `CollectionTransMapper.java` và `DisbursementTransMapper.java` sử dụng MapStruct với component model của Spring. Sửa interface mapper và annotation, không sửa file implementation được sinh ra trong thư mục build.
- Đọc `pom.xml` để xác định dependency, annotation processor và mức tương thích hiện tại. Với namespace persistence/validation/servlet, theo cấu hình và import đang dùng trong module; không tự thực hiện migration namespace.

## Hợp đồng dữ liệu và xử lý giao dịch

- `domain/payment_core/entity/TransPayment.java` có các trường tiền/fee dạng `Long`; `domain/bill_service_hub/entity/TransPaymentEntity.java` sử dụng `BigDecimal`. Giữ đơn vị và quy tắc của từng trường; không áp một kiểu dữ liệu chung cho mọi domain.
- Entity có thể dùng `Date`, còn DTO tìm kiếm nhận chuỗi thời gian và repository chuyển đổi theo format hiện có. Kiểm tra format, timezone và ranh giới lọc ở use case liên quan trước khi sửa.
- `utils/SecurityUtils.java` lấy thông tin người dùng từ security context. Luồng phê duyệt trong service xử lý chung kiểm tra trạng thái được phép và người phê duyệt trước khi ghi dữ liệu, đồng thời cập nhật lịch sử/thông báo. Giữ đủ các bước nghiệp vụ có liên quan.
- Dùng những ví dụ trên để tìm code đúng vị trí, không sao chép nguyên phương thức lớn, comment thừa hoặc logging payload vào phần mới.

## Kiểm tra production code

Repository có Maven wrapper. Dùng compile phù hợp khi thay Java; dependency nội bộ `com.epayjsc:epay-lib` có thể cần repository hoặc cache đã được cấu hình trong môi trường. Không thay dependency này bằng thư viện khác chỉ để compile thành công.

Quy tắc của người dùng vẫn áp dụng: chỉ thêm file test hoặc bổ sung test khi được yêu cầu rõ ràng. Đọc lại quy tắc đầy đủ ở `../SKILL.md` trước khi thực hiện bước kiểm tra.
