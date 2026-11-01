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

# Fuse bits as configured in report (Page 41):
# Low Fuse = 0xFF (Ext Crystal 8MHz, SUT1=1, SUT0=1)
# High Fuse = 0xD9 (SPIEN=0, BOOTSZ=00, etc.)
LFUSE = 0xFF
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

# Write Fuse bits to ATmega16 (8MHz external crystal)
fuse:
	$(AVRDUDE) -c $(PROGRAMMER) -p $(AVRDUDE_MCU) -U lfuse:w:$(LFUSE):m -U hfuse:w:$(HFUSE):m

clean:
	rm -f $(TARGET).elf $(TARGET).hex $(TARGET).o

.PHONY: all clean flash fuse
