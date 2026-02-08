# BUZZER PIANO

**A computer-controlled virtual piano that plays sound through a microcontroller-driven piezo buzzer over a USB serial connection.**

The system is split into two parts:
- **Computer application** — Graphical piano interface and serial controller
- **Microcontroller mpy script** — Receives note data and generates sound using PWM

Due to Windows COM port exclusive-access limitations, **this only works on Linux.**

https://github.com/user-attachments/assets/6d5003f8-bf1f-4924-867a-da4762076cf4

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
### Microcontroller
- [Micropython](https://micropython.org/download/)
- [Passive piezo buzzer](https://deepbluembedded.com/active-buzzer-vs-passive-buzzer/)

### Computer
#### Use the binary: 
**[See Releases](https://github.com/baerkanogue/buzzer-piano/releases/)**

#### Or run from source:
| Dependancy | Version | Notes |
|------------|---------|-------|
|  Python    | 3.13.11 | 
|  PyQt6     | 6.10.2  | GUI
|  Pygame    | 2.6.1   | Virtual piano framework
|  Pyserial  | 3.5     | Sending data to MCU
|  Mpremote  | 1.27    | Sending script to MCU
|  Colorama  | 0.4.6   | stdout coloring (debug)

Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Or compile from source:

```bash
pyinstaller \
--onefile \
--add-data "misc:misc" \
--add-data "game/assets:game/assets" \
--name "buzzer_piano" \
main.py

chmod +x dist/buzzer_piano
```
