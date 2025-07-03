import json
import requests
from bs4 import BeautifulSoup
import time

# 辞書ファイルのパス
file_path = '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary.json'

# 既存の辞書を読み込む
with open(file_path, 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

def get_wiktionary_declension(word_de):
    url = f"https://en.wiktionary.org/wiki/{word_de}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        forms = {}
        plural = {}

        # ドイツ語のセクションを探す
        german_section_header = soup.find('span', id='German')
        if not german_section_header:
            return {}, {}
        
        # ドイツ語のセクションから、格変化テーブルを探す
        # Wiktionaryのテーブルは 'inflection-table' または 'inflection-table-noun' などのクラスを持つことが多い
        # または、h3/h4タグの次のテーブルを探す
        table = None
        current_element = german_section_header.find_parent()
        while current_element:
            table = current_element.find_next_sibling('table', class_=[lambda x: x and 'inflection-table' in x])
            if table: # テーブルが見つかったらループを抜ける
                break
            current_element = current_element.find_next_sibling()

        if not table:
            # 別の方法でテーブルを探す（例: ページ全体から探す）
            table = soup.find('table', class_=[lambda x: x and 'inflection-table' in x])

        if not table:
            return {}, {}

        # テーブルから格変化情報を抽出
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['th', 'td'])
            if len(cells) < 3: # 少なくとも格、単数、複数が必要
                continue
            
            case_text = cells[0].get_text(strip=True)
            
            # 格の特定
            case_map = {
                'Nominative': 'nominative',
                'Genitive': 'genitive',
                'Dative': 'dative',
                'Accusative': 'accusative'
            }
            case = case_map.get(case_text)
            
            if case:
                # 単数形 (通常は2列目)
                singular_form = cells[2].get_text(strip=True) if len(cells) > 2 else '-'
                # 複数形 (通常は5列目)
                plural_form = cells[5].get_text(strip=True) if len(cells) > 5 else '-'
                
                forms[case] = singular_form
                plural[case] = plural_form

        return forms, plural
    except requests.exceptions.RequestException as e:
        print(f"Wiktionaryからのデータ取得エラー ({word_de}): {e}")
        return {}, {}

# 処理する単語のリストを準備
words_to_process = []
for jp_key, data in dictionary.items():
    # formsまたはpluralが空のものを対象とする
    if not data['forms'] or not data['plural']:
        words_to_process.append((jp_key, data['de']))

print(f"{len(words_to_process)}個の単語の格変化と複数形を処理します。")

# 処理の実行
processed_count = 0
for jp_key, word_de in words_to_process:
    print(f"Processing declension for: {word_de} (JP Key: {jp_key})")

    forms, plural = get_wiktionary_declension(word_de)
    time.sleep(1) # サーバーへの負荷軽減

    # 辞書を更新
    dictionary[jp_key]['forms'] = forms
    dictionary[jp_key]['plural'] = plural

    processed_count += 1
    if processed_count % 10 == 0:
        print(f"{processed_count}個の単語の格変化を処理しました。dictionary.jsonを保存中...")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, indent=2, ensure_ascii=False)

# 最終保存
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, indent=2, ensure_ascii=False)

print("すべての単語の格変化と複数形の処理が完了しました。")
