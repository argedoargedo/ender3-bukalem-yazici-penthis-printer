# 🖨️ Ender 3 Bukalemun Yazıcı / Pen This Printer

**Ender 3'ünüzü kalemli bir plottere dönüştürün!**  
Hershey fontları ile tek hatlı (single line) yazılar çizin. Türkçe karakter desteği ile `ğ`, `ü`, `ş`, `ı`, `ö`, `ç` gibi harfleri sorunsuz kullanın.


---

## ✨ Özellikler

- 🖊️ **Kalemli çizim:** Ender 3'ünüzü yazı yazabilen bir plotter yapın
- 🔤 **Tek hatlı fontlar:** Hershey font ailesi (cursive, rowmans, gothic vb.)
- 🇹🇷 **Türkçe karakter desteği:** Ğ,ğ,İ,ı,Ö,ö,Ü,ü,Ç,ç,Ş,ş
- 📐 **Dinamik karakter aralığı:** J, j, K, k gibi harflerde boşluk sorunu çözüldü
- ⚙️ **Kolay ayarlanabilir:** SCALE, LETTER_SPACING, LINE_SPACING, DRAW_Z, TRAVEL_Z
- 🐍 **Python tabanlı:** Sadece Python 3.7+ ve `Hershey-Fonts` paketi yeterli

---

## 📁 Dosyalar

| Dosya | Açıklama |
|---|---|
| `ender3_yazi_yaz.py` | Ana G-code üretici (Türkçe) |
| `ender3_pen_writer_en.py` | Ana G-code üretici (İngilizce) |
| `hershey_font2json.py` | Hershey fontlarından JSON vektör üretici (Türkçe) |
| `hershey_font2json_en.py` | Hershey fontlarından JSON vektör üretici (İngilizce) |
| `hershey_cursive.json` | El yazısı (cursive) font vektörleri |
| `text.txt` | Örnek metin dosyası |
| `output.gcode` | Örnek G-code çıktısı |

---

## 🚀 Kullanım

### 1. Gereksinimler

```bash
pip install Hershey-Fonts


###Font oluşturma:


```bash
python hershey_font2json.py 
(Font tipi seçimi yazılımın içinde)

###Ender3_yazi_yaz

içindeki Ayarlar:
FONT_FILE = "***.json"  		        # Kullanılacak font
START_X = 10                        # Başlangıç X 
START_Y = 220                       # Başlangıç Y 
DRAW_Z = 2                          # Kalem kağıda değme yüksekliği
TRAVEL_Z = 7                     		# Kalem kalkma yüksekliği
SCALE = 10                          # Harf büyüklüğü 
LETTER_SPACING = 0.25 * SCALE / 10  # Harf aralığı
LINE_SPACING = 13 * SCALE / 10      # Satır aralığı
SPEED = 1000                        # Çizim hızı 

#Output.gcode oluşturma:

```bash
python ender3_yazi_yaz.py 



( çıktıyı isterseniz https://ncviewer.com/ adresinde deneyebilirsiniz)

###Hazır fontlar:
hershey_cursive.json      #el yazısı
hershey_rowmans.json      

