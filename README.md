# Hệ Thống Giám Sát Nhiệt Độ & Cảnh Báo Ngưỡng (ATmega16 + DHT11)

Dự án Đồ án 2 (ĐA2) - Đại học Bách Khoa Hà Nội (HUST).  
Ứng dụng vi điều khiển **ATmega16** thu thập dữ liệu nhiệt độ từ cảm biến **DHT11**, hiển thị trực quan lên màn hình **LCD 16x2** và kích hoạt cảnh báo thông qua dàn LED khi nhiệt độ vượt ngưỡng an toàn.

---

## 📌 Tính Năng Nổi Bật

- **Đọc dữ liệu chính xác từ DHT11**: Giao tiếp 1-Wire thời gian thực, kiểm tra mã bù lỗi (Checksum).
- **Hiển thị trực quan qua LCD 16x2**:
  - **Dòng 1**: Hiển thị nhiệt độ hiện tại kèm phần thập phân (`Temp: 28.5 °C`).
  - **Dòng 2**: Hiển thị ngưỡng cảnh báo (`HIGH Th: 30°C`).
  - Tự động hiển thị thông báo lỗi `DHT11: No Signal - Check Pin PA1` khi mất kết nối hoặc cảm biến lỗi.
- **Hệ thống cảnh báo tự động**:
  - Tự động so sánh nhiệt độ đo được với ngưỡng **High Threshold (30°C)**.
  - Khi $T \ge 30^\circ\text{C}$: Kích hoạt dấu cảnh báo `*!*` trên LCD và bật sáng 5 LED cảnh báo.
  - Khi $T < 30^\circ\text{C}$: Trạng thái bình thường, dàn LED tắt.
- **Tối ưu phần cứng**: Tắt JTAG để tái sử dụng PORT C điều khiển LCD 4-bit; hỗ trợ Makefile tự động hóa toàn bộ quy trình biên dịch và nạp firmware.

---

## 🛠️ Cấu Trúc Thư Mục

```text
├── .vscode/               # Cấu hình IntelliSense C/C++ cho VS Code
│   ├── c_cpp_properties.json
│   └── settings.json
├── ref/                   # Tài liệu kỹ thuật, sơ đồ kit và chân MCU
│   ├── atmega_sodo.png
│   └── So do mach Kit.docx
├── src/                   # Mã nguồn C và Makefile
│   ├── hunget_lcd.h       # Thư viện giao tiếp LCD 16x2 chế độ 4-bit (chuẩn Kit BK)
│   ├── tempsen.c          # Chương trình chính (DHT11, xử lý logic, LCD, LED)
│   └── Makefile           # Script build tự động với avr-gcc và avrdude
├── tools/                 # Công cụ phần mềm đi kèm
│   └── progisp/           # Trình nạp GUI ProgISP và driver USBasp
├── .gitignore             # Danh sách loại trừ file build, cache và tệp tạm
└── README.md              # Tài liệu hướng dẫn dự án
```

---

## 🔌 Sơ Đồ Đấu Nối Phần Cứng (Pinout)

### 1. Cảm biến DHT11
| Chân DHT11 | Chân ATmega16 | Chức năng / Ghi chú |
| :--- | :--- | :--- |
| **VCC** | 5V | Nguồn cấp 5V |
| **GND** | GND | Mass hệ thống |
| **DATA** | **PA1** (PORT A, Pin 1) | Giao tiếp 1-wire (cần trở kéo lên 4.7kΩ - 10kΩ nếu module chưa tích hợp) |

### 2. Màn hình LCD 16x2 (Chế độ 4-bit)
> [!IMPORTANT]
> Chương trình thực hiện tắt tính năng **JTAG** (`MCUCSR = (1 << JTD); MCUCSR = (1 << JTD);`) khi khởi động để giải phóng các chân **PC4 - PC7** làm GPIO xuất dữ liệu ra LCD.

| Chân LCD | Chân ATmega16 | Chức năng |
| :--- | :--- | :--- |
| **D4** | **PC4** | Bit dữ liệu 4 |
| **D5** | **PC5** | Bit dữ liệu 5 |
| **D6** | **PC6** | Bit dữ liệu 6 |
| **D7** | **PC7** | Bit dữ liệu 7 |
| **RS** (Chân 4) | **PD6** | Register Select (Lệnh: 0, Dữ liệu: 1) |
| **RW** (Chân 5) | **PD5** | Read/Write (Ghi: 0) |
| **EN** (Chân 6) | **PD7** | Chốt xung kích hoạt (Enable Strobe) |
| **VSS / VDD / VEE** | GND / 5V / Biến trở | Nguồn và chân chỉnh độ tương phản |

### 3. Dàn LED Cảnh Báo (Active LOW)
- **5 LED đơn**: Kết nối vào các chân **PD0, PD1, PD2, PD3, PD4**.
- Cơ chế kích hoạt:
  - Mức logic `0` (LOW): LED **SÁNG** (cảnh báo).
  - Mức logic `1` (HIGH): LED **TẮT** (bình thường).

---

## ⚙️ Cấu Hình Fuse Bits (Thạch anh ngoài 8MHz)

Dự án cấu hình sử dụng dao động thạch anh ngoài tần số **8.0 MHz**:
- **Low Fuse (LFUSE)**: `0xFF` (Ext. Crystal Osc. 8MHz, SUT1=1, SUT0=1)
- **High Fuse (HFUSE)**: `0xD9` (Bật nạp ISP qua SPI, giữ JTAG tắt theo firmware)

---

## 🚀 Hướng Dẫn Biên Dịch & Nạp Code

### Yêu cầu cài đặt
- Trình biên dịch **AVR-GCC** (kèm bộ công cụ `avr-binutils`).
- Trình nạp **AVRDUDE** hoặc phần mềm **ProgISP**.
- Tiện ích `make`.

---

### Cách 1: Sử dụng dòng lệnh (Makefile)

1. Di chuyển vào thư mục `src`:
   ```bash
   cd src
   ```

2. Biên dịch mã nguồn thành file `.hex`:
   ```bash
   make
   ```
   *(File thực thi `tempsen.elf` và file mã máy `tempsen.hex` sẽ được tự động tạo ra).*

3. Nạp firmware vào vi điều khiển bằng **USBasp**:
   ```bash
   make flash
   ```

4. Nạp Fuse bits (nếu vi điều khiển chưa cấu hình thạch anh ngoài 8MHz):
   ```bash
   make fuse
   ```

5. Dọn dẹp các file tạo ra sau khi build:
   ```bash
   make clean
   ```

---

### Cách 2: Nạp code bằng phần mềm ProgISP

1. Cắm mạch nạp USBasp vào máy tính (đảm bảo đã cài đặt driver trong thư mục `tools/progisp/win-driver`).
2. Mở file [tools/progisp/progisp.exe](file:///D:/Vibe/HUST/2026.1/DA2/tools/progisp/progisp.exe).
3. Tại ô **Select Chip**, chọn: `ATMEGA16`.
4. Nhấn **Load Flash** và trỏ đến file [src/tempsen.hex](file:///D:/Vibe/HUST/2026.1/DA2/src/tempsen.hex).
5. Tích chọn các mục cần nạp (như *Program Flash*, *Verify Flash*).
6. Nhấn nút **Auto** để bắt đầu nạp chương trình vào vi điều khiển.
