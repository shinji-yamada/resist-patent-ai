import streamlit as st
from pptx import Presentation
import os

# ページ設定
st.set_page_config(page_title="特許調査ツール", layout="wide")
st.title("🔍 特許調査アプリ（PowerPoint対応）")

# --- ① IPC分類コードのチェックボックス表示 ---
st.header("① IPC分類コードの選択")

ipc_options = {
    "C08F2/00（重合反応）": "C08F2/00",
    "G03F7/027（感光性レジスト）": "G03F7/027",
    "C09D11/00（光学コーティング）": "C09D11/00",
    "C08L33/00（樹脂組成）": "C08L33/00",
}

selected_ipcs = []
st.markdown("調査対象としたいIPC分類を選択してください：")

# 各IPC分類にチェックボックスを用意
for label in ipc_options:
    if st.checkbox(label, value=True):
        selected_ipcs.append(ipc_options[label])

# --- ② PowerPointファイルのアップロード ---
st.header("② PowerPoint資料のアップロード（発明概要）")
uploaded_file = st.file_uploader("📎 発明内容を説明するPowerPointファイル（.pptx）をアップロード", type=["pptx"])

ppt_text = ""
if uploaded_file:
    try:
        prs = Presentation(uploaded_file)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    ppt_text += shape.text + "\n"
        st.success("✅ PowerPointファイルからテキストを抽出しました。")
        st.text_area("📘 抽出されたテキスト", ppt_text, height=200)
    except Exception as e:
        st.error(f"❌ PowerPointの読み込み中にエラーが発生しました: {e}")

# --- ③ 実行ボタンと後続処理（仮） ---
st.header("③ 類似特許の取得")

if st.button("🔍 類似特許を探す（※現在はダミー動作）"):
    if not uploaded_file:
        st.warning("⚠️ まずPowerPointファイルをアップロードしてください。")
    elif not selected_ipcs:
        st.warning("⚠️ IPC分類コードを1つ以上選択してください。")
    else:
        st.info("🔧 概念検索機能とGoogle Patents検索は現在開発中です。")
        st.write("✅ 選択されたIPCコード:", ", ".join(selected_ipcs))
        st.write("📝 抽出されたテキストの一部:", ppt_text[:300] + "..." if len(ppt_text) > 300 else ppt_text)
