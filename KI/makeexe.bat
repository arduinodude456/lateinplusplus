py -m pip install pyinstaller
py -m pip install requests
py -m pip install pillow
py -m pip install groq
py -m pip install threading
py -m pyinstaller --onefile --noconsole ^
  --add-data "cat.jpg;." ^
  --add-data "wissen.txt;." ^
  assistant.py



