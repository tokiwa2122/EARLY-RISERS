import requests
from bs4 import BeautifulSoup
import pandas as pd

import requests
BASE_URL = 'https://shumi.info'
REQUEST_URL_CATEGORY = 'https://shumi.info/category'
res_category = requests.get(REQUEST_URL_CATEGORY)

soup_category = BeautifulSoup(res_category.text, 'html.parser')

#スクレイピングの参照範囲をaタグに狭めている
hobby_category = soup_category.select('ul.list.cf li a')

#全ページ分の趣味名を蓄積するためのリストを空で用意する
hobby_data = []

#必要なライブラリのインポート
import pandas as pd
import sqlite3
import re
import time

#____________________________________________________________________________
#スクレイピングの実行
for a_tag in hobby_category: #hobby_categoryの範囲内でできることを次の段落で記述
    print(f"カテゴリ取得中: {a_tag.text.strip()}")

    url_category = a_tag.get("href") #aタグに狭めた参照範囲からhrefを取り出す
    res_category_name = requests.get(BASE_URL+url_category, timeout = 5) #各趣味カテゴリのURLをループ生成    
    time.sleep(1)
    soup_hobby_category_url = BeautifulSoup(res_category_name.text, 'html.parser') #parse処理
    hobby_names = soup_hobby_category_url.select('a p.ttl') #各趣味カテゴリに属する名前を抽出
    for tag in hobby_names: #hobby_namesの範囲内でできることを次の段落で記述
        url_hobby = tag.find_parent("a").get("href")
        full_url = BASE_URL + url_hobby
        print(f"  → 趣味ページアクセス中: {full_url}")  # ★どこにアクセスしているか表示

        try:
            res_hobby_name = requests.get(full_url, timeout=5)
            time.sleep(1)
            soup_hobby_name = BeautifulSoup(res_hobby_name.text, 'html.parser')  # parse処理

            p_tags = soup_hobby_name.find_all("p")
            hobby_description = " ".join(p.text.strip() for p in p_tags if p.text.strip())
            hobby_description = re.sub(r"^あなたの人生を変える趣味、きっと見つかる。\s*文字サイズ：\s*", "", hobby_description)
        
            hobby_data.append({
                'カテゴリ': a_tag.text.strip(),
                '趣味名': tag.text.strip(),
                "趣味詳細説明文": hobby_description
            })
            print(f"    ✅ 成功: {tag.text.strip()}")
        
        except Exception as e:
            print(f"    ⚠️ 失敗: {full_url} → {e}")
            continue
#____________________________________________________________________________


#ファイルの出力
df = pd.DataFrame(hobby_data)
df.to_csv("hobby_data.csv", index=False, encoding = "utf-8-sig")

#____________________________________________________________________________
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
#____________________________________________________________________________

# 最後に SQLite に保存
conn = sqlite3.connect("hobby_data_cleaned.db")
df_unique2.to_sql("hobbies", conn, if_exists="replace", index=False)
conn.close()