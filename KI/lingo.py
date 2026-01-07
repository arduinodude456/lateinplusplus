import tkinter as tk
from tkinter import scrolledtext
import requests
import threading

from PIL import Image, ImageTk  # Pillow wird benötigt
import sys
import os

def resource_path(relative_path):
    """Pfad für Dateien finden – funktioniert in .py und .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

from PIL import Image, ImageTk

def show_splash(root, main_app_callback):
    splash = tk.Toplevel()
    splash.overrideredirect(True)

    bildpfad = resource_path("cat.jpg")
    img = Image.open(bildpfad)
    splash_img = ImageTk.PhotoImage(img)

    w, h = img.size
    screen_w = splash.winfo_screenwidth()
    screen_h = splash.winfo_screenheight()
    x = (screen_w - w) // 2
    y = (screen_h - h) // 2
    splash.geometry(f"{w}x{h}+{x}+{y}")

    label = tk.Label(splash, image=splash_img)
    label.image = splash_img
    label.pack()

    root.after(5000, lambda: (splash.destroy(), main_app_callback()))

# ---------------------------------------------------------
#  CONFIG
# ---------------------------------------------------------
GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.3-70b-versatile"   # Beispielmodell – anpassen falls nötig
def lade_wissen():
    pfad = resource_path("wissen.txt")
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"[Fehler beim Laden der Wissensdatei: {e}]"

# Dein statisches Wissen, das in jeden Prompt eingebaut wird
WISSEN = lade_wissen()


SYSTEM_PROMPT_TEMPLATE = (
    "Du bist ein hilfreicher, geduldiger KI-Assistent.\n"
    "Dies ist das Wissen, mit dem du die Fragen des Benutzers "
    "leicht verständlich beantwortest:\n"
    f"'{WISSEN}'\n"
    "Wenn dich der Nutzer etwas fragt, was nichts mit dem Thema zu tun hat, z.B. wie das Wetter wird oder was in Stranger Things Staffel 2 passiert, antwortest du am Besten mit: \n'Da kann ich dir leider nicht helfen, aber hey, wir sind hier um Latein zu üben! Wie kann ich dir helfen?'."
    "Wenn der Nutzer jedoch explizit erwähnt, dass er Lehrer ist, hilfst du ihm bei jeder Frage weiter."
    "Der Nutzer stellt folgende Frage:\n{frage}"
)

# ---------------------------------------------------------
#  FUNKTION: Anfrage an Groq senden
# ---------------------------------------------------------
def ask_groq(user_question):
    url = "https://api.groq.com/openai/v1/chat/completions"

    prompt = SYSTEM_PROMPT_TEMPLATE.format(frage=user_question)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Du bist ein KI-Assistent."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


# ---------------------------------------------------------
#  GUI-FUNKTIONEN
# ---------------------------------------------------------
def send_message():
    user_msg = entry.get().strip()
    if not user_msg:
        return

    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"Du: {user_msg}\n")
    chat_box.config(state="disabled")
    chat_box.yview(tk.END)

    entry.delete(0, tk.END)

    # Anfrage in Thread auslagern, damit GUI nicht blockiert
    threading.Thread(target=process_ai_response, args=(user_msg,)).start()


def process_ai_response(user_msg):
    try:
        ai_response = ask_groq(user_msg)
    except Exception as e:
        ai_response = f"[Fehler bei der Anfrage: {e}]"

    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"KI: {ai_response}\n\n")
    chat_box.config(state="disabled")
    chat_box.yview(tk.END)


# ---------------------------------------------------------
#  TKINTER-GUI
# ---------------------------------------------------------
root = tk.Tk()
root.title("Groq KI-Assistent")
def start_main_window(root):
    chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled", width=70, height=25)
    chat_box.pack(padx=10, pady=10)

    entry = tk.Entry(root, width=70)
    entry.pack(side=tk.LEFT, padx=10, pady=10)

    send_button = tk.Button(root, text="Senden", command=send_message)
    send_button.pack(side=tk.LEFT, padx=5)
show_splash(root, lambda: start_main_window(root))

root.mainloop()
    








