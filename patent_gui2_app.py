import streamlit as st
import urllib.parse

# タイトルとレイアウトの設定
st.set_page_config(page_title="半導体リソグラフィーレジスト特化型先行技術調査AI", layout="wide")

# メインタイトル
st.title("🔍 半導体リソグラフィーレジスト特化型先行技術調査AI")

st.markdown("発明の概要を入力し、Google Patents で関連特許を検索します。")

# 発明概要の入力
query = st.text_area("📘 発明の概要", height=200, placeholder="例：フォトリソグラフィ用の新しいレジスト材料...")

# IPC分類の選択肢（必要に応じて追加・編集可）
ipc_all = ["G03F7/027", "G03F7/30", "C08F2/00", "C08L79/00", "C09D11/10"]
selected_ipcs = []

st.markdown("### 📁 関連するIPC分類を選択")
select_all = st.checkbox("すべて選択")

if select_all:
    selected_ipcs = ipc_all
else:
    for ipc in ipc_all:
        if st.checkbox(ipc):
            selected_ipcs.append(ipc)

# 検索ボタンの処理
if st.button("🔍 Google Patentsで検索"):
    if not query.strip():
        st.warning("発明の概要を入力してください。")
    else:
        # IPCクエリ組み立て
        ipc_query = " ".join([f'"{ipc}"' for ipc in selected_ipcs]) if selected_ipcs else ""
        full_query = f"{query} {ipc_query} site:patents.google.com"
        encoded_query = urllib.parse.quote_plus(full_query)
        search_url = f"https://www.google.com/search?q={encoded_query}"

        st.markdown(f"🔗 [🔍 Google Patentsで検索]({search_url})")
        st.success("検索リンクが生成されました！クリックして特許調査を開始してください。")


