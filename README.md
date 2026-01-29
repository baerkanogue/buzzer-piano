## BUZZER PIANO

**A computer-controlled virtual piano that plays real sound through a microcontroller-driven piezo buzzer over a USB serial connection.**

The system is split into two parts:
- **Computer application** — Graphical piano interface and serial controller
- **Microcontroller firmware** — Receives note data and generates sound using PWM

### Overview

This project allows a user to play a virtual piano on a computer while producing physical sound through a passive piezo buzzer connected to a microcontroller (ESP, Raspberry Pi Pico, or similar).

1. The desktop app connects to a microcontroller over a serial (USB) port.
2. A virtual piano keyboard is displayed.
3. When a key is pressed with the mouse:
    - The corresponding musical note is sent over serial.
4. The microcontroller:
    - Receives the note data
    - Generates a PWM signal at the correct frequency
    - Drives a passive piezo buzzer to produce the sound

### Features
- Configurable number of piano octaves
- Graphical piano interface
- Serial communication between PC and MCU
- Real-time tone generation using PWM
- Hardware-agnostic design (works with multiple MCU types)