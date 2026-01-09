set PATH=%PATH%;%LOCALAPPDATA%\Python\pythoncore-3.14-64\Scripts

py -m pip install pyinstaller
py -m pip install requests
py -m pip install pillow
py -m pip install groq
py -m pip install threading
pyinstaller --onefile --noconsole ^
  --add-data "cat.jpg;." ^
  --add-data "wissen.txt;." ^
  assistant.py






