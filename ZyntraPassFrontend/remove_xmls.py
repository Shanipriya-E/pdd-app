import os

res_dir = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main\res"
anydpi = os.path.join(res_dir, 'mipmap-anydpi')

for f in ['ic_launcher.xml', 'ic_launcher_round.xml']:
    file_path = os.path.join(anydpi, f)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed {f}")
