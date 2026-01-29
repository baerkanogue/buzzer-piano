import sys
import struct
from machine import Pin, PWM


def main() -> None:
    MAX_U16: int = (1 << 16) - 1
    gpio_pin: int = get_gpio_pin()

    buzzer_pin: Pin = Pin(gpio_pin)
    buzzer_pwm: PWM = PWM(buzzer_pin, freq=500, duty_u16=0)

    print("Listening for piano input...")
    try:
        while True:
            line_input = sys.stdin.buffer.read(4)
            frequency_input: int = 0
            try:
                frequency_input = int(struct.unpack("<f", line_input)[0])
            except Exception as error:
                print(f"Invalid frequency input, error: {error}")

            if frequency_input > 0:
                buzzer_pwm.freq(frequency_input)
                buzzer_pwm.duty_u16(MAX_U16 // 2)
            else:
                buzzer_pwm.duty_u16(0)
    except KeyboardInterrupt:
        buzzer_pwm.deinit()
        print("\nKeyboard Interrupt...")


def get_gpio_pin() -> int:
    while True:
        try:
            gpio_pin = int(input("Enter the buzzer's GPIO pin: "))
            return gpio_pin
        except ValueError as error:
            print(f"Invalid GPIO pin number, error: {error}")


if __name__ == "__main__":
    main()
