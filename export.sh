pyinstaller \
--onefile \
--add-data "misc/:misc" \
--add-data "game/assets:game/assets" \
--name "buzzer_piano" \
main.py

chmod +x dist/buzzer_piano

mkdir export

mv dist/buzzer_piano export/buzzer_piano
cp misc/modules_licenses.txt export/licenses.txt
cp mpy/mcu.py export/mcu.py

cd export
tar -czvf bp_linux_VERSION.tar.gz .
rm buzzer_piano
rm licenses.txt
cd -

echo Done