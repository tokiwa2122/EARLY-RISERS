# 趣味探しアプリ

import streamlit as st


st.set_page_config(page_title="趣味探しアプリ", layout="centered")
st.title("東京都民の趣味探しアプリ")
st.title("人生楽しまないと！")

if "show_form" not in st.session_state:
    st.session_state["show_form"] = False

# スタートボタン（初期状態のみ）
if not st.session_state["show_form"]:
    st.button("趣味探しスタート", on_click=lambda: st.session_state.update(show_form=True))

# ボタン押下後の表示
if st.session_state["show_form"]:
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


# じぴちゃんのプロンプト生成（修正版）

if st.session_state.get("show_form"):

   if st.button("おすすめ趣味を探す"):
    # 設問1〜5の値（ここではすでに上で取得済みの変数をそのまま使う）
    # age, gender, address, social_style, start_preference ← 既存変数

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
あなたは趣味を通じて「{', '.join(body_goals)}」ことや「{', '.join(mind_goals)}」を望んでいます。
また、それは{social_text}、なおかつ{start_pref_text}、より「{', '.join(skill_goals)}」を高めたいです。
このような希望を叶える新たな趣味探しのキーワードを抽出してください。
        """.strip()

        st.markdown("#### 🔍 趣味探しプロンプト（じぴちゃん生成）")
        st.code(prompt, language="markdown")

