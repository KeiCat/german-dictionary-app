import json
import requests
from bs4 import BeautifulSoup
import time

# 辞書ファイルのパス
file_path = '/Users/yamada-kei/Desktop/ドイツ語辞書/dictionary.json'

# 既存の辞書を読み込む
with open(file_path, 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

def get_weblio_data(word_de):
    url = f"https://ejje.weblio.jp/content/{word_de}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # HTTPエラーがあれば例外を発生させる
        soup = BeautifulSoup(response.text, 'html.parser')

        jp_translation = ""
        pronunciation = ""

        # 日本語訳の取得
        # Weblioの構造は複雑なため、いくつかのパターンを試す
        # 例: <div class="content-wrapper"> <div class="content-explanation"> ... </div> </div>
        content_explanation = soup.find('div', class_='content-explanation')
        if content_explanation:
            # 最初の日本語訳を取得
            jp_translation_tag = content_explanation.find('p', class_='content-explanation-text')
            if jp_translation_tag:
                jp_translation = jp_translation_tag.get_text(strip=True).split('[')[0].strip()

        # カタカナ発音の取得
        # 例: <span class="pronunciation-text">[ˈapzɛndɐ]</span>
        pronunciation_tag = soup.find('span', class_='pronunciation-text')
        if pronunciation_tag:
            pronunciation = pronunciation_tag.get_text(strip=True).replace('[', '').replace(']', '')

        return jp_translation, pronunciation
    except requests.exceptions.RequestException as e:
        print(f"Weblioからのデータ取得エラー ({word_de}): {e}")
        return "", ""

def get_wiktionary_declension(word_de, gender_article):
    # WiktionaryのURLは単語によって異なる場合があるため、まずは一般的な形を試す
    url = f"https://en.wiktionary.org/wiki/{word_de}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        forms = {}
        plural = {}

        # ドイツ語のセクションを探す
        german_section = soup.find('span', id='German')
        if not german_section:
            return {}, {}
        
        # ドイツ語のセクションから名詞の格変化テーブルを探す
        # テーブルの構造はWiktionaryのバージョンによって変わる可能性がある
        table = german_section.find_next('table', class_='inflection-table')
        if not table:
            # 別のテーブルクラスを試すなど、より堅牢な方法が必要になる場合がある
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
    # 日本語訳がドイツ語単語と同じ、または発音が空のものを対象とする
    if data['pronunciation'] == "" or data['de'] == jp_key:
        words_to_process.append((jp_key, data['de'], data['gender']))

print(f"{len(words_to_process)}個の単語を処理します。")

# 処理の実行
processed_count = 0
for jp_key_original, word_de, gender_article in words_to_process:
    print(f"Processing: {word_de} (Original JP Key: {jp_key_original})")

    # Weblioから日本語訳と発音を取得
    jp_translation, pronunciation = get_weblio_data(word_de)
    time.sleep(1) # サーバーへの負荷軽減

    # Wiktionaryから格変化と複数形を取得
    forms, plural = get_wiktionary_declension(word_de, gender_article)
    time.sleep(1) # サーバーへの負荷軽減

    # 辞書を更新
    # 新しい日本語訳があれば、キーを更新
    if jp_translation and jp_translation != jp_key_original:
        # 古いエントリを削除
        del dictionary[jp_key_original]
        # 新しい日本語訳をキーとして追加
        dictionary[jp_translation] = {
            "de": word_de,
            "gender": gender_article,
            "pronunciation": pronunciation,
            "forms": forms,
            "plural": plural
        }
    else:
        # 日本語訳が変わらない場合は既存のエントリを更新
        dictionary[jp_key_original]['pronunciation'] = pronunciation
        dictionary[jp_key_original]['forms'] = forms
        dictionary[jp_key_original]['plural'] = plural

    processed_count += 1
    if processed_count % 10 == 0:
        print(f"{processed_count}個の単語を処理しました。dictionary.jsonを保存中...")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, indent=2, ensure_ascii=False)

# 最終保存
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, indent=2, ensure_ascii=False)

print("すべての単語の処理が完了しました。")
