pip install pyinstaller
pyinstaller --onefile --noconsole ^
  --add-data "cat.jpg;." ^
  --add-data "wissen.txt;." ^
  lingo.py

