
# 🖨️ Ender 3 Bukalemun Yazıcı / Pen This Printer
https://www.thingiverse.com/thing:7352596
https://www.youtube.com/watch?v=NHBilCCeiWg


**Turn your Ender 3 into a pen plotter!**  
Draw single-line text using Hershey fonts. Supports Turkish characters like `ğ`, `ü`, `ş`, `ı`, `ö`, `ç`.

![Example Output](cikti.jpg)

---

## ✨ Features

- 🖊️ **Pen plotting:** Turn your Ender 3 into a text writer
- 🔤 **Single-line fonts:** Hershey font family (cursive, rowmans, gothic, etc.)
- 🇹🇷 **Turkish character support:** Ğ,ğ,İ,ı,Ö,ö,Ü,ü,Ç,ç,Ş,ş
- 📐 **Dynamic character spacing:** Solves spacing issues with J, j, K, k
- ⚙️ **Easily adjustable:** SCALE, LETTER_SPACING, LINE_SPACING, DRAW_Z, TRAVEL_Z
- 🐍 **Python based:** Only needs Python 3.7+ and `Hershey-Fonts` package

---

## 📁 Files

| File | Description |
|---|---|
| `ender3_yazi_yaz.py` | Main G-code generator (Turkish) |
| `ender3_pen_writer_en.py` | Main G-code generator (English) |
| `hershey_font2json.py` | Hershey font to JSON vector converter (Turkish) |
| `hershey_font2json_en.py` | Hershey font to JSON vector converter (English) |
| `hershey_cursive.json` | Cursive font vectors |
| `hershey_rowmans.json` | Rowmans font vectors |
| `text.txt` | Example text file |
| `output.gcode` | Example G-code output |

---

## 🚀 Usage

### 1. Requirements

```bash
pip install Hershey-Fonts

### Generate font:

python hershey_font2json_en.py 
(Font selection is done inside the script)

FONT_FILE = "***.json"                  # Font file to use
START_X = 10                            # Starting X coordinate
START_Y = 220                           # Starting Y coordinate
DRAW_Z = 2                              # Pen down height (touching paper)
TRAVEL_Z = 7                            # Pen up height (moving freely)
SCALE = 10                              # Font size
LETTER_SPACING = 0.25 * SCALE / 10      # Space between letters
LINE_SPACING = 13 * SCALE / 10          # Space between lines
SPEED = 1000                            # Drawing speed

#Generate G-code:

```bash
python ender3_pen_writer_en.py
(You can test the output at https://ncviewer.com)

#Ready-to-use fonts:
hershey_cursive.json # cursive / handwriting style
hershey_rowmans.json # Roman / standard style

