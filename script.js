document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const resultDiv = document.getElementById('result');
    let dictionary = {};

    // Load the combined dictionary data
    const dictionaryFile = 'dictionary_combined.json';

    fetch(dictionaryFile)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok for ${dictionaryFile}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            dictionary = data;
            console.log("Combined dictionary loaded successfully.");
        })
        .catch(error => {
            console.error('Error loading combined dictionary:', error);
            resultDiv.innerHTML = `<p>辞書ファイルの読み込みに失敗しました。ローカルサーバーが起動しているか確認してください。</p>`;
        });

    const searchWord = () => {
        const jp = searchInput.value.trim();
        if (!jp) {
            resultDiv.innerHTML = "";
            return;
        }

        let foundEntries = [];
        // 日本語をキーの一部として辞書を検索
        for (const jp_key in dictionary) {
            if (jp_key.includes(jp)) {
                dictionary[jp_key].forEach(de_entry => {
                    foundEntries.push({
                        jp_word: jp_key, // 検索にヒットした日本語のキー
                        de_entry: de_entry // そのキーに紐付くドイツ語エントリ
                    });
                });
            }
        }

        if (foundEntries.length === 0) {
            resultDiv.innerHTML = `<p>「${jp}」は見つかりませんでした。</p>`;
            return;
        }

        let html = ``;

        foundEntries.forEach((item, index) => {
            const { jp_word, de_entry } = item; // 日本語のキーとドイツ語エントリを取得
            const { de, gender, pronunciation, forms, plural } = de_entry;

            const genderMap = {
                "der": "男性",
                "die": "女性",
                "das": "中性"
            };

            html += `
              <div class="word-entry">
                <p class="word-translation"><strong>${jp_word}</strong> → ${de}</p>
                <p class="word-details">[${pronunciation}] (${genderMap[gender]})</p>
                <div class="table-responsive">
                  <table>
                    <thead>
                      <tr><th>格</th><th>単数</th><th>複数</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>主格</td><td>${forms.nominative || '-'}</td><td>${plural.nominative || '-'}</td></tr>
                      <tr><td>属格</td><td>${forms.genitive || '-'}</td><td>${plural.genitive || '-'}</td></tr>
                      <tr><td>与格</td><td>${forms.dative || '-'}</td><td>${plural.dative || '-'}</td></tr>
                      <tr><td>対格</td><td>${forms.accusative || '-'}</td><td>${plural.accusative || '-'}</td></tr>
                    </tbody>
                  </table>
                </div>
              </div>
            `;
        });

        resultDiv.innerHTML = html;
    };

    searchButton.addEventListener('click', searchWord);

    searchInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            searchWord();
        }
    });
});