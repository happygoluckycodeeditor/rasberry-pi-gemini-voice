"""Minimal I2C LCD test.

- Designed for a common 16x2 LCD with a PCF8574 backpack
- Uses RPLCD's CharLCD

Run on Raspberry Pi:
    python3 examples/lcd_test.py

If your screen shows nothing, adjust the contrast screw on the I2C backpack.
"""

from RPLCD.i2c import CharLCD


LCD_I2C_ADDR = 0x27  # change if i2cdetect shows something else
LCD_COLS = 16
LCD_ROWS = 2


def main() -> None:
    lcd = CharLCD(
        i2c_expander="PCF8574",
        address=LCD_I2C_ADDR,
        port=1,
        cols=LCD_COLS,
        rows=LCD_ROWS,
        charmap="A02",
    )

    lcd.clear()
    lcd.write_string("Hello from Pi!")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("LCD works :)"[:LCD_COLS])


if __name__ == "__main__":
    main()
