import json

def convert_dictionary():
    combined_data = {}

    # Load dictionary_A1_1.json
    try:
        with open('/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_A1_1.json', 'r', encoding='utf-8') as f:
            data_a1_1 = json.load(f)
            for jp_word, de_data in data_a1_1.items():
                # ここでリストとして初期化
                combined_data[jp_word] = [de_data]
    except FileNotFoundError:
        print("dictionary_A1_1.json not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding dictionary_A1_1.json: {e}")
        return

    # Load dictionary_A1_2.json
    try:
        with open('/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary_A1_2.json', 'r', encoding='utf-8') as f:
            data_a1_2 = json.load(f)
            for jp_word, de_data in data_a1_2.items():
                if jp_word in combined_data:
                    # 既存のキーの場合はリストに追加
                    combined_data[jp_word].append(de_data)
                else:
                    # 新しいキーの場合はリストとして初期化
                    combined_data[jp_word] = [de_data]
    except FileNotFoundError:
        print("dictionary_A1_2.json not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding dictionary_A1_2.json: {e}")
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