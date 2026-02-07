# BUZZER PIANO

**A computer-controlled virtual piano that plays sound through a microcontroller-driven piezo buzzer over a USB serial connection.**

The system is split into two parts:
- **Computer application** — Graphical piano interface and serial controller
- **Microcontroller mpy script** — Receives note data and generates sound using PWM

Due to Windows COM port exclusive-access limitations, **this only works on Linux.**

https://github.com/user-attachments/assets/6d5003f8-bf1f-4924-867a-da4762076cf4


## Overview

Play a virtual piano on the computer while producing physical sound through a passive piezo buzzer connected to a microcontroller (ESP, Raspberry Pi Pico, or similar).

1. The desktop app connects to a microcontroller over a serial (USB) port.
2. A virtual piano keyboard is displayed.
3. When a key is pressed with the mouse:
    - The corresponding musical note is sent over serial.
4. The microcontroller:
    - Receives the note data
    - Generates a PWM signal at the correct frequency
    - Drives a passive piezo buzzer to produce the sound

## Features
- Graphical piano interface
- Configurable number of piano octaves
- User-defined MCU pin via REPL

## Running the project
### Computer side
Run the main script or executable. A GUI window will open and prompt you for the following information:
1. **Number of octaves** to display on the virtual piano (starting from octave 3)
2. **Serial port**, for example:
    *`/dev/ttyACM0`*

After clicking **`DONE`**, the application will attempt to connect to the microcontroller.
If the connection is successful, the virtual piano interface will appear.

The application is then ready to send note data to the microcontroller.

### MCU side
Copy the mcu.py as the main script on the board.
Exemple using mpremote:
```bash
mpremote cp mpy/mcu.py :main.py
```
Open the REPL. The program will prompt you to choose a GPIO pin for the buzzer.
Enter the number of the pin connected to the passive piezo buzzer.

The microcontroller is now ready to receive note data from the virtual piano.

## Building / Running
### Computer
#### Use the binary:
[See Releases](https://github.com/baerkanogue/buzzer-piano/releases/)

#### Or run from source:
| Dependancy | Version |
|--------|---------|
| Python | 3.13.11 |
| PyQt6 | 6.10.2 |
| Pygame | 2.6.1 |
| Pyserial | 3.5 |
| Colorama | 0.4.6 |

Install dependencies:
```bash
python -m venv .venv
pip install -r requirements.txt
```

#### Or compile from source:

```bash
pyinstaller \
--onefile \
--add-data "misc/:misc" \
--add-data "game/assets:game/assets" \
--name "buzzer_piano" \
main.py

chmod +x dist/buzzer_piano
```

### Microcontroller
- Micropython
- Passive piezo buzzer