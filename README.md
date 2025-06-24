# 🎛️ Media Archiver

**FOSS playlist downloader + DJ prep tool**  
Built for archiving and signal preservation by the ꪑꪮꪻꫝꫀ᥅ᦓꫝ꠸ρ 🛸

---

## 🚀 Features

- ✅ Accepts Spotify, YouTube & SoundCloud links
- ✅ Auto-downloads, renames, and archives audio
- ✅ Clean Tag or DJ Mode (with BPM + Key detection)
- ✅ Rekordbox XML export for Pioneer decks
- ✅ Animated traffic-light download bar (green, orange, red)
- ✅ FLAC default + MP3 toggle
- ✅ Modular fallback font logic: DejaVu → Segoe UI → Arial
- ✅ Watchlist syncing for saved playlists
- ✅ Fully standalone Windows executable (via `build.bat`)
- ✅ Semiotic OS-aligned UI ✨️

---

## 🛠️ Usage

1. Paste a playlist link (Spotify / YouTube / SoundCloud)
2. Choose mode:
   - `Clean` – for tidy archives
   - `DJ` – adds BPM/key and rekordbox export
3. Hit `download & archive` or run `watchlist sync`

🎧 Files are saved in `/archive/[playlist name]`

---

## 🔨 Building from Source

```bash
py -m pip install pyinstaller
pyinstaller --onefile --windowed media_archiver.py
```

> Or just run `build.bat`

---

## 📂 Files Included

- `media_archiver.py` – main app logic
- `build.bat` – 1-click build script
- `DejaVuSans-BoldOblique.ttf` – FOSS font for UI
- `watchlist.json` – stores tracked playlists
- `archive/` – output folder

---

## 🌍 License

FOSS. Remix, fork, distribute.  
This is the signal 🔊  
