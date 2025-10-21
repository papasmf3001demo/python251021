import os
import shutil

DOWNLOADS = r"C:\Users\student\Downloads"

TARGET_MAP = {
    "images": {".jpg", ".jpeg"},
    "data": {".csv", ".xlsx"},
    "docs": {".txt", ".doc", ".pdf"},
    "archive": {".zip"},
}

def ensure_dirs(base, names):
    for name in names:
        os.makedirs(os.path.join(base, name), exist_ok=True)

def unique_path(path):
    base, ext = os.path.splitext(path)
    counter = 1
    new_path = path
    while os.path.exists(new_path):
        new_path = f"{base} ({counter}){ext}"
        counter += 1
    return new_path

def move_files(src):
    ensure_dirs(src, TARGET_MAP.keys())
    moved = []
    errors = []
    for entry in os.scandir(src):
        if not entry.is_file():
            continue
        ext = os.path.splitext(entry.name)[1].lower()
        target_sub = None
        for sub, exts in TARGET_MAP.items():
            if ext in exts:
                target_sub = sub
                break
        if not target_sub:
            continue
        dest_dir = os.path.join(src, target_sub)
        dest_path = os.path.join(dest_dir, entry.name)
        dest_path = unique_path(dest_path)
        try:
            shutil.move(entry.path, dest_path)
            moved.append((entry.name, os.path.relpath(dest_path, src)))
        except Exception as e:
            errors.append((entry.name, str(e)))
    return moved, errors

if __name__ == "__main__":
    moved, errors = move_files(DOWNLOADS)
    print(f"이동된 파일: {len(moved)}")
    for src_name, dest_rel in moved:
        print(f"  {src_name} -> {dest_rel}")
    if errors:
        print(f"오류: {len(errors)}")
        for name, err in errors:
            print(f"  {name}: {err}")