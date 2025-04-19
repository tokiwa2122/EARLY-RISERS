#必要なライブラリのインポート
import pandas as pd
import sqlite3

#データベースファイルへの接続 / SQLコマンドの実行 / クローズ
conn = sqlite3.connect("hobby_data_cleaned.db")
df = pd.read_sql_query("SELECT * FROM hobbies", conn)
conn.close()

# ここで df_unique2 を再定義、dfはPython（メモリ上）のPandas DataFrameとなっている
df_unique2 = df.copy()

#マッチング作業
#まずpowershellでこちらを実行する　pip install sentence-transformers

#from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
os.environ["HF_HOME"] = "./hf_cache"  # 別フォルダにキャッシュを保存

# 日本語対応のマルチリンガルモデル（安定版）
#model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

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

#上記で作成したマッチングルールを適用して"hybrid_score"として一時的なカラムをdfに追加する
df_unique2["趣味詳細説明文"] = df_unique2["趣味詳細説明文"].fillna("")
df_unique2["hybrid_score"] = df_unique2["趣味詳細説明文"].astype(str).apply(
    lambda x: hybrid_keyword_score(user_input, user_keywords, synonym_dict)
)

#"hybrid_score"を降順に並べたうえで、TOP3を抽出する
def get_top_n_hobby_name(df,column_name, n=3):
    return df.sort_values(by=column_name, ascending=False).head(n)

top_hobbies = get_top_n_hobby_name(df_unique2, "hybrid_score", n=3)

print(top_hobbies[["趣味名","hybrid_score"]])