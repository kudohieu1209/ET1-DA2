# Hướng dẫn hoàn thiện Chương 3

Đây là kế hoạch thu thập minh chứng, chưa phải kết quả thực nghiệm. Chỉ đưa số liệu đã đo vào báo cáo; các số lần thử dưới đây là đề xuất. Hình 3.1 đang được giữ nguyên theo yêu cầu.

## 1. Chuẩn bị và ghi điều kiện thử

- Kit ATmega16, module DHT11 3 chân (mã bán hàng LK_02463), LCD 1602 và 5 LED.
- Một nhiệt kế tham chiếu: ghi model, độ phân giải và sai số theo tài liệu của thiết bị. Nếu không có chứng nhận hiệu chuẩn, gọi là thiết bị tham chiếu hoặc phép đối chiếu; không kết luận đã hiệu chuẩn hệ thống.
- Đặt đầu đo DHT11 và nhiệt kế gần nhau, cùng môi trường, tránh gần LM7805, MCU hoặc nguồn nhiệt của bo mạch. Ghi khoảng cách và cách bố trí. Không để cảm biến tiếp xúc trực tiếp nước hoặc hơi gây ngưng tụ.
- Ghi ngày, phòng, nguồn cấp, phiên bản firmware, fuse đọc lại từ kit, chiều dài dây DATA, giá trị điện trở kéo lên nếu xác định được.
- Thử tại mỗi mức sau khi số đo hai thiết bị đã ổn định. Chụp ảnh toàn bộ bố trí để chứng minh hai thiết bị được đối chiếu cùng điều kiện.

Mã bán hàng LK_02463 và hình thức module 3 chân không xác định được phiên bản chip. Chưa suy ra độ phân giải 0,1°C chỉ vì LCD có phần thập phân.

## 2. Làm các phép thử theo thứ tự

| Phép thử | Cách thực hiện đề xuất | Dữ liệu cần ghi |
| --- | --- | --- |
| Khởi động | Cấp nguồn lại 5 lần | LCD chào, trạng thái LED, có vào vòng đo được không |
| Đối chiếu nhiệt độ | Chọn ít nhất 3 mức trong dải làm việc: dưới 30°C, quanh 30°C, trên 30°C. Thu 30 cặp số đo ở mỗi mức sau khi ổn định | Thời điểm, nhiệt kế tham chiếu, LCD, trạng thái LED |
| Kiểm tra điều kiện ngưỡng | Quan sát các lần dữ liệu nhận được dưới 30, bằng 30 và trên 30. Lặp quá trình tăng/giảm ít nhất 5 lượt | Giá trị nhận được khi LED bật và tắt; hiện tượng đổi trạng thái quanh ngưỡng |
| Mất và nối lại cảm biến | Thử rút dây DATA khi đang bình thường, rồi khi đang cảnh báo; nối lại và quan sát. Mỗi tình huống 5 lượt | Thông báo LCD, LED tắt khi lỗi, số chu kỳ để phục hồi |
| Chạy liên tục | Chạy ít nhất 30 phút trong điều kiện ghi rõ | Thời lượng thực, tổng lượt đọc, lượt hợp lệ, timeout, checksum; reset hoặc treo nếu có |
| Độ trễ phần mềm | Nếu có logic analyzer, đo mốc bắt đầu đọc và mốc đổi trạng thái LED | Chu kỳ thực, thời gian xử lý; tên thiết bị và phương pháp |

Không thể coi việc nhiệt kế tham chiếu chỉ đúng 30°C là bằng chứng code đã xử lý mẫu DHT11 bằng 30°C, vì hai thiết bị có sai lệch. Để kiểm tra phép so sánh chính xác, phải ghi giá trị nhận được của DHT11. Nếu module không tạo được một giá trị mong muốn, ghi rõ chưa thử được hoặc dùng phép thử mô phỏng có đánh dấu riêng.

Không thay đổi ngưỡng hoặc thêm hysteresis trước khi hoàn tất đối chiếu firmware hiện tại; nếu có thay đổi thì ghi lại phiên bản và thử lại.

## 3. Bảng ghi số liệu đối chiếu

Mỗi hàng là một cặp số đo tại cùng thời điểm. Các ô trống dưới đây dành cho số đo thật.

| Lượt | Thời gian | Mức thử | T tham chiếu (°C) | Giá trị LCD (°C) | Sai lệch LCD - tham chiếu (°C) | LED | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |

Với N cặp hợp lệ, tính:

- Sai lệch từng cặp: e_i = T_LCD,i - T_ref,i.
- Sai lệch trung bình có dấu: mean(e_i), giúp nhận ra xu hướng cao hoặc thấp hơn thiết bị tham chiếu.
- Sai lệch tuyệt đối trung bình: MAE = sum(abs(e_i)) / N.
- Sai lệch tuyệt đối lớn nhất: max(abs(e_i)).

