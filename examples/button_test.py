"""Minimal GPIO button/switch test.

Matches the wiring used by `ai_assistant.py`:
- GPIO17 is pulled down internally
- Switch connects 3.3V -> GPIO17 to trigger a press

Run on Raspberry Pi:
    python3 examples/button_test.py
"""

from gpiozero import Button


SWITCH_GPIO = 17


def main() -> None:
    button = Button(SWITCH_GPIO, pull_up=False)

    print("Waiting for button/switch on GPIO17...")

    while True:
        button.wait_for_press()
        print("Pressed!")

        button.wait_for_release()
        print("Released!")


if __name__ == "__main__":
    main()
