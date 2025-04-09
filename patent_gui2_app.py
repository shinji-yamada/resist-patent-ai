import streamlit as st
from duckduckgo_search import DDGS

# Streamlitページ設定
st.set_page_config(page_title="半導体リソグラフィーレジスト特化型先行特許調査AI", layout="wide")

st.title("🔍 半導体リソグラフィーレジスト特化型先行特許調査AI")
st.markdown("発明の概要を入力し、調査したい技術分野（IPC分類）を選んでください。")

# 発明概要入力欄
query = st.text_area("📘 発明の概要を入力", height=200, placeholder="例：EUVリソグラフィー向けの高解像度ネガ型レジスト...")

# IPC選択肢（必要に応じて追加可）
ipc_options = {
    "G03F 7/00": "感光性材料全般",
    "G03F 7/027": "ポジ型・ネガ型の感光性レジスト組成物",
    "G03F 7/20": "リソグラフィー用感光性材料とその応用",
    "C08F 2/00": "重合による高分子化（レジスト材料の基盤）",
    "C08L 33/00": "感光性樹脂組成物",
}

st.markdown("🎯 **関連するIPC分類を選択してください（複数選択可）**")

# 複数選択チェックボックス
selected_ipcs = []
for code, desc in ipc_options.items():
    if st.checkbox(f"{code} - {desc}", value=True):
        selected_ipcs.append(code)

# 検索ボタン
if st.button("🔍 調査開始"):
    if not query:
        st.warning("発明の概要を入力してください。")
    elif not selected_ipcs:
        st.warning("最低1つのIPC分類を選んでください。")
    else:
        # IPCコードを検索文に組み込む
        ipc_filter = " ".join([f'"{ipc}"' for ipc in selected_ipcs])
        full_query = f"{query} {ipc_filter} site:patents.google.com"

        with st.spinner("Google Patentsから類似特許を検索中..."):
            with DDGS() as ddgs:
                results = list(ddgs.text(full_query, max_results=5))

        if results:
            for idx, r in enumerate(results):
                st.subheader(f"🧾 類似特許 {idx+1}")
                st.markdown(f"🔗 [タイトル]({r['href']}): {r['title']}")
                st.markdown(f"📌 概要: {r['body']}")
        else:
            st.info("類似特許が見つかりませんでした。検索語を変更してみてください。")
