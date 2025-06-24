# ---------- media-archiver GUI (Spotify / YouTube / SoundCloud / Bandcamp) ----------
import os, re, subprocess, json
from tkinter import Tk, Label, Entry, Button, messagebox, StringVar, Radiobutton
from mutagen import File as MutagenFile
import yt_dlp, librosa
from xml.etree.ElementTree import Element, SubElement, ElementTree

ARCHIVE_DIR = "archive"
WATCHLIST_FILE = "watchlist.json"
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# ---------------- watchlist store ----------------
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f: json.dump({}, f)
with open(WATCHLIST_FILE, "r") as f: watchlist = json.load(f)

# ---------------- helpers ----------------
slug = lambda s: "".join(c for c in s if c.isalnum() or c in " -_[](){}!").strip()

def bpm_key(path):
    try:
        y, sr = librosa.load(path, mono=True)
        bpm, _ = librosa.beat.beat_track(y=y, sr=sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        key = "C C# D D# E F F# G G# A A# B".split()[chroma.mean(1).argmax()%12]
        return round(bpm), key
    except Exception: return None, None

def rekordbox_xml(tracks, xml_path):
    root = Element("DJ_PLAYLISTS")
    pl = SubElement(root, "PLAYLIST", Name="Playlist")
    for p, title, artist, bpm, key in tracks:
        url = "file://localhost" + os.path.abspath(p)
        tr = SubElement(pl, "TRACK", TrackID="1", Name=title, Artist=artist,
                        BPM=str(bpm or ""), Key=key or "", FilePath=url)
        SubElement(tr, "POSITION_MARK", Name="Start", Type="0", Start="0.000")
    ElementTree(root).write(xml_path, encoding="utf-8", xml_declaration=True)

# ------------- source detect + download -------------
def source(url):
    if "open.spotify.com" in url: return "spotify"
    if re.search(r"youtube\.com|youtu\.be", url): return "youtube"
    if "soundcloud.com" in url: return "soundcloud"
    if "bandcamp.com"   in url: return "bandcamp"
    return "unknown"

def dl_spotify(url, codec):
    fmt = ["--audio-format", codec] if codec!="mp3" else []
    subprocess.run(["spotdl", url, "--output", "temp_downloads", *fmt])

def dl_ytdlp(url, codec):
    y_opts = {"format":"bestaudio/best",
              "outtmpl":"temp_downloads/%(title)s.%(ext)s",
              "quiet":True,
              "postprocessors":[{"key":"FFmpegExtractAudio",
                                 "preferredcodec":codec,"preferredquality":"0"}]}
    with yt_dlp.YoutubeDL(y_opts) as ydl: ydl.download([url])

def grab(url, codec):
    src = source(url)
    if src=="spotify": dl_spotify(url, codec)
    elif src in ("youtube","soundcloud","bandcamp"): dl_ytdlp(url, codec)
    else: raise ValueError("link type not supported")

# ------------- main processing -------------
def process(url, mode, codec):
    grab(url, codec)
    pl_name = slug(watchlist.get(url,"Manual Downloads"))
    folder  = os.path.join(ARCHIVE_DIR, pl_name); os.makedirs(folder, exist_ok=True)
    xml_tracks=[]

    for r,_,fs in os.walk("temp_downloads"):
        for f in fs:
            if f.lower().endswith(("."+codec,)):
                src = os.path.join(r,f)
                artist,title="Unknown Artist",os.path.splitext(f)[0]
                try:
                    tags=MutagenFile(src, easy=True)
                    if tags:
                        artist=tags.get("artist",[artist])[0]
                        title =tags.get("title" ,[title ])[0]
                except: pass
                bpm,key= (bpm_key(src) if mode=="DJ" else (None,None))
                new=f"{artist} - {title}"
                if bpm: new+=f" ({bpm} BPM)"
                if key: new+=f" [{key}]"
                new+=f".{codec}"
                dest=os.path.join(folder,new); os.rename(src,dest)
                if mode=="DJ": xml_tracks.append((dest,title,artist,bpm,key))

    subprocess.run(["rm","-rf","temp_downloads"], shell=True)
    if mode=="DJ" and xml_tracks:
        rekordbox_xml(xml_tracks, os.path.join(folder,"rekordbox.xml"))

# ------------- GUI callbacks -------------
def add_watch(url):
    watchlist[url]=url
    with open(WATCHLIST_FILE,"w") as f: json.dump(watchlist,f,indent=2)

def run_watch():
    for u in watchlist: process(u, mode_var.get(), codec_var.get())

def do_download():
    url=entry.get().strip()
    if not url: messagebox.showerror("Error","Paste a URL"); return
    add_watch(url)
    try:
        process(url, mode_var.get(), codec_var.get())
        messagebox.showinfo("Done","Playlist archived.")
    except Exception as e:
        messagebox.showerror("Oops",str(e))

# ---------------- GUI ----------------
root=Tk(); root.title("Media Archiver"); root.geometry("560x380")
root.configure(bg="#000000")
L=lambda t:Label(root,text=t,bg="#000000",fg="#DFFF00",font=("Arial",11))
entry=Entry(root,bg="#1a1a1a",fg="#DFFF00",insertbackground="#DFFF00",width=64,
            highlightbackground="#DFFF00")

L("paste Spotify / YouTube / SoundCloud / Bandcamp link:").pack(pady=6)
entry.pack(pady=4)

mode_var=StringVar(value="Clean")
L("processing mode:").pack(pady=(8,0))
for txt,val in [("Clean Tag","Clean"),("DJ Prep (BPM/key + XML)","DJ")]:
    Radiobutton(root,text=txt,variable=mode_var,value=val,bg="#000000",fg="#DFFF00",
                selectcolor="#1a1a1a",activebackground="#000000").pack()

codec_var=StringVar(value="flac")
L("audio format:").pack(pady=(10,0))
for txt,val in [("FLAC (hi-res)","flac"),("MP3 (backup)","mp3")]:
    Radiobutton(root,text=txt,variable=codec_var,value=val,bg="#000000",fg="#DFFF00",
                selectcolor="#1a1a1a",activebackground="#000000").pack()

btn = lambda t,cmd: Button(root,text=t,command=cmd,bg="#1a1a1a",fg="#DFFF00",
                           activebackground="#333",activeforeground="#DFFF00",bd=2)
btn("download & archive", do_download).pack(pady=8)
btn("run watchlist sync", run_watch).pack(pady=2)

root.mainloop()