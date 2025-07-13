import json

def convert_dictionary():
    combined_data = {}

    # List of dictionary files to combine
    dictionary_files = [
        '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_A1_1.json',
        '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_A1_2.json',
        '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_A2_1.json',
        '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_B1_1.json',
        '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_B2_1.json',
        '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_C1_1.json',
        '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_C2_1.json',
        '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_additional.json',
        '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_daily_life_1.json',
        '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_eating_1.json' # これを追加
    ]

    for file_path in dictionary_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for jp_word, entry_value in data.items():
                    # エントリの値がリストの場合（dictionary_A2_1.jsonなど）
                    if isinstance(entry_value, list):
                        if jp_word in combined_data:
                            combined_data[jp_word].extend(entry_value)
                        else:
                            combined_data[jp_word] = entry_value
                    # エントリの値が辞書の場合（dictionary_A1_1.json, dictionary_A1_2.jsonなど）
                    elif isinstance(entry_value, dict):
                        if jp_word in combined_data:
                            combined_data[jp_word].append(entry_value)
                        else:
                            combined_data[jp_word] = [entry_value]
                    else:
                        print(f"Warning: Unexpected data type for {jp_word} in {file_path}. Skipping.")

        except FileNotFoundError:
            print(f"{file_path} not found. Skipping.")
        except json.JSONDecodeError as e:
            print(f"Error decoding {file_path}: {e}")
            return

    # Save combined dictionary to dictionary_combined.json
    try:
        with open('/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_combined.json', 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
        print("Successfully converted and saved dictionary_combined.json")
    except IOError as e:
        print(f"Error writing dictionary_combined.json: {e}")

if __name__ == '__main__':
    convert_dictionary()