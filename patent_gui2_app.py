import streamlit as st
from duckduckgo_search import DDGS

st.set_page_config(page_title="半導体フォトレジスト特化型特許調査ツール", layout="wide")
st.title("🔍 半導体フォトレジスト特化型特許調査ツール")

st.markdown("発明の概要と出願人を選択してください。Google Patents から類似特許を検索し、関連性の高い上位5社のみ表示します。")

# 出願人リスト
applicant_list = [
    "日本曹達", "DuPont", "東邦化学", "信越化学", "JSR", "住友化学", "PCAS-Canada",
    "Miwon", "CGPM", "三菱ケミカル", "ダイセル", "群栄化学工業", "セントラル硝子",
    "大阪有機", "上海B&C", "ダイトーケミックス", "東洋合成", "TOK", "メルク",
    "FFEM", "Dongjin", "SKMP", "Kempur", "Red Avenue", "NATA", "富士フィルム"
]

# レ点式の出願人選択（デフォルト全選択）
st.markdown("### ✅ 出願人を選択してください（すべて選択済）")
selected_applicants = []
cols = st.columns(3)
for i, applicant in enumerate(applicant_list):
    col = cols[i % 3]
    if col.checkbox(applicant, value=True):
        selected_applicants.append(applicant)

# 発明概要入力
query = st.text_area("📘 発明の概要を入力", height=200, placeholder="例：新規感光性樹脂を含むフォトレジストにより、分解能と感度を両立...")

# 簡易要約
def simple_summary(text):
    lines = text.split('。')
    for line in lines:
        if "本発明" in line or "提供する" in line or "課題" in line:
            return line.strip() + "。"
    return lines[0].strip() + "。" if lines else ""

# 調査ボタン
if st.button("🔍 調査開始"):
    if not selected_applicants:
        st.warning("出願人を1件以上チェックしてください。")
    elif not query.strip():
        st.warning("発明の概要を入力してください。")
    else:
        st.info(f"{len(selected_applicants)}社の中から、関連度の高い上位5社を表示します。")
        results_with_hits = []

        with DDGS() as ddgs:
            for applicant in selected_applicants:
                search_query = f"{query} {applicant} site:patents.google.com"
                try:
                    with st.spinner(f"🔎 {applicant} を検索中..."):
                        results = list(ddgs.text(search_query, max_results=1))
                        if results:
                            results_with_hits.append((applicant, results[0]))
                except Exception as e:
                    st.warning(f"❌ {applicant}: 検索失敗 - {str(e)}")

        if not results_with_hits:
            st.error("類似特許が見つかりませんでした。")
        else:
            top_5 = results_with_hits[:5]  # 成功した中から上位5件（順不同）

            for idx, (applicant, r) in enumerate(top_5):
                st.subheader(f"{idx+1}. 出願人: {applicant}")
                st.markdown(f"🔗 [タイトル]({r['href']}): {r['title']}")
                st.markdown(f"📌 概要: {r['body']}")
                st.markdown(f"🧠 簡易要約: {simple_summary(r['body'])}")
