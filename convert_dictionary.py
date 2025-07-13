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
        '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_eating_1.json'
    ]

    for file_path in dictionary_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for jp_word, entry_value in data.items():
                    if jp_word not in combined_data:
                        combined_data[jp_word] = []

                    # entry_value がリストの場合（複数のドイツ語訳がある場合）
                    if isinstance(entry_value, list):
                        for new_entry in entry_value:
                            # 既存のエントリと重複しないかチェック
                            is_duplicate = False
                            for existing_entry in combined_data[jp_word]:
                                if existing_entry.get('de') == new_entry.get('de') and \
                                   existing_entry.get('gender') == new_entry.get('gender'):
                                    is_duplicate = True
                                    break
                            if not is_duplicate:
                                combined_data[jp_word].append(new_entry)
                    # entry_value が辞書の場合（単一のドイツ語訳がある場合）
                    elif isinstance(entry_value, dict):
                        new_entry = entry_value
                        is_duplicate = False
                        for existing_entry in combined_data[jp_word]:
                            if existing_entry.get('de') == new_entry.get('de') and \
                               existing_entry.get('gender') == new_entry.get('gender'):
                                is_duplicate = True
                                break
                        if not is_duplicate:
                            combined_data[jp_word].append(new_entry)
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
