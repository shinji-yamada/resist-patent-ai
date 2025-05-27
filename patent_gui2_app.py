import streamlit as st
from duckduckgo_search import DDGS
import openai

st.set_page_config(page_title="量子特許AI", layout="wide")

st.title("🔍 半導体フォトレジスト特化型・先行特許調査AI")

st.markdown("発明の概要を入力してください。類似する特許をGoogle Patentsから探して、要約・請求項1を表示します。")

openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("OpenAI API Key", type="password")

query = st.text_area("📘 発明の概要を入力", height=200, placeholder="例：量子演算結果に対して、AIでデコヒーレンス補正を行い、冷却不要の量子コンピューターを構成...")

if st.button("🔍 調査開始"):
    with st.spinner("Google Patentsから類似特許を検索中..."):
        with DDGS() as ddgs:
            results = list(ddgs.text(f"{query} site:patents.google.com", max_results=5))
        
        for idx, r in enumerate(results):
            st.subheader(f"🧾 類似特許 {idx+1}")
            st.markdown(f"🔗 [タイトル]({r['href']}): {r['title']}")
            st.markdown(f"📌 概要: {r['body']}")

            # オプションでGPT要約
            if openai.api_key:
                with st.spinner("OpenAIで要約中..."):
                    gpt_response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "あなたは特許調査員です。以下のテキストから、要約と請求項1のような要点を抽出してください。"},
                            {"role": "user", "content": r['body']}
                        ]
                    )
                    st.markdown(f"🧠 GPT要約: {gpt_response.choices[0].message.content}")

