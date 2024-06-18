import os

label_dir = 'C:\\Users\\AISW-203-116\\Downloads\\dataset\\train\\labels'

invalid_labels = []

for label_file in os.listdir(label_dir):
    if label_file.endswith('.txt'):
        label_path = os.path.join(label_dir, label_file)
        with open(label_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                try:
                    class_id = int(float(line.split()[0]))
                    if class_id >= 2:
                        invalid_labels.append(label_path)
                        break
                except ValueError as e:
                    print(f"Error processing {label_path}: {e}")
                    invalid_labels.append(label_path)
                    break

if invalid_labels:
    print("Invalid label files found:")
    for label_path in invalid_labels:
        print(label_path)
else:
    print("All labels are valid.")