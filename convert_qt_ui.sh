rm pyqt/main_ui.py

pyuic6 -x pyqt/ui/main.ui -o pyqt/main_ui.py

echo "pyqt/ui/main.ui -> pyqt/main_ui.py"