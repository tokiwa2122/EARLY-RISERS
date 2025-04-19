import requests
from bs4 import BeautifulSoup
import pandas as pd

hobby_category_name_all_list = []
hobby_name_all_list = []

import requests
BASE_URL = 'https://shumi.info'
REQUEST_URL_CATEGORY = 'https://shumi.info/category'
res_category = requests.get(REQUEST_URL_CATEGORY)

soup_category = BeautifulSoup(res_category.text, 'html.parser')


hobby_category = soup_category.select('ul.list.cf li a')

print(len(hobby_category))

#スクレイピングの参照範囲をaタグに狭めている
hobby_category

#全ページ分の趣味名を蓄積するためのリストを空で用意する
hobby_category_url_all_list = []
hobby_data = []

import re

#スクレイピングの実行
for a_tag in hobby_category: #hobby_categoryの範囲内でできることを次の段落で記述
    url_category = a_tag.get("href") #aタグに狭めた参照範囲からhrefを取り出す
    res_category_name = requests.get(BASE_URL+url_category) #各趣味カテゴリのURLをループ生成
    soup_hobby_category_url = BeautifulSoup(res_category_name.text, 'html.parser') #parse処理
    hobby_category_url_all_list.append(soup_hobby_category_url) #parse済URLを追加してリストに格納
    hobby_names = soup_hobby_category_url.select('a p.ttl') #各趣味カテゴリに属する名前を抽出
    for tag in hobby_names: #hobby_namesの範囲内でできることを次の段落で記述
        url_hobby = tag.find_parent("a").get("href")
        res_hobby_name = requests.get(BASE_URL+url_hobby) 
        soup_hobby_name = BeautifulSoup(res_hobby_name.text, 'html.parser') #parse処理

        p_tags = soup_hobby_name.find_all("p")
        hobby_description = " ".join(p.text.strip() for p in p_tags if p.text.strip())
        hobby_description = re.sub(r"^あなたの人生を変える趣味、きっと見つかる。\s*文字サイズ：\s*", "", hobby_description)
        hobby_data.append({
            'カテゴリ': a_tag.text.strip(),
            '趣味名': tag.text.strip(),
            "趣味詳細説明文": hobby_description
        })
        

import pandas as pd
df = pd.DataFrame(hobby_data)

#趣味名の重複が多いので、削除する
# ステップ① 空白除去
df["趣味名"] = df["趣味名"].astype(str).str.strip()

# ステップ② 重複削除して独立コピー作成
df_unique = df.drop_duplicates(subset="趣味名", keep="first").copy()

# ステップ③ 「アーチェリー」だけを完全一致で抽出（空白・改行など除去して比較）
cleaned_hobby_names = df_unique["趣味名"].astype(str).str.replace(r"\s+", "", regex=True).str.strip()
archery_indexes = df_unique[cleaned_hobby_names == "アーチェリー"].index

# ステップ④ 最初の1件を残して他は削除
df_unique2 = df_unique.drop(index=archery_indexes[1:]).reset_index(drop=True)

#マッチング作業
#まずpowershellでこちらを実行する　pip install sentence-transformers

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
os.environ["HF_HOME"] = "./hf_cache"  # 別フォルダにキャッシュを保存

# データの読み込み
df_unique2 = pd.read_csv("hobby_data_unique2.csv")  # ←適宜ファイル名に置き換えてください
df_unique2["趣味詳細説明文"] = df_unique2["趣味詳細説明文"].fillna("")

# 日本語対応のマルチリンガルモデル（安定版）
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 類義語リストを辞書形式で定義
synonym_dict = {
    "体幹を鍛える": ["体幹", "バランス", "姿勢強化"],
    "姿勢がよくなる": ["美姿勢", "姿勢改善", "背筋が伸びる"],
    "代謝が上がる": ["ダイエット", "脂肪燃焼", "体温上昇"],

    "リラックス": ["ストレス解消", "安らぐ", "落ち着く"],
    "癒される": ["癒し", "心が和む", "ほっこりする"],
    "ワクワクする": ["興奮", "テンションが上がる", "ドキドキ"],
    "集中する": ["没頭", "ゾーンに入る", "集中力が増す"],
    "非日常感を味わう": ["刺激的", "冒険", "日常から離れる"],

    "表現力が身につく": ["アウトプット力", "感情表現", "自己表現"],
    "観察力が鍛える": ["洞察", "気づき", "注意深くなる"],
    "創造力を育てる": ["クリエイティブ", "想像力", "アイデア"],
    "達成感を味わう": ["やりがい", "目標達成", "満足感"],
    "文化に触れる": ["伝統文化", "アート", "知的好奇心"],
    "自然と関わる": ["自然体験", "屋外", "アウトドア"],

    "一人で楽しむ": ["ソロ", "マイペース", "自分の時間"],
    "仲間と楽しむ": ["グループ", "交流", "コミュニティ"],

    "初期費用が安い": ["低コスト", "安価", "コスパがいい"],
    "自宅でできる": ["家でできる", "在宅", "家時間"],
    "気軽に始められる": ["初心者OK", "始めやすい", "敷居が低い"]
}

user_input = ["あなたは趣味を通じて体幹を鍛える、非日常感を味わう、達成感を味わうことを望んでいます。またそれは仲間と楽しむことができ、なおかつ自宅でできるものであると、より満足感が高まります。"]

# ユーザーの回答に含まれるキーワード
user_keywords = ["体幹を鍛える", "非日常感を味わう", "達成感を味わう", "仲間と楽しむ", "自宅でできる"]

# マッチングのルールを作成（ユーザーが回答したキーワードをカバーしている数が多いほどポイントが高い、更にすべてカバーしている場合にマッチしたキーワードの数が多ければボーナスポイント追加）
def hybrid_keyword_score(user_input, user_keywords, synonym_dict):
    covered_count = 0
    total_match_count = 0

    for keyword in user_keywords:
        synonyms = [keyword] + synonym_dict.get(keyword, [])
        match_count = 0
        for syn in synonyms:
            if syn in user_input:
                match_count +=1
        if match_count > 0:
            covered_count += 1
            total_match_count += match_count
        else:
            total_match_count += 0

    base_score = covered_count

    if covered_count == len(user_keywords):
        bonus_score = (total_match_count - covered_count) * 0.1
    else:
        bonus_score = 0
    
    return base_score + bonus_score

#上記で作成したマッチングルールを適用して"hybrid_score"としてカラム追加する
df_unique2["hybrid_score"] = df_unique2["趣味詳細説明文"].astype(str).apply(
    lambda x: hybrid_keyword_score(user_input, user_keywords, synonym_dict)
)

#"hybrid_score"を降順に並べたうえで、TOP3を抽出する。（追加しました）
def get_top_n_hobby_name(df,column_name, n=3):
    return df.sort_values(by=column_name, ascending=False).head(n)

top_hobbies = get_top_n_hobby_name(df_unique2, "hybrid_score", n=3)

print(top_hobbies[["趣味名","hybrid_score"]])

# これはYukaによるバックエンド追加です！
print("バックエンドの処理を追加しました。")