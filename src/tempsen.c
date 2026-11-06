#define F_CPU 8000000UL
#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#include "hunget_lcd.h" // Thư viện điều khiển LCD 16x2 chế độ 4 bit

// =======================================================
// CẤU HÌNH CHÂN DHT11 NỐI VÀO CHÂN PA1 TRÊN PORT A
// =======================================================
#define DHT_DDR   DDRA
#define DHT_PORT  PORTA
#define DHT_PIN_R PINA
#define DHT_BIT   PA1

// Hàm đọc dữ liệu từ cảm biến số DHT11
// Trả về 0 nếu thành công, < 0 nếu lỗi/timeout
int8_t DHT11_Read(uint8_t *temp_int, uint8_t *temp_dec, uint8_t *humi_int) {
    uint8_t data[5] = {0, 0, 0, 0, 0};
    uint16_t timeout;

    // 1. MCU gửi tín hiệu Start (kéo LOW tối thiểu 18ms)
    DHT_DDR |= (1 << DHT_BIT);     // Set PA1 là Output
    DHT_PORT &= ~(1 << DHT_BIT);   // Kéo xuống LOW
    _delay_ms(20);                 // Giữ mức LOW 20ms

    // 2. Nhả bus sang Input và kích hoạt trở kéo lên để chờ DHT11 phản hồi (tránh xung đột bus)
    DHT_DDR &= ~(1 << DHT_BIT);    // Chuyển PA1 thành Input
    DHT_PORT |= (1 << DHT_BIT);    // Bật điện trở kéo lên nội
    _delay_us(30);                 // Chờ 20-40us cho DHT11 bắt đầu phản hồi

    // Đợi DHT11 kéo LOW (khoảng 20-40µs)
    timeout = 10000;
    while (DHT_PIN_R & (1 << DHT_BIT)) {
        if (--timeout == 0) return -1; // Timeout chờ DHT11 phản hồi
    }

    // Đợi DHT11 kéo HIGH (khoảng 80µs)
    timeout = 10000;
    while (!(DHT_PIN_R & (1 << DHT_BIT))) {
        if (--timeout == 0) return -2;
    }

    // Đợi DHT11 kéo LOW chuẩn bị truyền bit đầu tiên (khoảng 80µs)
    timeout = 10000;
    while (DHT_PIN_R & (1 << DHT_BIT)) {
        if (--timeout == 0) return -3;
    }

    // 3. Đọc 40 bit (5 byte: Humi_int, Humi_dec, Temp_int, Temp_dec, Checksum)
    for (uint8_t i = 0; i < 5; i++) {
        for (int8_t j = 7; j >= 0; j--) {
            // Đợi hết xung LOW 50µs của từng bit
            timeout = 10000;
            while (!(DHT_PIN_R & (1 << DHT_BIT))) {
                if (--timeout == 0) return -4;
            }

            // Đo độ rộng xung HIGH:
            // 26-28µs -> bit 0
            // 70µs    -> bit 1
            // Chờ 38µs rồi đọc trạng thái chân
            _delay_us(38);
            if (DHT_PIN_R & (1 << DHT_BIT)) {
                data[i] |= (1 << j);
                // Đợi xung HIGH kết thúc
                timeout = 10000;
                while (DHT_PIN_R & (1 << DHT_BIT)) {
                    if (--timeout == 0) return -5;
                }
            }
        }
    }

    // 4. Kiểm tra mã kiểm tra lỗi (Checksum 8-bit)
    if ((uint8_t)(data[0] + data[1] + data[2] + data[3]) != data[4]) {
        return -6; // Sai checksum
    }

    *humi_int  = data[0];
    *temp_int  = data[2];
    *temp_dec  = data[3];
    return 0; // Đọc thành công
}

int main(void) {
    // 1. TẮT JTAG (BẮT BUỘC để giải phóng PORT C điều khiển LCD)
    MCUCSR = (1 << JTD);
    MCUCSR = (1 << JTD);

    // 2. KHỞI TẠO LCD
    LCD4_INIT(0, 0);

    // 3. KHỞI TẠO DÃY LED CẢNH BÁO (PD0 - PD4)
    // PD5-PD7 là Output cho LCD (đã set trong thư viện LCD)
    // Set thêm PD0-PD4 là Output cho LED
    DDRD |= 0x1F;  // Set 5 chân thấp là Output
    PORTD |= 0x1F; // Xuất mức 1 để TẮT hết LED ban đầu (Active Low)

    // --- MÀN HÌNH CHÀO MỪNG ---
    LCD4_CUR_GOTO(1, 0);
    LCD4_OUT_STR("DA2: DO NHIET DO");
    LCD4_CUR_GOTO(2, 2);
    LCD4_OUT_STR("DHT11 SENSOR");
    _delay_ms(1500);
    LCD4_OUT_CMD(0x01); // Xóa màn hình
    _delay_ms(2);

    char buffer[32];
    uint8_t temp_int = 0;
    uint8_t temp_dec = 0;
    uint8_t humi_int = 0;

    while (1) {
        int8_t status = DHT11_Read(&temp_int, &temp_dec, &humi_int);

        if (status == 0) {
            // --- ĐỌC THÀNH CÔNG TỪ DHT11 ---
            // Dòng 1: "Temp: 31.5 °C   " (đúng 16 ký tự chuẩn)
            LCD4_CUR_GOTO(1, 0);
            sprintf(buffer, "Temp: %u.%u \xDF""C   ", temp_int, temp_dec);
            LCD4_OUT_STR(buffer);

            // Dòng 2: Hiển thị ngưỡng cảnh báo "HIGH Th: 30°C"
            LCD4_CUR_GOTO(2, 0);
            if (temp_int >= 30) {
                // Nhiệt độ vượt ngưỡng 30 độ C: Báo WARNING và BẬT LED (đúng 16 ký tự)
                LCD4_OUT_STR("HIGH Th: 30\xDF""C *!");
                PORTD &= 0xE0; // Bật sáng 5 LED cảnh báo (Active LOW)
            } else {
                // Nhiệt độ bình thường < 30 độ C: TẮT LED (đúng 16 ký tự, xóa dấu *!)
                LCD4_OUT_STR("HIGH Th: 30\xDF""C   ");
                PORTD |= 0x1F; // Tắt 5 LED cảnh báo
            }
        } else if (status == -6) {
            // Lỗi kiểm tra toàn vẹn dữ liệu (Checksum Error)
            LCD4_CUR_GOTO(1, 0);
            LCD4_OUT_STR("DHT11: Sum Error");
            LCD4_CUR_GOTO(2, 0);
            LCD4_OUT_STR("Checksum Invalid");
            PORTD |= 0x1F; // Trạng thái xác định: Tắt LED cảnh báo
        } else {
            // Trường hợp mất tín hiệu, chưa cắm chân PA1 hoặc lỏng dây
            LCD4_CUR_GOTO(1, 0);
            LCD4_OUT_STR("DHT11: No Signal");
            LCD4_CUR_GOTO(2, 0);
            LCD4_OUT_STR("Check Pin PA1   ");
            PORTD |= 0x1F; // Trạng thái xác định: Tắt LED cảnh báo
        }

        // Chu kỳ lấy mẫu khuyến nghị theo datasheet của Aosong (2 giây)
        _delay_ms(2000);
    }

    return 0;
}
