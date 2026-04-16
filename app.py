import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import urllib.parse
import streamlit.components.v1 as components

# --- 1. データセットの定義 ---
# 「マップ用検索語」と「日本の研究.com検索用キーワード」を追加
data = [
    {"大学名": "京都大学", "区分": "国立", "立地": "京都市左京区", "マップ検索": "京都大学 吉田キャンパス", "科研費規模": 100, "科研費の質": "S・A多数 (超大型)", "研究": 5, "臨床": 5, "教育": 4, "データ統計": 5, "資格実学": 3},
    {"大学名": "大阪大学", "区分": "国立", "立地": "大阪府吹田市", "マップ検索": "大阪大学 吹田キャンパス", "科研費規模": 95, "科研費の質": "S・A多数 (超大型)", "研究": 5, "臨床": 4, "教育": 4, "データ統計": 5, "資格実学": 3},
    {"大学名": "大阪公立大学", "区分": "公立", "立地": "大阪市住吉区", "マップ検索": "大阪公立大学 杉本キャンパス", "科研費規模": 75, "科研費の質": "A・B・C (中大型)", "研究": 4, "臨床": 4, "教育": 3, "データ統計": 4, "資格実学": 3},
    {"大学名": "京都府立大学", "区分": "公立", "立地": "京都市左京区", "マップ検索": "京都府立大学 下鴨キャンパス", "科研費規模": 40, "科研費の質": "B・C主体 (小型)", "研究": 3, "臨床": 3, "教育": 3, "データ統計": 2, "資格実学": 3},
    {"大学名": "立命館大学", "区分": "私立", "立地": "大阪府茨木市", "マップ検索": "立命館大学 大阪いばらきキャンパス", "年間学費(万円)": 140, "科研費規模": 85, "科研費の質": "A・B多数 (中大型)", "研究": 4, "臨床": 4, "教育": 4, "データ統計": 5, "資格実学": 4},
    {"大学名": "同志社大学", "区分": "私立", "立地": "京都府京田辺市", "マップ検索": "同志社大学 京田辺キャンパス", "年間学費(万円)": 130, "科研費規模": 80, "科研費の質": "A・B多数 (中大型)", "研究": 4, "臨床": 4, "教育": 3, "データ統計": 4, "資格実学": 5},
    {"大学名": "関西学院大学", "区分": "私立", "立地": "兵庫県西宮市", "マップ検索": "関西学院大学 西宮上ヶ原キャンパス", "年間学費(万円)": 130, "科研費規模": 80, "科研費の質": "A・B多数 (中大型)", "研究": 5, "臨床": 4, "教育": 4, "データ統計": 4, "資格実学": 4},
    {"大学名": "京都女子大学", "区分": "私立", "立地": "京都市東山区", "マップ検索": "京都女子大学", "年間学費(万円)": 135, "科研費規模": 50, "科研費の質": "B・C主体 (実学・臨床系)", "研究": 3, "臨床": 5, "教育": 5, "データ統計": 2, "資格実学": 5},
    {"大学名": "同志社女子大学", "区分": "私立", "立地": "京都府京田辺市", "マップ検索": "同志社女子大学 京田辺キャンパス", "年間学費(万円)": 135, "科研費規模": 40, "科研費の質": "C主体 (実学・臨床系)", "研究": 2, "臨床": 4, "教育": 4, "データ統計": 2, "資格実学": 4},
    {"大学名": "龍谷大学", "区分": "私立", "立地": "京都市伏見区", "マップ検索": "龍谷大学 深草キャンパス", "年間学費(万円)": 125, "科研費規模": 55, "科研費の質": "B・C主体 (実学・臨床系)", "研究": 3, "臨床": 4, "教育": 4, "データ統計": 3, "資格実学": 4},
]

# 欠損値（国立の学費など）を補完
for d in data:
    if "年間学費(万円)" not in d:
        d["年間学費(万円)"] = 54  # 国公立の標準額

df = pd.DataFrame(data)
categories = ['研究', '臨床', '教育', 'データ統計', '資格実学']

# --- 2. Streamlit UI構築 ---
st.set_page_config(page_title="関西圏 心理学大学セレクター", layout="wide")
st.title("関西圏 心理学系大学 比較ダッシュボード")

# サイドバー: フィルター
st.sidebar.header("絞り込み条件🔍")
selected_type = st.sidebar.multiselect("設立区分", ["国立", "公立", "私立"], default=["公立", "私立"])
selected_univs = st.sidebar.multiselect("比較する大学を選択", df["大学名"].tolist(), default=["京都女子大学", "立命館大学", "関西学院大学"])

filtered_df = df[df["区分"].isin(selected_type)]

# --- 3. グラフ描画セクション ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("学費vs科研費規模")
    st.markdown("##### ざっくりいうと、大学の「費用対効果」がわかります。")
    st.info("""
    **科研費（科学研究費助成事業）とは？** 国から研究者に配分される、「研究のための競争的資金」です。  
    ざっくりと以下のような規模感に分かれています。
    * **特別推進・基盤S / A:** 2千万〜数億円（超大型・巨大な実験設備など）
    * **基盤B:** 5百万〜2000万円（中型・本格的な実験や調査）
    * **基盤C・萌芽:** 〜500万円（小型・面接調査やデータ分析など）
    
    ※心理学（特に臨床系）は高額な機械を使わないため、基盤Cが多くなる傾向があります。
    """)
    fig_scatter = px.scatter(
        filtered_df, x="年間学費(万円)", y="科研費規模", color="区分", text="大学名",
        size_max=60, hover_data=["科研費の質"]
    )
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.subheader("分野別レーダーチャート")
    if selected_univs:
        fig_radar = go.Figure()
        for univ in selected_univs:
            univ_data = df[df["大学名"] == univ].iloc[0]
            fig_radar.add_trace(go.Scatterpolar(
                r=[univ_data[cat] for cat in categories],
                theta=categories, fill='toself', name=univ
            ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), height=400)
        st.plotly_chart(fig_radar, use_container_width=True)

# --- 4. 選択した大学の詳細情報（マップ＆科研費リンク） ---
st.markdown("---")
st.subheader("選択した大学の詳細情報（キャンパス立地 ＆ 科研費データ）")

if selected_univs:
    # 選択された大学の数に合わせてカラムを作成
    cols = st.columns(len(selected_univs))
    
    for i, univ in enumerate(selected_univs):
        with cols[i]:
            univ_data = df[df["大学名"] == univ].iloc[0]
            st.markdown(f"### {univ}")
            st.write(f"**立地:** {univ_data['立地']}")
            st.write(f"**科研費の質:** {univ_data['科研費の質']}")
            
            # --- 日本の研究.com へのリンク生成 ---
            # 「大学名 + 心理」で検索するURLを動的に生成
            search_query = urllib.parse.quote(f"{univ} 心理")
            kenkyu_url = f"https://research-er.jp/researchers/search?q={search_query}"
            st.markdown(f"🔗 **[日本の研究.com で『{univ} 心理』の科研費・研究者を調べる]({kenkyu_url})**")
            
            # --- Google Map の iframe 埋め込み ---
            map_query = urllib.parse.quote(univ_data["マップ検索"])
            map_html = f"""
            <iframe 
                width="100%" 
                height="250" 
                frameborder="0" 
                style="border:0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" 
                src="https://maps.google.com/maps?q={map_query}&t=m&z=14&output=embed" 
                allowfullscreen>
            </iframe>
            """
            components.html(map_html, height=260)
else:
    st.info("サイドバーから大学を選択すると、ここに地図と詳細が表示されます。")
