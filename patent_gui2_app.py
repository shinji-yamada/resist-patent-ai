import streamlit as st
from duckduckgo_search import DDGS
import re

st.set_page_config(page_title="半導体フォトレジスト特化型特許調査ツール", layout="wide")

st.title("🔍 半導体フォトレジスト特化型特許調査ツール")
st.markdown("発明の概要を入力してください。Google Patentsから類似特許を検索し、簡易要約を表示します。")

query = st.text_area("📘 発明の概要を入力", height=200, placeholder="例：量子演算結果に対して、AIでデコヒーレンス補正を行い、冷却不要の量子コンピューターを構成...")

def simple_summary(text):
    lines = text.split('。')
    for line in lines:
        if "本発明" in line or "提供する" in line or "課題" in line:
            return line.strip() + "。"
    return lines[0].strip() + "。"

if st.button("🔍 調査開始"):
    with st.spinner("Google Patentsから類似特許を検索中..."):
        with DDGS() as ddgs:
            results = list(ddgs.text(f"{query} site:patents.google.com", max_results=5))

    for idx, r in enumerate(results):
        st.subheader(f"🧾 類似特許 {idx+1}")
        st.markdown(f"🔗 [タイトル]({r['href']}): {r['title']}")
        st.markdown(f"📌 概要: {r['body']}")

        summary = simple_summary(r['body'])
        st.markdown(f"🧠 簡易要約（ルールベース）: {summary}")
