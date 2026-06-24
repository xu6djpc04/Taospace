import os
import shutil
import unicodedata

def normalize_path(p):
    return unicodedata.normalize('NFC', p)

def main():
    src_dir = normalize_path(r"C:\Users\kevin\Desktop\Taospace\Taofiles")
    dest_dir = normalize_path(r"C:\Users\kevin\Desktop\Taospace\Taofiles\班務組\策劃組會議")
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    copied_files = []
    
    for root, dirs, files in os.walk(src_dir):
        # Skip the destination directory to avoid copying from itself
        if dest_dir in normalize_path(root):
            continue
            
        for f in files:
            norm_f = normalize_path(f)
            # Only copy files containing "策劃" or "策畫"
            if "策劃" in norm_f or "策畫" in norm_f:
                src_path = os.path.join(root, f)
                
                # Check for duplication
                dest_path = os.path.join(dest_dir, f)
                base, ext = os.path.splitext(f)
                counter = 1
                while os.path.exists(dest_path):
                    new_name = f"{base}_舊版備份{counter}{ext}"
                    dest_path = os.path.join(dest_dir, new_name)
                    counter += 1
                
                shutil.copy2(src_path, dest_path)
                copied_files.append(f)
                print(f"Copied: {f} -> {os.path.basename(dest_path)}")

    print(f"Total files copied: {len(copied_files)}")

if __name__ == "__main__":
    main()
