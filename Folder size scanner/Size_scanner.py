import os


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

def scan_large_folders(drive_path, size_threshold_gb):
    size_threshold_bytes = size_threshold_gb * (1024 ** 3)
    large_folders = []

    def scan_directory(path):
        folder_size = get_folder_size(path)
        if folder_size > size_threshold_bytes:
            large_folders.append((path, folder_size / (1024 ** 3)))
        
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    scan_directory(entry.path)

    scan_directory(drive_path)
    return large_folders


if __name__ == "__main__":
    print("Path example 'C:\\'")
    while True:    
        try:
            path = input("Enter the path to scan: ")
            if not os.path.exists(path):
                raise ValueError("Invalid path or folder doesn't exist. Please enter a valid path.")
            break
        except ValueError as e:
            print(e)
            continue

    while True:
        try:
            size = float(input("Enter the size threshold in GB: "))
            if size < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid number. Please enter a valid number.")
            continue

    print("Scanning for large folders...")
    large_folders = scan_large_folders(path, size)
    if large_folders:
        for folder, size in large_folders:
            print(f"Folder: {folder}, Size: {size:.2f} GB")
    else:
        print(f"No folders larger than {size} GB found.")
    print("Done.")