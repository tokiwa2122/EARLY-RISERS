# Open AI API連携

import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()  
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


matched_hobbies = ["アーチェリー", "ジョギング", "ピアノ"]

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

    return response.choices[0].message.content.strip()

st.set_page_config(page_title="おすすめ趣味", layout="centered")
st.title("🎯 あなたにおすすめの趣味3選（AIが理由も提案！）")

for i, hobby in enumerate(matched_hobbies, 1):
    with st.spinner(f"{hobby} の理由を生成中..."):
        reason = generate_reason(hobby)
    with st.container():
        st.subheader(f"✅ おすすめ {i}：{hobby}")
        st.write(reason)
        st.markdown("---")
