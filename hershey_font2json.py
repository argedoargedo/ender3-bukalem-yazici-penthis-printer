#!/usr/bin/env python3

"""
Hershey Fontlarını json dosyasına çevirir
========================================================================
3d yazıcılar için hazır font.
"""

import json
from HersheyFonts import HersheyFonts

def generate_font_json(chars, font_name="cursive", scale=50, output="hershey_font.json"):
    """
    Hershey font'dan json dosyası oluştur
    
    Degişkenler:
        chars (str): İşlenecek olan karakter
        font_name (str): Hershey font : cursive, rowmans, vb
        scale (int): Karakter boyutu
        output (str): Çıktı
    """
    hf = HersheyFonts()
    hf.load_default_font(font_name)
    hf.normalize_rendering(scale)
    
    font_data = {}
    for ch in chars:
        lines = list(hf.lines_for_text(ch))
        if not lines:
            print(f"⚠️ Dikkat: '{ch}' bulunamadı")
            continue
        
        paths = []
        current_path = []
        for i, ((x1, y1), (x2, y2)) in enumerate(lines):
            if i == 0 or (x1, y1) != (current_path[-1][0], current_path[-1][1]):
                if current_path:
                    paths.append(current_path)
                current_path = [[x1, y1], [x2, y2]]
            else:
                current_path.append([x2, y2])
        if current_path:
            paths.append(current_path)
        
        font_data[ch] = paths
    
    with open(output, "w") as f:
        json.dump(font_data, f, indent=2, ensure_ascii=False)
    print(f"✅  {output} dosyasına {len(font_data)} karakter kaydedildi ")

if __name__ == "__main__":
    # İstenilen karakterler. Herşey_font ları türkçe karakter içermiyor. Sonradan eklenmesi gerekiyor.
    # Büyük karakterler + Küçük karakterler + Türkçe(içermiyor) + Sayılar + Özel karakterler
    chars = (
        # Büyük karakterler
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # Küçük karakterler
        "abcdefghijklmnopqrstuvwxyz"
        # Türkçe karakterler
        "ĞğİıÖöÜüÇçŞş"
        # Sayılar
        "0123456789"
        # Özel karakterler
        ".,:;!?\'\"'+-*/=()[]{}<>|@#$%&^\\~`=_"
    )
    generate_font_json(chars, "cursive", scale=100, output="hershey_cursive.json")
    

