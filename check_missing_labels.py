import os

json_dir = 'C:/Users/AISW-203-116/Downloads/dataset/json'
label_dir = 'C:/Users/AISW-203-116/Downloads/dataset/train/labels'

json_files = {os.path.splitext(f)[0] for f in os.listdir(json_dir) if f.endswith('.json')}
label_files = {os.path.splitext(f)[0] for f in os.listdir(label_dir) if f.endswith('.txt')}

missing_labels = json_files - label_files

if missing_labels:
    print("Missing label files for the following JSON files:")
    for missing_label in missing_labels:
        print(f"{missing_label}.json")
else:
    print("All JSON files have corresponding label files.")
