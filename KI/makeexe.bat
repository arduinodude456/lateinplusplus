pip install pyinstaller
pip install requests
pip install pillow
pip install groq
pyinstaller --onefile --noconsole ^
  --add-data "cat.jpg;." ^
  --add-data "wissen.txt;." ^
  lingo.py