Không gọi MAE là độ chính xác tuyệt đối của cảm biến. Kết quả còn chịu ảnh hưởng sai số nhiệt kế, vị trí đặt và việc hai thiết bị đáp ứng nhiệt với tốc độ khác nhau. Số liệu sai số ±2°C của datasheet là thông số danh định, không phải kết quả nhóm đã đo.

## 4. Ghi log 5 byte để kiểm tra phần thập phân

Cần lưu đủ `data[0]` đến `data[4]`, mã trạng thái và thời điểm. Dữ liệu này có trong hàm `DHT11_Read`; firmware hiện tại chưa xuất log ra máy tính. Khi bổ sung chức năng log, chỉ xuất sau khi nhận xong gói tin để không làm sai thời gian lấy mẫu xung DHT11.

| Thời gian | RH nguyên | RH lẻ | T nguyên | T lẻ | Checksum nhận | Tổng 4 byte & 0xFF | Status | LCD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

USART phần cứng dùng PD0/RXD và PD1/TXD, đang được dùng cho LED cảnh báo. Nếu chọn log qua UART, cần bố trí lại hoặc ngắt tải LED liên quan và kiểm tra mức điện áp adapter. Không nối thêm UART rồi coi cấu hình này tương đương nguyên trạng 5 LED. Có thể dùng một bản firmware đo kiểm riêng, nhưng phải mô tả sự khác biệt trong phương pháp thử.

Nếu nhiều gói checksum hợp lệ có byte T lẻ khác 0, đối chiếu cách mã hóa với tài liệu đúng phiên bản chip trước khi diễn giải. Không sửa ảnh hoặc làm tròn số liệu cũ để khớp giả định của datasheet.

## 5. Phân biệt kiểm tra checksum và kiểm tra chịu nhiễu

Hiện báo cáo chỉ phân tích nhánh `status == -6`. Không có thiết bị gây nhiễu vẫn có thể kiểm tra nhánh này bằng bản firmware kiểm thử: đưa một gói giả định hợp lệ vào bước kiểm tra tổng, rồi thay đúng một byte để tạo checksum sai. Ghi rõ đó là phép thử dữ liệu mô phỏng; không gọi là đo khả năng chống nhiễu của đường truyền.

Nếu chưa làm phép thử đó, giữ mô tả hiện tại là phân tích mã nguồn. Không ghi số lượt đạt cho trường hợp này.

## 6. Thống kê chạy liên tục và đo độ trễ

| Bắt đầu | Kết thúc | Thời lượng | Tổng lần đọc | Thành công | Timeout | Checksum lỗi | Reset/treo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

Tỷ lệ đọc thành công = số lần `status == 0` / tổng số lần đọc × 100%. Tổng lượt thành công, timeout và checksum phải bằng tổng số lần đọc. Không tính lượt rút dây chủ động vào tỷ lệ lỗi trong điều kiện vận hành bình thường; báo riêng các lượt đó.

Nếu chỉ quay video, ghi tốc độ khung hình và coi thời gian rút DATA đến thông báo lỗi là độ trễ quan sát được. Không dùng video LCD để khẳng định độ chính xác từng micro giây. Độ trễ phản ứng với nhiệt bao gồm đáp ứng nhiệt của cảm biến, pha lấy mẫu và thời gian xử lý; cần phân biệt với độ trễ phần mềm sau khi đã nhận một mẫu đạt ngưỡng.

## 7. Đưa kết quả vào báo cáo

1. Đầu mục 3.1: thêm điều kiện, thiết bị, sơ đồ bố trí, cách tạo các mức nhiệt và số lần lặp.
2. Giữ các trạng thái chức năng hiện có. Bổ sung kết quả đúng ngưỡng, nối lại cảm biến và nguồn minh chứng cho mỗi trường hợp.
3. Sau bảng tổng hợp chức năng: thêm bảng đối chiếu nhiệt độ, bảng thống kê chạy liên tục và bảng độ trễ nếu đã đo. Đánh số bảng tự động bằng LaTeX.
4. Mục 3.2: thay các giới hạn đã có dữ liệu bằng nhận xét định lượng, ghi N, thời lượng và điều kiện. Chỉ bỏ giới hạn nào đã thực sự giải quyết.
5. Chương 4: cập nhật kết luận tương ứng với bằng chứng mới. Chỉ kết luận trong phạm vi điều kiện đã thử.

Mẫu câu để điền sau khi đo:

> Trong [thời lượng thực] ở [điều kiện], hệ thống thực hiện [N] lần đọc, gồm [n_ok] lần hợp lệ, [n_timeout] lỗi timeout và [n_sum] lỗi checksum. Tỷ lệ đọc thành công là [giá trị]%. Trên [N cặp] số đo đối chiếu với [model nhiệt kế], sai lệch tuyệt đối trung bình là [MAE]°C và sai lệch tuyệt đối lớn nhất là [E_max]°C. Kết quả phản ánh điều kiện thử này; chưa đại diện cho mọi môi trường vận hành.

Các nội dung trong ngoặc vuông chỉ là hướng dẫn điền, không đưa nguyên trạng vào PDF nộp.
