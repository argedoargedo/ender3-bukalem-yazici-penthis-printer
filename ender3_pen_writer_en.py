#!/usr/bin/env python3
"""
Ender 3 / Pen Plotter – Single Line Text Drawing with Hershey Fonts
========================================================================

This software converts single-line vector data from Hershey fonts into G-code.
It is specifically designed for pen plotters such as an Ender 3.

Features:
- Uses JSON format font vectors (Hershey)
- Dynamically calculates each character's endpoint (solves spacing issues with J, j, K, k)
- Supports Turkish characters (Ğ,ğ,İ,ı,Ö,ö,Ü,ü,Ç,ç,Ş,ş)
- Fine-tuning with SCALE, LETTER_SPACING, DRAW_Z parameters

Usage:
1. Choose a font file (FONT_FILE variable)
2. Write your text into TEXT_FILE
3. Run the script: python yaz.py
4. Load the generated output.gcode into Cura and print on your Ender 3

Requirements:
- Python 3.7+
- A JSON file containing Hershey font vectors

Example: python yaz.py

Speed conversion (SPEED - mm/min):
600  → 10 mm/s
1200 → 20 mm/s
1800 → 30 mm/s
2400 → 40 mm/s
"""

import json
# ============================================================================
# CONFIGURATION SETTINGS - User should modify this section
# ============================================================================

FONT_FILE = "hershey_cursive.json"      # Font file to use
TEXT_FILE = "text.txt"                  # Input text file
OUTPUT_FILE = "output.gcode"            # Output G-code file

START_X = 10                            # Starting X coordinate (mm)
START_Y = 220                           # Starting Y coordinate (mm)

DRAW_Z = 2                              # Pen down height (touching paper)
TRAVEL_Z = 7                            # Pen up height (moving freely)

SCALE = 10                              # Font size (1 = 100% scale)
LETTER_SPACING = .25 * SCALE / 10       # Extra spacing between letters (rowmans: 2, cursive: 0.25)
LINE_SPACING = 13 * SCALE / 10          # Line spacing
SCALE = SCALE / 100                     # Convert to internal scale

SPEED = 1000                            # Drawing speed (mm/min)

# ============================================================================
# FUNCTIONS - User should not modify below
# ============================================================================

def load_font():
    """Loads the JSON font file and returns it as a dictionary."""
    with open(FONT_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_text():
    """Loads the text file and returns its content."""
    with open(TEXT_FILE, encoding="utf-8") as f:
        return f.read()


def get_char_endpoint(font, scale=1.0):
    """
    Calculates the rightmost X coordinate (endpoint) of a character.
    
    Args:
        scale: Scaling factor
    
    Returns:
        max_x: Rightmost X coordinate of the character
    """
    
    max_x = -float('inf')
    
    for stroke in font:
        for x, y in stroke:
            sx = x * scale
            if sx > max_x:
                max_x = sx
    
    # If the font is empty or consists of a single point
    if max_x == -float('inf'):
        return 0
    
    return max_x


def generate_letter_gcode(font, x_offset, y_offset, scale):
    """
    Converts a single character into G-code commands.
    
    Args:
        font: Character vector data
        x_offset: X axis starting point
        y_offset: Y axis starting point
        scale: Scaling factor
    
    Returns:
        list: G-code command lines
    """

    lines = []
    
    for stroke in font:
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

    # Character finished, lift pen
    lines.append(f"G0 Z{TRAVEL_Z}")
    
    return lines


def main():
    """Main program: read text, load font, generate and save G-code."""
    
    # Load files
    text = load_text()
    fonts = load_font()

    # G-code header
    gcode = [
        "G21 ; Millimeter units",
        "G90 ; Absolute positioning",
        "G28 ; Home all axes",
        f"G0 Z{TRAVEL_Z} ; Lift pen"
    ]

    y_offset = 0
    lines = text.splitlines()
 
    print(f"📝 Processing: {len(lines)} lines, total {len(text)} characters")
    print("-" * 50)

    for line in lines:
        
        x_offset = 0
 
        for char in line:
            
            # Space character
            if char == " ":
                x_offset += 15 * SCALE + LETTER_SPACING
                continue

            # Tab character 
            if char == "\t":
                x_offset += 180 * SCALE + LETTER_SPACING
                continue
                
            # Skip if character not found in font
            if char not in fonts:
                print(f"  Warning: '{char}' not found in font (skipping)")
                continue
            
            font = fonts[char]
            
            # 1. Get character endpoint
            char_end = get_char_endpoint(font, SCALE)
            
            # 2. Draw character
            letter_gcode = generate_letter_gcode(
                font,
                START_X + x_offset,
                START_Y - y_offset,
                SCALE
            )
            gcode.extend(letter_gcode)
            
            # 3. Update x_offset for next character
            x_offset += char_end + LETTER_SPACING
        
        # End of line, update y_offset
        y_offset += LINE_SPACING
        print(f"  Line: {line}  \t y_offset: {y_offset:.2f}\n")

    # G-code footer
    gcode.append(f"G0 Z{TRAVEL_Z}")
    gcode.append("G0 X0 Y0")
    gcode.append("M84 ; Disable motors")

    # Write to file
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(gcode))

    print("-" * 50)
    print(f"\n✅ G-code generated: {OUTPUT_FILE}")
    print(f"📊 Total {len(gcode)} lines of G-code, {len(text)} characters processed.")
    print()
    print("🎯 Next steps:")
    print("   1. Load output.gcode into Cura")
    print("   2. Print on your Ender 3")
    print("   3. Check the result and adjust LETTER_SPACING or SCALE if needed")

if __name__ == "__main__":
    main()
