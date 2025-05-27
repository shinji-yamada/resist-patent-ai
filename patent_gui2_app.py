import streamlit as st
from duckduckgo_search import DDGS

st.set_page_config(page_title="半導体フォトレジスト特化型特許調査ツール", layout="wide")
st.title("🔍 半導体フォトレジスト特化型特許調査ツール")

st.markdown("発明の概要と出願人を選択してください。Google Patents から類似特許を検索し、簡易要約を表示します。")

# 出願人リスト
applicant_list = [
    "日本曹達", "DuPont", "東邦化学", "信越化学", "JSR", "住友化学", "PCAS-Canada",
    "Miwon", "CGPM", "三菱ケミカル", "ダイセル", "群栄化学工業", "セントラル硝子",
    "大阪有機", "上海B&C", "ダイトーケミックス", "東洋合成", "TOK", "メルク",
    "FFEM", "Dongjin", "SKMP", "Kempur", "Red Avenue", "NATA", "富士フィルム"
]

# レ点チェック（初期状態で全選択）
st.markdown("### ✅ 出願人を選択してください（すべて選択済）")
selected_applicants = []
cols = st.columns(3)
for i, applicant in enumerate(applicant_list):
    col = cols[i % 3]
    if col.checkbox(applicant, value=True):
        selected_applicants.append(applicant)

# 発明概要
query = st.text_area("📘 発明の概要を入力", height=200, placeholder="例：新規感光性樹脂を含むフォトレジスト...")

# 要約関数
def simple_summary(text):
    lines = text.split('。')
    for line in lines:
        if "本発明" in line or "提供する" in line or "課題" in line:
            return line.strip() + "。"
    return lines[0].strip() + "。" if lines else ""

# 調査実行
if st.button("🔍 調査開始"):
    if not selected_applicants:
        st.warning("出願人を1件以上選択してください。")
    elif not query.strip():
        st.warning("発明の概要を入力してください。")
    else:
        st.info(f"{len(selected_applicants)}件の出願人に対して検索を行います。")

        for applicant in selected_applicants:
            search_query = f"{query} {applicant} site:patents.google.com"
            st.subheader(f"🧾 出願人: {applicant}")

            results = []

            try:
                with st.spinner(f"{applicant} の特許をDuckDuckGoで検索中..."):
                    with DDGS() as ddgs:
                        results = list(ddgs.text(search_query, max_results=2))
            except Exception as e:
                st.error(f"❌ DuckDuckGo 検索に失敗しました（{applicant}）: {str(e)}")
                google_link = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                st.markdown(f"🔗 代替: [Googleで検索]({google_link})")

            if results:
                for idx, r in enumerate(results):
                    st.markdown(f"**{idx+1}. [{r['title']}]({r['href']})**")
                    st.markdown(f"📌 概要: {r['body']}")
                    st.markdown(f"🧠 簡易要約: {simple_summary(r['body'])}")
