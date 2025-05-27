import streamlit as st
from duckduckgo_search import DDGS

st.set_page_config(page_title="半導体フォトレジスト特化型特許調査ツール", layout="wide")
st.title("🔍 半導体フォトレジスト特化型特許調査ツール")

st.markdown("発明の概要を入力してください。Google Patents から類似特許を検索し、関連性の高い出願人上位5社のみ表示します。")

# 出願人リスト
applicant_list = [
    "日本曹達", "DuPont", "東邦化学", "信越化学", "JSR", "住友化学", "PCAS-Canada",
    "Miwon", "CGPM", "三菱ケミカル", "ダイセル", "群栄化学工業", "セントラル硝子",
    "大阪有機", "上海B&C", "ダイトーケミックス", "東洋合成", "TOK", "メルク",
    "FFEM", "Dongjin", "SKMP", "Kempur", "Red Avenue", "NATA", "富士フィルム"
]

# 発明概要
query = st.text_area("📘 発明の概要を入力", height=200, placeholder="例：新規感光性樹脂を含むフォトレジストにより、分解能と感度を両立...")

def simple_summary(text):
    lines = text.split('。')
    for line in lines:
        if "本発明" in line or "提供する" in line or "課題" in line:
            return line.strip() + "。"
    return lines[0].strip() + "。" if lines else ""

if st.button("🔍 調査開始"):
    if not query.strip():
        st.warning("発明の概要を入力してください。")
    else:
        st.info("DuckDuckGoで検索を行い、最も関連性の高い出願人5社を表示します。")
        candidates = []

        with DDGS() as ddgs:
            for applicant in applicant_list:
                search_query = f"{query} {applicant} site:patents.google.com"
                try:
                    with st.spinner(f"🔎 {applicant} を検索中..."):
                        results = list(ddgs.text(search_query, max_results=1))
                        if results:
                            candidates.append((applicant, results[0]))  # タイトルや概要も含めて保持
                except Exception as e:
                    st.warning(f"❌ {applicant}: 検索失敗 - {str(e)}")

        if not candidates:
            st.error("いずれの出願人でも関連特許が見つかりませんでした。")
        else:
            st.success(f"{len(candidates)}件の出願人で結果が見つかりました。上位5件を表示します。")
            top_5 = candidates[:5]  # 検索成功順の先頭5件を表示

            for idx, (applicant, r) in enumerate(top_5):
                st.subheader(f"{idx+1}. 出願人: {applicant}")
                st.markdown(f"🔗 [タイトル]({r['href']}): {r['title']}")
                st.markdown(f"📌 概要: {r['body']}")
                st.markdown(f"🧠 簡易要約: {simple_summary(r['body'])}")
