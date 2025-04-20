# merge test
#searchとっきー

# 趣味探しアプリ

import streamlit as st

if "show_form" not in st.session_state:
    st.session_state["show_form"] = False
if "show_result" not in st.session_state:
    st.session_state["show_result"] = False

st.set_page_config(page_title="趣味探しアプリ", layout="centered")
st.title("東京都民の趣味探しアプリ")
st.title("人生楽しまないと！")

if "show_form" not in st.session_state:
    st.session_state["show_form"] = False

# スタートボタン（初期状態のみ）
if not st.session_state["show_form"]:
    st.button("趣味探しスタート", on_click=lambda: st.session_state.update(show_form=True))

# ボタン押下後の表示
if st.session_state["show_form"] and not st.session_state["show_result"]:
    st.subheader("あなたに関する情報を教えてください！")

    # 設問1
    st.markdown("### ① 年代を教えてください")
    age = st.radio(
        label="年代",
        options=["30代未満", "30代", "40代", "50代", "60代以上"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # 設問2
    st.markdown("### ② 性別を教えてください")
    gender = st.radio(
        label="性別",
        options=["男", "女", "その他", "無回答"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # 設問3
    st.markdown("### ③ 居住地を教えてください")
    address = st.radio(
        label="居住地",
        options=["東京都"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # 設問4
    st.markdown("### ④ 趣味を通じた人とのかかわり方について教えてください")
    social_style = st.radio(
        label="人とのかかわり方",
        options=["一人で楽しむ", "仲間と楽しむ"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # 設問5
    st.markdown("### ⑤ 趣味の始め方について、最も優先度が高いものを教えてください")
    start_preference = st.radio(
        label="始めやすさの優先",
        options=["初期費用が安い", "自宅でできる", "気軽に始められる"],
        horizontal=True,
        label_visibility="collapsed"
    )


    # 設問6
    st.markdown("#### 次に、趣味を通じてご自身がなっていたい状態を教えてください（複数選択可）")

    st.markdown("### ⑥ 求める身体・運動機能は？（複数選択可）")

    cols = st.columns(3)
    with cols[0]:
       goal1 = st.checkbox("体幹を鍛える", key="goal1")
    with cols[1]:
       goal2 = st.checkbox("姿勢がよくなる", key="goal2")
    with cols[2]:
       goal3 = st.checkbox("代謝が上がる", key="goal3")


    # 設問7
    st.markdown("### ⑦ 求めるこころ・感情の変化は？（複数選択可）")
    
    cols = st.columns(5)
    with cols[0]:
       goal1 = st.checkbox("リラックス", key="goal4")
    with cols[1]:
       goal2 = st.checkbox("癒される", key="goal5")
    with cols[2]:
       goal3 = st.checkbox("ワクワクする", key="goal6")
    with cols[3]:
       goal4 = st.checkbox("集中する", key="goal7")
    with cols[4]:
       goal5 = st.checkbox("非日常を味わう", key="goal8")



    # 設問8 
    st.markdown("### ⑧ 得たいスキルは？（複数選択可）")
    
    cols = st.columns(6)
    with cols[0]:
       goal1 = st.checkbox("表現力", key="goal9")
    with cols[1]:
       goal2 = st.checkbox("観察力", key="goal10")
    with cols[2]:
       goal3 = st.checkbox("想像力", key="goal11")
    with cols[3]:
       goal4 = st.checkbox("達成感", key="goal12")
    with cols[4]:
       goal5 = st.checkbox("文化力", key="goal13")
    with cols[5]:
       goal6 = st.checkbox("自然力", key="goal14")


# じぴちゃんのプロンプト生成（修正版）　とっきー

if st.session_state.get("show_form"):

   # if st.button("おすすめ趣味を探す"):

    # 設問1〜5の値（ここではすでに上で取得済みの変数をそのまま使う）
    # age, gender, address, social_style, start_preference ← 既存変数

  if st.session_state.get("show_form"):  # ← ここはフォーム表示のトリガー
    age = st.session_state.get("age")         # ← ここで各値を取得
    gender = st.session_state.get("gender")
    address = st.session_state.get("address")
    social_style = st.session_state.get("social_style")
    start_preference = st.session_state.get("start_preference")

    # 設問6〜8（複数選択）
    body_goals = [label for label, key in {
        "体幹を鍛える": "goal1",
        "姿勢がよくなる": "goal2",
        "代謝が上がる": "goal3"
    }.items() if st.session_state.get(key)]

    mind_goals = [label for label, key in {
        "リラックス": "goal4",
        "癒される": "goal5",
        "ワクワクする": "goal6",
        "集中する": "goal7",
        "非日常を味わう": "goal8"
    }.items() if st.session_state.get(key)]

    skill_goals = [label for label, key in {
        "表現力": "goal9",
        "観察力": "goal10",
        "想像力": "goal11",
        "達成感": "goal12",
        "文化力": "goal13",
        "自然力": "goal14"
    }.items() if st.session_state.get(key)]

    if not all([age, gender, address, social_style, start_preference, body_goals, mind_goals, skill_goals]):
        st.error("未回答の設問があります。すべての項目に回答してください。")
    else:
        social_text = f"「{social_style}」ことができ"
        start_pref_text = f"「{start_preference}」もので"

        prompt = f"""
          趣味を通じて「{', '.join(body_goals)}」ことや「{', '.join(mind_goals)}」を望んでいます。
          また、それは{social_text}、なおかつ{start_pref_text}、より「{', '.join(skill_goals)}」を高めたいです。
        """.strip()

        # st.markdown("#### 🔍 趣味探しプロンプト（じぴちゃん生成）")
        # st.code(prompt, language="markdown")

# app ゆかちん

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

# prompt がセッションにあれば使う
if "prompt" in st.session_state:
    user_input = st.session_state["prompt"]
else:
    user_input = ""  # またはエラーメッセージでもOK


# ユーザーの回答に含まれるキーワード
user_keywords = ["goal1","goal2","goal3","goal4","goal5","goal6","goal7","goal8","goal9","goal10","goal11","goal12","goal13","goal14",]

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
# if st.session_state.get("show_result"):
    # "hybrid_score" を一時的なスコアとして生成

if st.session_state.get("show_form"):

 if st.button("おすすめ趣味を探す", key="search_button_top", on_click=lambda: st.session_state.update(show_result=True)):

    df_unique2["趣味詳細説明文"] = df_unique2["趣味詳細説明文"].fillna("")
    df_unique2["hybrid_score"] = df_unique2["趣味詳細説明文"].astype(str).apply(
        lambda x: hybrid_keyword_score(user_input, user_keywords, synonym_dict)
    )

    # "hybrid_score" を降順に並べて、TOP3を抽出する
    def get_top_n_hobby_name(df, column_name, n=3):
        return df.sort_values(by=column_name, ascending=False).head(n)

    top_hobbies = get_top_n_hobby_name(df_unique2, "hybrid_score", n=3)

    TOP1 = top_hobbies.iloc[0]["趣味名"]
    TOP2 = top_hobbies.iloc[1]["趣味名"]
    TOP3 = top_hobbies.iloc[2]["趣味名"]

    st.session_state["matched_hobbies"] = [TOP1, TOP2, TOP3]
    st.session_state["show_result"] = True

    # Open AI API連携　とっきー

import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()  
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    
    # 正しい関数定義
def generate_reason(hobby):
     prompt = f"""
     あなたは趣味提案のプロフェッショナルです。
     以下の趣味について、ユーザーに「なるほど！」と思わせるような理由を200文字程度で説明してください。

    趣味: {hobby}
    理由:
    """
     response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたは親しみやすく、簡潔で納得感のある説明が得意なアドバイザーです。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )
     return prompt,response.choices[0].message.content.strip()

if st.session_state.get("show_result"):
    st.markdown("### 🔍 あなたにおすすめの趣味3選")
     
    for i, hobby in enumerate(st.session_state["matched_hobbies"], 1):
       with st.spinner(f"{hobby} の理由を生成中..."):
            prompt, reason = generate_reason(hobby)
       with st.container():
           st.subheader(f"✅ おすすめ {i}：{hobby}")
           st.write(reason)
           st.markdown("---")

     # return prompt,response.choices[0].message.content.strip()


# print(top_hobbies[["趣味名","hybrid_score"]])

# Open AI API連携　とっきー

#import streamlit as st
#import openai
#import os
#from dotenv import load_dotenv

#load_dotenv()  
#from openai import OpenAI
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 正しいマッチング趣味リスト
# matched_hobbies =  [TOP1, TOP2, TOP3]

# 正しい関数定義
#def generate_reason(hobby):
   # prompt = f"""
#あなたは趣味提案のプロフェッショナルです。
#以下の趣味について、ユーザーに「なるほど！」と思わせるような理由を200文字程度で説明してください。

#趣味: {hobby}
#理由:
#"""
   # response = client.chat.completions.create(
    #    model="gpt-4",
     #   messages=[
      #      {"role": "system", "content": "あなたは親しみやすく、簡潔で納得感のある説明が得意なアドバイザーです。"},
       #     {"role": "user", "content": prompt}
        #],
       # temperature=0.7,
       # max_tokens=300
   # )

   # return prompt,response.choices[0].message.content.strip()

# 表示部分はこのままでOK！
# for i, hobby in enumerate(matched_hobbies, 1):
    #with st.spinner(f"{hobby} の理由を生成中..."):
        # prompt, reason = generate_reason(hobby)
     #with st.container():
       # st.subheader(f"✅ おすすめ {i}：{hobby}")
       # st.write(reason)
       # st.markdown("---")

