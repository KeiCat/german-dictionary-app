import json

file_path = '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_combined.json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(len(data))
except FileNotFoundError:
    print(f"Error: {file_path} not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON from {file_path}: {e}")