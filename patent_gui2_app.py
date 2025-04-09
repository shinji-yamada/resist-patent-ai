import streamlit as st
import urllib.parse

st.set_page_config(page_title="先行特許調査AI", layout="wide")

st.title("🔍 先行特許調査AI（Google Patents連携）")

st.markdown("発明の概要を入力してください。Google Patents上で直接検索します。")

# 入力欄
query = st.text_area("📘 発明の概要", height=200, placeholder="例：フォトリソグラフィ用の新しいレジスト材料...")

# IPC分類指定
ipc_options = ["G03F7/027", "G03F7/30", "C08F2/00", "全部"]
ipc_selection = st.multiselect("📁 関連するIPC分類を選択", ipc_options, default=["全部"])

# 検索ボタン
if st.button("🔍 Google Patentsで検索"):
    if not query.strip():
        st.warning("発明の概要を入力してください。")
    else:
        # IPC絞り込みの追加
        ipc_query = ""
        if "全部" not in ipc_selection:
            ipc_query = " ".join([f'"{ipc}"' for ipc in ipc_selection])
        
        full_query = f"{query} {ipc_query} site:patents.google.com"
        encoded_query = urllib.parse.quote_plus(full_query)

        search_url = f"https://www.google.com/search?q={encoded_query}"

        st.markdown(f"🔗 [Google Patentsで検索を実行する]({search_url})")
        st.success("🔍 検索リンクが生成されました。クリックしてGoogle Patentsを開いてください。")

