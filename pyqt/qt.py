from PyQt6 import QtGui, QtWidgets, QtCore
from dataclasses import dataclass
from pathlib import Path
import pyqt.main_ui as ui
import sys
import serial


@dataclass
class RuntimeData:
    octaves: int
    mcu_port: str


class Window:
    def __init__(self) -> None:
        self.app: QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)
        self.window: QtWidgets.QMainWindow = QtWidgets.QMainWindow()

        self.ui: ui.Ui_MainWindow = ui.Ui_MainWindow()
        self.ui.setupUi(self.window)

        self.icon_path: Path = Path("misc", "buzzer.icon")
        self.window.setWindowIcon(QtGui.QIcon(str(self.icon_path)))

        self.ui.done_button.pressed.connect(self._on_connect_button_pressed)

        self.runtime_data: RuntimeData
        self.is_done_button_pressed: bool = False
        self.is_window_closed: bool = False

        self.window.closeEvent = self._on_window_close  # type: ignore

    def run(self) -> RuntimeData:
        self.window.show()
        while not self.is_done_button_pressed and not self.is_window_closed:
            self.app.processEvents()

        if self.is_window_closed and not self.is_done_button_pressed:
            sys.exit(0)

        return self.runtime_data

    def _on_connect_button_pressed(self) -> None:
        octaves: int = self.ui.octaves_spin_box.value()
        mcu_port: str = self.ui.port_line_edit.text()

        try:
            serial_port: serial.Serial = serial.Serial(mcu_port)
        except serial.SerialException:
            self.ui.done_button.setText("Invalid port, try again...")
            QtCore.QTimer.singleShot(1500, self._reset_done_button_text)
            return

        self.runtime_data = RuntimeData(octaves, mcu_port)

        self.is_done_button_pressed = True
        self.window.close()

    def _on_window_close(self, event: QtGui.QCloseEvent) -> None:
        self.is_window_closed = True
        event.accept()

    def _reset_done_button_text(self) -> None:
        self.ui.done_button.setText("DONE")


if __name__ == "__main__":
    window: Window = Window()
    data: RuntimeData = window.run()
    print(data)
