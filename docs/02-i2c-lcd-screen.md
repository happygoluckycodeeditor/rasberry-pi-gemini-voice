# 02 — Connect an IIC/I2C LCD 1602 (PCF8574)

This guide shows how to wire a common **IIC/I2C LCD 1602** module (a 16x2 LCD with an I2C backpack—often labeled **PCF8574**) and print text from Python.

## What you’ll need

- Raspberry Pi
- IIC/I2C LCD 1602 module (16x2 + PCF8574 backpack)
- Jumper wires

## Wiring (I2C)

Most I2C LCD backpacks have 4 pins:

- **GND** → Pi **GND**
- **VCC** → Pi **5V** (common) or **3.3V** (often works too)
- **SDA** → Pi **SDA** (GPIO2, physical pin 3)
- **SCL** → Pi **SCL** (GPIO3, physical pin 5)

### Notes

- Many PCF8574 boards are happy on **5V** power, while I2C lines are still safe because the backpack is usually designed for I2C.
- If you’re unsure, start with **3.3V** for VCC. If the backlight is dim or unstable, try 5V.

### Quick “parts list” callout

- LCD: “**IIC/I2C LCD 1602**” (sometimes sold as “1602A + IIC/I2C backpack”)
- Backpack chip: typically **PCF8574** (address commonly `0x27`)

## Enable I2C

If you haven’t already, enable I2C using the setup guide:

- See `docs/01-raspberry-pi-setup.md` → “Enable I2C”.

## Find the I2C address

Run:

```bash
i2cdetect -y 1
```

You’ll typically see something like `27` or `3f`.

- `0x27` is extremely common (your `ai_assistant.py` uses `0x27`).

## Install the Python library

```bash
pip install RPLCD
```

## Minimal LCD test script

This repo includes `examples/lcd_test.py`.

What it does:
- Initializes a 16x2 LCD over I2C
- Prints two lines

### Common config knobs

- `LCD_I2C_ADDR`: change if your `i2cdetect` shows a different address
- `port=1`: correct for modern Raspberry Pi models

## Troubleshooting

### Nothing shows on the LCD

- Turn the small **contrast potentiometer** on the I2C backpack (tiny screw). This is the #1 issue.
- Confirm the address with `i2cdetect -y 1`.
- Confirm your wires:
  - SDA = GPIO2 (pin 3)
  - SCL = GPIO3 (pin 5)

### `OSError: [Errno 121] Remote I/O error`

- Usually wrong I2C address or wiring.

### Random characters

- Contrast set too high/low.
- Power instability (try shorter cables / better PSU).
