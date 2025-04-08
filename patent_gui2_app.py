import streamlit as st
from duckduckgo_search import DDGS

st.set_page_config(page_title="先行特許調査AI", layout="wide")
st.title("🔍 半導体フォトレジスト特化型・レジスト特許調査AI")

st.markdown("発明の概要を入力してください。Google Patents から類似特許を探します。")

query = st.text_area("📘 発明の概要を入力", height=200, placeholder="例：半導体フォトレジストの製造方法であって、貧溶媒として・・・")

if st.button("🔍 調査開始"):
    with st.spinner("Google Patentsから類似特許を検索中..."):
        with DDGS() as ddgs:
            results = list(ddgs.text(f"{query} site:patents.google.com", max_results=5))

    for idx, r in enumerate(results):
        st.subheader(f"🧾 類似特許 {idx+1}")
        st.markdown(f"🔗 [タイトル]({r['href']}): {r['title']}")
        st.markdown(f"📌 概要: {r['body']}")
