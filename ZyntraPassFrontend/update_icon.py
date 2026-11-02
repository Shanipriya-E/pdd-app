import os
from PIL import Image
import shutil

image_path = r"C:\Users\Vishnu\.gemini\antigravity\brain\2c398681-ac77-476d-9c61-f9c67cbe8d1a\.user_uploaded\media_1787586943739.png"
res_dir = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main\res"

sizes = {
    'mipmap-mdpi': 48,
    'mipmap-hdpi': 72,
    'mipmap-xhdpi': 96,
    'mipmap-xxhdpi': 144,
    'mipmap-xxxhdpi': 192
}

try:
    img = Image.open(image_path)
    
    # 1. Generate PNGs and delete WebPs
    for folder, size in sizes.items():
        folder_path = os.path.join(res_dir, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        # Resize image
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Save as ic_launcher.png and ic_launcher_round.png
        resized.save(os.path.join(folder_path, 'ic_launcher.png'), 'PNG')
        resized.save(os.path.join(folder_path, 'ic_launcher_round.png'), 'PNG')
        
        # Remove old webp if they exist
        webp1 = os.path.join(folder_path, 'ic_launcher.webp')
        webp2 = os.path.join(folder_path, 'ic_launcher_round.webp')
        if os.path.exists(webp1): os.remove(webp1)
        if os.path.exists(webp2): os.remove(webp2)

    # 2. Delete mipmap-anydpi so it falls back to the generated PNGs
    anydpi = os.path.join(res_dir, 'mipmap-anydpi')
    if os.path.exists(anydpi):
        shutil.rmtree(anydpi)

    print("Icons successfully updated!")

except Exception as e:
    print(f"Error: {e}")
