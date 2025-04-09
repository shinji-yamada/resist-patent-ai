import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.parse

st.set_page_config(page_title="半導体リソグラフィーレジスト特化型先行技術調査AI", layout="wide")
st.title("🔍 半導体リソグラフィーレジスト特化型先行技術調査AI")

st.markdown("発明の概要を入力してください。該当しそうな特許を Wikidata 経由で取得します。")

query = st.text_area("📘 発明の概要", height=200, placeholder="例：フォトリソグラフィ用の新しいレジスト材料...")

if st.button("🔍 特許調査を実行"):
    if not query.strip():
        st.warning("発明の概要を入力してください。")
    else:
        st.info("Wikidataから特許情報を取得中...")

        # SPARQLクエリをWikidataに送信
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery(f"""
        SELECT ?item ?itemLabel ?publicationDate ?url WHERE {{
          ?item wdt:P31 wd:Q253623 .
          ?item rdfs:label ?itemLabel .
          FILTER (LANG(?itemLabel) = "en") .
          FILTER(CONTAINS(LCASE(?itemLabel), "{query.lower()}")) .
          OPTIONAL {{ ?item wdt:P577 ?publicationDate. }}
          OPTIONAL {{ ?item wdt:P856 ?url. }}
        }}
        LIMIT 10
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        bindings = results["results"]["bindings"]

        if not bindings:
            st.error("該当する特許が見つかりませんでした。キーワードを変えてみてください。")
        else:
            for res in bindings:
                label = res["itemLabel"]["value"]
                link = res["item"]["value"]
                pub_date = res.get("publicationDate", {}).get("value", "不明")
                gpat_url = res.get("url", {}).get("value", "[Google Patentsで探す](https://patents.google.com)")

                st.subheader(f"🧾 {label}")
                st.markdown(f"🔗 Wikidata: [{link}]({link})")
                st.markdown(f"📅 出願日: {pub_date}")
                st.markdown(f"🌐 関連リンク: {gpat_url}")



