#!/usr/bin/env python3
"""
Ender 3 / Pen Plotter için Hershey Fontları ile Tek Hatlı Yazı Çizimi
========================================================================

Bu yazılım, Hershey font ailesini kullanarak tek hatlı (single line)
vektörleri G-code'a çevirir. Özellikle kalemli Ender 3 gibi cihazlar için
geliştirilmiştir.

Özellikler:
- JSON formatında font vektörleri kullanır (Hershey)
- Her karakterin gerçek genişliğini dinamik hesaplar (J, j, K, k aralık sorunu çözüldü)
- Türkçe karakterleri destekler (Ğ,ğ,İ,ı,Ö,ö,Ü,ü,Ç,ç,Ş,ş)
- SCALE, LETTER_SPACING, DRAW_Z gibi parametrelerle ince ayar yapılabilir

Kullanım:
1. Hangi fontu kullanacağınızı seçin (FONT_FILE değişkeni)
2. Yazılacak metni TEXT_FILE dosyasına yazın
3. Yazılımı çalıştırın: python yaz.py
4. Oluşan output.gcode dosyasını Cura'ya yükleyip Ender 3'ünüzden çıktı alın

Gereksinimler:
- Python 3.7+
- Hershey font içeren JSON dosyası

Örnek: python yaz.py

Hız dönüşümleri (SPEED ):
600  → 10 
1200 → 20 
1800 → 30 
2400 → 40 
"""

import json
# ============================================================================
# KONFİGÜRASYON AYARLARI - Kullanıcı burayı değiştirsin
# ============================================================================

FONT_FILE = "hershey_cursive.json"      # Kullanılacak font dosyası
TEXT_FILE = "text.txt"                  # Yazılacak metnin bulunduğu dosya
OUTPUT_FILE = "output.gcode"            # Oluşturulacak G-code dosyası

START_X = 10                            # Başlangıç X koordinatı (mm)
START_Y = 220                           # Başlangıç Y koordinatı (mm)

DRAW_Z = 2                              # Kalemin kağıda değdiği yükseklik 
TRAVEL_Z = 7                            # Kalemin havada olduğu yükseklik 

SCALE = 10                              # Harflerin büyüklüğü (1=fontun %100 ölçeği)
LETTER_SPACING = .25 * SCALE / 10       # Harfler arasına eklenecek ek boşluk. rowmans da 2 cursive de .25
LINE_SPACING = 13 * SCALE / 10          # Satırlar arası mesafe
SCALE = SCALE/100                       # Yazılımın anladığı değere indiriyorum

SPEED = 1000                            # Çizim hızı 

# ============================================================================
# FONKSİYONLAR
# ============================================================================

def load_font():
    """JSON font dosyasını yükler ve sözlük olarak döndürür."""
    with open(FONT_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_text():
    """Metin dosyasını yükler ve içeriğini döndürür."""
    with open(TEXT_FILE, encoding="utf-8") as f:
        return f.read()


def get_char_endpoint(font, scale=1.0):
    """
    Bir karakterin konumunun son noktasını hesaplar.
    max_x
    
    Değişkenler:
        scale: Ölçeklendirme faktörü
    
    Dönüş:
        max_x: Karakterin son noktası
    """
    
    max_x = -float('inf')
    
    for stroke in font:
        for x, y in stroke:
            sx = x * scale
            if sx > max_x:
                max_x = sx
    
    # Eğer karakter boşsa veya tek noktadan oluşuyorsa
    if max_x == -float('inf'):
        return 0
    
    return max_x


def generate_letter_gcode(font, x_offset, y_offset, scale):
    """
    Bir karakteri G-code komutlarına çevirir.
    
    Değişkenler:
        font: Karakterin vektör verisi
        x_offset: X ekseni başlangıç noktası
        y_offset: Y ekseni başlangıç noktası
        scale: Ölçeklendirme faktörü
    
    Dönüş:
        list: G-code komut satırları
    """

    lines = []
    

    for stroke in font:

        # Kalemi kaldırarak başlangıç noktasına git
        first = True

        for x, y in stroke:

            sx = x * scale + x_offset
            sy = y * scale + y_offset

            if first:
                lines.append(f"G0 Z{TRAVEL_Z}")
                lines.append(f"G0 X{sx:.3f} Y{sy:.3f}")
                lines.append(f"G1 Z{DRAW_Z}")
                first = False
            else:
                lines.append(f"G1 X{sx:.3f} Y{sy:.3f} F{SPEED}")

    # Karakter bitti, kalemi kaldır
    lines.append(f"G0 Z{TRAVEL_Z}")
    
    return lines


def main():
    """Ana program: metni oku, fontu yükle, G-code'u oluştur ve kaydet."""
    
    # Dosyaları yükle
    text = load_text()
    fonts = load_font()

    # G-code başlığı
    gcode = [
        "G21 ; Milimetre birimi",
        "G90 ; Mutlak konumlama",
        "G28 ; Eksenleri ev konumuna al",
        f"G0 Z{TRAVEL_Z} ; Kalemi kaldır"
    ]


    y_offset = 0
    lines = text.splitlines()
 
    print(f"📝 İşleniyor: {len(lines)} satır, toplam {len(text)} karakter")
    print("-" * 50)

    for line in lines:
        
        x_offset = 0
        
 
        for char in line:
            
            # Boşluk karakteri
            if char == " ":
                x_offset += 15 * SCALE + LETTER_SPACING
                continue

            # Tab karakteri (boşluk değerine bağımlı istediğiniz değer)
            if char == "\t":
                x_offset += 180 * SCALE + LETTER_SPACING  
                continue
                
            # Karakter fontta yoksa uyar ve atla    
            if char not in fonts:
                print(f"  Uyarı: '{char}' karakteri fontta bulunamadı (atlanıyor)")
                continue
            
            font = fonts[char]
            
            # 1. Önce karakterin son noktasını bul
            char_end = get_char_endpoint(font, SCALE)
            
            # 2. Karakteri çiz
            letter_gcode = generate_letter_gcode(
                font,
                START_X + x_offset,
                START_Y - y_offset,
                SCALE
            )
            gcode.extend(letter_gcode)
            
            # 3. x_offset'u karakterin gerçek genişliği + letter_spacing kadar artır
            x_offset += char_end + LETTER_SPACING
            
            
        
        # Satır sonunda y_offset'u artır
        y_offset += LINE_SPACING
        print(f"  Satır: {line}  \t y_offset: {y_offset:.2f}\n")

    # Son hareketler-gcode sonu
    gcode.append(f"G0 Z{TRAVEL_Z}")
    gcode.append("G0 X0 Y0")
    gcode.append("M84 ; motorları kapat")

    # Dosyaya yaz
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(gcode))

    print("-" * 50)
    print(f"\n✅ G-code oluşturuldu: {OUTPUT_FILE}")
    print(f"📊 Toplam {len(gcode)} satır G-code, {len(text)} karakter işlendi.")
    print()
    print("🎯 Sıradaki adımlar:")
    print("   1. output.gcode dosyasını Cura'ya yükleyin")
    print("   2. Ender 3'ünüzde çıktı alın")
    print("   3. Sonucu kontrol edin, gerekirse LETTER_SPACING veya SCALE ayarlarını değiştirin")

if __name__ == "__main__":
    main()
