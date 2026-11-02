# ========================================================
# Makefile for ATmega16 DHT11 Temperature Monitor Project
# ========================================================

MCU = atmega16
F_CPU = 8000000UL
TARGET = tempsen
SRC = tempsen.c

CC = avr-gcc
OBJCOPY = avr-objcopy
SIZE = avr-size
AVRDUDE = avrdude

# Programmer type (USBasp by default as in report)
PROGRAMMER = usbasp
AVRDUDE_MCU = m16

# Fuse bits matching the report: calibrated internal RC, 8 MHz.
# Low Fuse = 0xE4 (CKSEL=0100, SUT=10).
# High Fuse = 0xD9 (JTAGEN=1: disabled, SPIEN=0: ISP enabled).
LFUSE = 0xE4
HFUSE = 0xD9

CFLAGS = -Wall -Os -mmcu=$(MCU) -DF_CPU=$(F_CPU) -I.

all: $(TARGET).hex

$(TARGET).elf: $(SRC) hunget_lcd.h
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET).elf
	$(SIZE) $(TARGET).elf

$(TARGET).hex: $(TARGET).elf
	$(OBJCOPY) -O ihex -R .eeprom $(TARGET).elf $(TARGET).hex
	@echo "========================================================"
	@echo "Build successful! Generated: $(TARGET).hex"
	@echo "========================================================"

# Flash firmware via USBasp
flash: $(TARGET).hex
	$(AVRDUDE) -c $(PROGRAMMER) -p $(AVRDUDE_MCU) -U flash:w:$(TARGET).hex:i

# Write Fuse bits to ATmega16 (8 MHz internal RC oscillator)
fuse:
	$(AVRDUDE) -c $(PROGRAMMER) -p $(AVRDUDE_MCU) -U lfuse:w:$(LFUSE):m -U hfuse:w:$(HFUSE):m

clean:
	rm -f $(TARGET).elf $(TARGET).hex $(TARGET).o

.PHONY: all clean flash fuse
