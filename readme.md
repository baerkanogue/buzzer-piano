# BUZZER PIANO

**A computer-controlled virtual piano that plays sound through a microcontroller-driven piezo buzzer over a USB serial connection.**

The system is split into two parts:
- **Desktop application** — Graphical piano interface and serial controller
- **MCU Micropython script** — Receives note data and generates sound using PWM


https://github.com/user-attachments/assets/6d5003f8-bf1f-4924-867a-da4762076cf4

## Features
- Graphical piano interface
- Configurable number of piano octaves
- User-defined MCU pin via REPL (Linux)

## Running the project
### MCU side
1. Copy the **OS-appropriate** mcu.py as the main script on the board.
Exemple using mpremote:
```bash
mpremote cp mpy/mcu_linux.py :main.py
```
2. Configure the GPIO pin used for the buzzer:
    - **Linux**
        - Open the REPL after flashing the script.
        - The program will prompt you to choose a GPIO pin.
        - Enter the number of the pin connected to the passive piezo buzzer.
    - **Windows** 
        - On Windows, the serial port cannot be shared between the REPL and the running script, so GPIO selection must be hardcoded.
        - The script defaults to **GPIO pin 2**.
        - To use a different pin, edit mcu_windows.py before copying it to the board.

3. The microcontroller is now ready to receive note data from the virtual piano.


### Computer side
1. Run the main script or executable. A GUI window will open and prompt you for the following information:
    - **Number of octaves** to display on the virtual piano (starting from octave 3)
    - **Serial port**, for example:
        - Linux: *`/dev/ttyACM0`*
        - Windows: *`COM3`*
2. After clicking **`DONE`**, the application will attempt to connect to the microcontroller.
3. If the connection is successful, the virtual piano interface will appear. The application is then ready to send note data to the microcontroller.

## Building / Running
### Microcontroller
- [Micropython](https://micropython.org/download/)
- [Passive piezo buzzer](https://deepbluembedded.com/active-buzzer-vs-passive-buzzer/)

### Computer
#### Use the binary: 
**[See Releases](https://github.com/baerkanogue/buzzer-piano/releases/)**

#### Or run from source:
| Dependency | Version | Notes |
|------------|---------|-------|
|  Python    | 3.13.11 | 
|  PyQt6     | 6.10.2  | GUI
|  Pygame    | 2.6.1   | Virtual piano framework
|  Pyserial  | 3.5     | Sending data to MCU
|  Mpremote  | 1.27    | Sending script to MCU
|  Colorama  | 0.4.6   | stdout coloring (debug)

Install dependencies:
```bash
# Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
```pwsh
# Windows (Powershell)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Or compile from source:

```bash
# Linux
pyinstaller \
--onefile \
--add-data "misc:misc" \
--add-data "game/assets:game/assets" \
--name "buzzer_piano" \
main.py

chmod +x dist/buzzer_piano
```
```pwsh
# Windows (Powershell)
pyinstaller `
--onefile `
--noconsole `
--icon=misc\buzzer.icon `
--add-data "misc;misc" `
--add-data "game\assets;game\assets" `
--name "buzzer_piano" `
main.py
```