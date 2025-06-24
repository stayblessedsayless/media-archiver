
import os
import threading
import time
from tkinter import Tk, Label, Entry, Button, StringVar, Radiobutton, messagebox, ttk

def choose_font():
    try:
        return ("IBM Plex Sans", 11, "italic")
    except:
        return ("Arial", 11, "italic")

def simulate_download(progress, status_label):
    try:
        status_label.config(text="downloading...", foreground="orange")
        for i in range(101):
            progress["value"] = i
            time.sleep(0.02)
            progress.update()
        status_label.config(text="done!", foreground="lime")
    except Exception:
        progress["value"] = 0
        status_label.config(text="error!", foreground="red")

def run_gui():
    print("GUI launching…")
    root = Tk()
    root.title("Playlist Archiver – Layer 2 Font Fallback")
    root.geometry("540x400")
    root.configure(bg="#000000")

    font_choice = choose_font()

    # Style dictionaries
    sty_label = {"bg": "#000000", "fg": "#DFFF00", "font": font_choice}
    entry_style = {"bg": "#1a1a1a", "fg": "#DFFF00", "insertbackground": "#DFFF00", "width": 62,
                   "highlightbackground": "#DFFF00"}
    btn_style = {"bg": "#1a1a1a", "fg": "#DFFF00", "activebackground": "#333333", "activeforeground": "#DFFF00",
                 "relief": "raised", "bd": 2}
    radio_style = {"bg": "#000000", "fg": "#DFFF00", "selectcolor": "#1a1a1a", "activebackground": "#000000"}

    Label(root, text="paste Spotify / YouTube / SoundCloud playlist URL:", **sty_label).pack(pady=6)
    Entry(root, **entry_style).pack(pady=4)

    # mode selector
    mode_var = StringVar(value="Clean")
    Label(root, text="select processing mode:", **sty_label).pack(pady=(8, 0))
    Radiobutton(root, text="Clean Tag", variable=mode_var, value="Clean", **radio_style).pack()
    Radiobutton(root, text="DJ Prep (BPM/key + XML)", variable=mode_var, value="DJ", **radio_style).pack()

    # codec selector
    codec_var = StringVar(value="flac")
    Label(root, text="choose audio format:", **sty_label).pack(pady=(10, 0))
    Radiobutton(root, text="FLAC (hi‑res)", variable=codec_var, value="flac", **radio_style).pack()
    Radiobutton(root, text="MP3 (backup)", variable=codec_var, value="mp3", **radio_style).pack()

    Button(root, text="download & archive", command=lambda: threading.Thread(
        target=simulate_download, args=(progress, status_label)).start(), **btn_style).pack(pady=8)
    Button(root, text="run watchlist sync", command=lambda: messagebox.showinfo("info", "simulated sync"), **btn_style).pack(pady=2)

    # Progress bar
    progress = ttk.Progressbar(root, length=400, mode='determinate')
    progress.pack(pady=10)
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TProgressbar", troughcolor="#1a1a1a", bordercolor="#000000",
                    background="#FF7F00", lightcolor="#FF7F00", darkcolor="#FF7F00")

    # Status label
    status_label = Label(root, text="", **sty_label)
    status_label.pack(pady=2)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
