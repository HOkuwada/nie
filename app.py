import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import urllib.parse
import streamlit.components.v1 as components

# --- 1. データセットの定義 ---
# 「募集要項URL」を単一の文字列から、入試方式ごとの辞書（dict）に変更しました。
# 後ほど、奥和田さんが実際のリサーチ結果に合わせてURL部分を書き換えてください。
data = [
    {
        "大学名": "京都大学",
        "学部学科名": "教育学部 教育科学科 / 文学部 人文学科 / 総合人間学部",
        "区分": "国立",
        "立地": "京都市左京区",
        "マップ検索": "京都大学 吉田キャンパス",
        "科研費規模": 100,
        "科研費の質": "S・A多数（超大型・世界レベル）",
        "研究": 5, "臨床": 5, "教育": 4, "データ統計": 5, "資格実学": 3,
        "入試形式": "一般選抜（前期），特色入試（AO）",
        "科目数": "共通テスト: 5教科7科目 / 二次試験: 3〜4科目",
        "入試対策": "共通テストは9割近くが必要。二次試験は記述量が非常に多く，深い思考力と論述力が求められる。特色の場合においても共通テストは必須であり，文学部では84％，教育学部では80％を超えなければ足きりとなる。総人は宇宙人が行くところ。",
        "募集要項": {
            "一般選抜": "https://www.kyoto-u.ac.jp/ja/admissions/undergrad/requirements",
            "特色入試": "https://www.kyoto-u.ac.jp/ja/admissions/tokusyoku/student-recruitment"
        }
    },
    {
        "大学名": "大阪大学",
        "学部学科名": "人間科学部",
        "区分": "国立",
        "立地": "大阪府吹田市",
        "マップ検索": "大阪大学 吹田キャンパス",
        "科研費規模": 95,
        "科研費の質": "S・A多数（超大型・実験系に強い）",
        "研究": 5, "臨床": 4, "教育": 4, "データ統計": 5, "資格実学": 3,
        "入試形式": "一般選抜（前期），総合型選抜",
        "科目数": "共通テスト: 5教科7科目 / 二次試験: 3科目",
        "入試対策": "人間科学部は文理融合型。共通テストの配点も高いため，全教科で穴を作らないことが重要。総合型選抜においても共通テストは必須であり，75％以上取らなければ足きりとなる。",
        "募集要項": {
            "一般選抜": "https://www.osaka-u.ac.jp/ja/admissions/faculty/general/2026",
            "総合型選抜": "https://www.nyusi.icho.osaka-u.ac.jp/requirement/human-sciences"
        }
    },
    {
        "大学名": "奈良女子大学",
        "学部学科名": "文学部 人間科学科（心理学コース）",
        "区分": "国立",
        "立地": "奈良県奈良市",
        "マップ検索": "奈良女子大学",
        "科研費規模": 85,
        "科研費の質": "A・B多数（国立女子大の最高峰）",
        "研究": 5, "臨床": 5, "教育": 4, "データ統計": 4, "資格実学": 4,
        "入試形式": "一般選抜（前期・後期），総合型選抜",
        "科目数": "共通テスト: 5教科6〜7科目 / 二次試験: 2科目",
        "入試対策": "女子大No.2。大阪公立大ととんとんか少し下ぐらいなだけで，かなり難しい。",
        "募集要項": {
            "一般選抜": "https://www.nara-wu.ac.jp/nyusi/nyusi2_a.html",
            "総合型選抜": "https://www.nara-wu.ac.jp/nyusi/qnyusi/download/index.html"
        }
    },
    {
        "大学名": "和歌山大学",
        "学部学科名": "教育学部（心理学専攻）",
        "区分": "国立",
        "立地": "和歌山県和歌山市",
        "マップ検索": "和歌山大学",
        "科研費規模": 50,
        "科研費の質": "B・C主体（教育心理・発達重視）",
        "研究": 3, "臨床": 3, "教育": 5, "データ統計": 3, "資格実学": 4,
        "入試形式": "一般選抜（前期），学校推薦型選抜",
        "科目数": "共通テスト: 5〜6教科 / 二次試験: 1〜2科目",
        "入試対策": "教育学部に属するため，学校心理や発達心理に強い。国公立としては共通テストのボーダーが比較的狙いやすい。",
        "募集要項": {
            "一般選抜": "https://www.wakayama-u.ac.jp/admission/faculty/invitation/",
            "学校推薦型選抜": "https://www.wakayama-u.ac.jp/admission/faculty/invitation/"
        }
    },
    {
        "大学名": "大阪公立大学",
        "学部学科名": "文学部 人文学科 / 生活科学部 人間福祉学科 / 現代システム科学域 心理学類",
        "区分": "公立",
        "立地": "大阪市住吉区",
        "マップ検索": "大阪公立大学 杉本キャンパス",
        "科研費規模": 75,
        "科研費の質": "A・B・Cバランス型",
        "研究": 4, "臨床": 4, "教育": 3, "データ統計": 4, "資格実学": 3,
        "入試形式": "一般選抜（前期・中期），学校推薦型選抜",
        "科目数": "共通テスト: 5教科 / 二次試験: 1〜2科目",
        "入試対策": "中期日程は倍率が非常に高くなる。学校推薦は評定平均が高いと有利に進められるが，共通テストの受験が必須。",
        "募集要項": {
            "一般選抜": "https://www.omu.ac.jp/admissions/ug/exam_info/general/#boshuyoukou",
            "学校推薦型選抜": "https://www.omu.ac.jp/admissions/ug/exam_info/special/recommend/"
        }
    },
    {
        "大学名": "京都府立大学",
        "学部学科名": "社会科学部 福祉社会学科",
        "区分": "公立",
        "立地": "京都市左京区",
        "マップ検索": "京都府立大学 下鴨キャンパス",
        "科研費規模": 40,
        "科研費の質": "B・C主体（地域密着・少人数）",
        "研究": 3, "臨床": 3, "教育": 3, "データ統計": 2, "資格実学": 3,
        "入試形式": "一般選抜（前期・後期），学校推薦型選抜",
        "科目数": "共通テスト: 5教科 / 二次試験: 2科目",
        "入試対策": "少人数制のため合格枠が狭い。共通テストで確実に7割以上を確保し，英語・国語の記述力を磨くことが望ましい。",
        "募集要項": {
            "一般選抜": "https://www.kpu.ac.jp/admissions/exam/guide/general/#0af2beaa",
            "学校推薦型選抜": "https://www.kpu.ac.jp/admissions/exam/guide/recommendation/#0af2beaa"
        }
    },
    {
        "大学名": "滋賀県立大学",
        "学部学科名": "人間文化学部 人間関係学科",
        "区分": "公立",
        "立地": "滋賀県彦根市",
        "マップ検索": "滋賀県立大学",
        "科研費規模": 45,
        "科研費の質": "B・C主体（地域密着・臨床）",
        "研究": 3, "臨床": 4, "教育": 3, "データ統計": 2, "資格実学": 4,
        "入試形式": "一般選抜（前期・後期），学校推薦型選抜",
        "科目数": "共通テスト: 5教科 / 二次試験: 2科目",
        "入試対策": "公立で心理学が学べる貴重な枠。",
        "募集要項": {
            "一般選抜": "https://www.usp.ac.jp/nyushi/senbatsuyoukou/ippansenbatu/",
            "学校推薦型選抜": "https://www.usp.ac.jp/nyushi/senbatsuyoukou/tokubetu/"
        }
    },
    {
        "大学名": "立命館大学",
        "学部学科名": "総合心理学部 総合心理学科",
        "区分": "私立",
        "立地": "大阪府茨木市",
        "マップ検索": "立命館大学 大阪いばらきキャンパス",
        "年間学費(万円)": 140,
        "科研費規模": 85,
        "科研費の質": "A・B多数（私立トップクラスの設備）",
        "研究": 4, "臨床": 4, "教育": 4, "データ統計": 5, "資格実学": 4,
        "入試形式": "一般選抜，共通テスト利用，AO選抜，指定校推薦",
        "科目数": "一般: 3科目 / AO: 書類・面接・小論文",
        "入試対策": "AO選抜は評定平均と活動実績が重視される。一般入試は英語の配点が高く，速読力が求められる。",
        "募集要項": {
            "一般選抜・共テ利用": "https://admission-old.ritsumei.ac.jp/application/general/dl.html",
            "AO選抜": "https://admission-old.ritsumei.ac.jp/application/ao/dl.html"
        }
    },
    {
        "大学名": "同志社大学",
        "学部学科名": "心理学部 心理学科",
        "区分": "私立",
        "立地": "京都府京田辺市",
        "マップ検索": "同志社大学 京田辺キャンパス",
        "年間学費(万円)": 130,
        "科研費規模": 80,
        "科研費の質": "A・B多数（基礎から臨床までバランス良）",
        "研究": 4, "臨床": 4, "教育": 3, "データ統計": 4, "資格実学": 5,
        "入試形式": "一般選抜，共通テスト利用，指定校推薦",
        "科目数": "一般: 3科目（英・国・選択）",
        "入試対策": "英語の難易度が非常に高い。長文の語彙レベルでは京大英語とタメを張れる。",
        "募集要項": {
            "一般選抜・共テ利用": "https://www.doshisha.ac.jp/admissions_undergrad/general_application/index.html"
        }
    },
    {
        "大学名": "関西学院大学",
        "学部学科名": "文学部 総合心理科学科",
        "区分": "私立",
        "立地": "兵庫県西宮市",
        "マップ検索": "関西学院大学 西宮上ヶ原キャンパス",
        "年間学費(万円)": 130,
        "科研費規模": 80,
        "科研費の質": "A・B多数（実験心理学の伝統校）",
        "研究": 5, "臨床": 4, "教育": 4, "データ統計": 4, "資格実学": 4,
        "入試形式": "一般選抜，共通テスト利用，学部特色入試，指定校推薦",
        "科目数": "一般: 3科目 / AO: 書類・面接・口頭試問",
        "入試対策": "基礎研究を重視する校風。一般入試は標準的な問題が多いが，高得点勝負になりやすい。",
        "募集要項": {
            "一般選抜・共テ利用": "https://www.kwansei.ac.jp/admissions/guideline/general.html#id-r17dr0q6",
            "学部特色": "https://www.kwansei.ac.jp/admissions/guideline/faculty-specific.html"
        }
    },
    {
        "大学名": "京都女子大学",
        "学部学科名": "心理共生学部 心理共生学科",
        "区分": "私立",
        "立地": "京都市東山区",
        "マップ検索": "京都女子大学",
        "年間学費(万円)": 135,
        "科研費規模": 50,
        "科研費の質": "B・C主体（臨床・発達の現場に強い）",
        "研究": 3, "臨床": 5, "教育": 5, "データ統計": 2, "資格実学": 5,
        "入試形式": "一般選抜，公募制推薦，総合型選抜，指定校推薦",
        "科目数": "一般: 2科目か3科目 / 公募: 2科目（英・国・数のうち2つ）",
        "入試対策": "公募推薦は英語と現代文のみ。標準的な難易度のため，ミスをしない正確な解答力が求められる。",
        "募集要項": {
            "公募制推薦": "https://www.kyoto-wu.ac.jp/nyushi/daigaku/koubo/index.html",
            "一般選抜": "https://www.kyoto-wu.ac.jp/nyushi/daigaku/ippan_zen/index.html",
            "総合型選抜": "https://www.kyoto-wu.ac.jp/nyushi/daigaku/ao/index.html"
        }
    },
    {
        "大学名": "同志社女子大学",
        "学部学科名": "現代社会学部 社会システム学科",
        "区分": "私立",
        "立地": "京都府京田辺市",
        "マップ検索": "同志社女子大学 京田辺キャンパス",
        "年間学費(万円)": 135,
        "科研費規模": 40,
        "科研費の質": "C主体（教育・臨床実学重視）",
        "研究": 2, "臨床": 4, "教育": 4, "データ統計": 2, "資格実学": 4,
        "入試形式": "一般選抜，公募制推薦，AO選抜，指定校推薦",
        "科目数": "一般: 2科目か3科目 / 公募: 2科目（英・国・数のうち2つ）",
        "入試対策": "京女との併願が多い。標準レベルの問題を確実に正解する基礎力が合格の鍵。",
        "募集要項": {
            "公募制推薦": "https://www.dwc.doshisha.ac.jp/dp/2026_recommendation_s/",
            "一般選抜": "https://www.dwc.doshisha.ac.jp/dp/2026_recommendation_s/",
            "AO選抜": "https://www.dwc.doshisha.ac.jp/dp/250618_2026_ao/s"
        }
    },
    {
        "大学名": "龍谷大学",
        "学部学科名": "心理学部 心理学科",
        "区分": "私立",
        "立地": "京都市伏見区",
        "マップ検索": "龍谷大学 深草キャンパス",
        "年間学費(万円)": 125,
        "科研費規模": 55,
        "科研費の質": "B・C主体（臨床心理の層が厚い）",
        "研究": 3, "臨床": 4, "教育": 4, "データ統計": 3, "資格実学": 4,
        "入試形式": "一般選抜，共通テスト利用，公募制推薦，指定校推薦",
        "科目数": "一般: 3科目 / 公募: 2科目（英・国）",
        "入試対策": "指定校推薦の枠が多い。公募推薦は高得点での争いになるため，過去問での演習が必須。",
        "募集要項": {
            "公募制推薦": "https://www.ryukoku.ac.jp/admission/nyushi/about/download.html",
            "一般選抜": "https://www.ryukoku.ac.jp/admission/nyushi/about/download.html"
        }
    },
]

# 欠損値補完および四軸チャート用のスコア計算
for d in data:
    if "年間学費(万円)" not in d:
        d["年間学費(万円)"] = 54
    # 横軸：教育(プラス) vs 臨床(マイナス)
    d["X_Score"] = d["教育"] - d["臨床"]
    # 縦軸：研究(プラス) vs 資格実学(マイナス)
    d["Y_Score"] = d["研究"] - d["資格実学"]

df = pd.DataFrame(data)
categories = ['研究', '臨床', '教育', 'データ統計', '資格実学']

# --- 2. Streamlit UI構築 ---
st.set_page_config(page_title="関西圏心理学大学比較", layout="wide")
st.title("関西圏 心理学系大学 簡易な比較")

# サイドバー
st.sidebar.header("絞り込み条件")
selected_type = st.sidebar.multiselect("設立区分", ["国立", "公立", "私立"], default=["公立", "私立"])
filtered_df = df[df["区分"].isin(selected_type)]
available_univs = filtered_df["大学名"].tolist()

ideal_defaults = ["京都女子大学", "立命館大学", "関西学院大学", "奈良女子大学"]
valid_defaults = [u for u in ideal_defaults if u in available_univs]
selected_univs = st.sidebar.multiselect("比較する大学を選択", available_univs, default=valid_defaults)

# --- 3. グラフ描画セクション ---

st.markdown("---")
st.subheader("学費 vs 研究力（科研費規模）")
st.markdown("ざっくりいうと，大学の「費用対効果」がわかります。")
st.info("""
科研費（科学研究費助成事業）: 国から配分される研究資金。
特別推進・基盤S/A: 2千万〜数億円（大型設備・世界レベル）
基盤B: 500万〜2000万円（本格的な実験・調査）
基盤C: 500万円以下（地道な臨床・データ分析）

※心理学（特に臨床系）は高額な機械を使わないため，基盤Cが多くなる傾向があります。
""")

fig_scatter = px.scatter(
    filtered_df, x="年間学費(万円)", y="科研費規模", color="区分", text="大学名",
    hover_data=["科研費の質"],
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_scatter.update_traces(
    textposition='top center',
    marker=dict(size=16, line=dict(width=1.5, color='DarkSlateGrey')), 
    textfont=dict(size=13, color='black') 
)

fig_scatter.update_layout(
    height=450,
    plot_bgcolor='rgba(245, 245, 245, 1)', 
    xaxis=dict(title="年間学費（万円）", title_font=dict(size=14, weight="bold"), gridcolor='white', linecolor='black'),
    yaxis=dict(title="科研費規模（相対値）", title_font=dict(size=14, weight="bold"), gridcolor='white', linecolor='black'),
    margin=dict(l=40, r=40, t=40, b=40)
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("大学の学風（スタンス）マップ")
    st.markdown("各大学の注力分野が**「研究か実学か」「教育か臨床か」**で分かれます。")
    
    if selected_univs:
        focus_df = df[df["大学名"].isin(selected_univs)]
    else:
        focus_df = pd.DataFrame(columns=df.columns)

    fig_quad = px.scatter(
        focus_df, x="X_Score", y="Y_Score", color="大学名", text="大学名",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    
    fig_quad.update_traces(
        textposition='top center',
        marker=dict(size=14, opacity=0.8, line=dict(width=1, color='DarkSlateGrey')),
        textfont=dict(size=12, color='black')
    )

    fig_quad.add_hline(y=0, line_width=2, line_color="black", opacity=0.3)
    fig_quad.add_vline(x=0, line_width=2, line_color="black", opacity=0.3)

    fig_quad.update_layout(
        height=450,
        showlegend=False,
        plot_bgcolor='rgba(250, 250, 250, 1)',
        xaxis=dict(title="← 臨床現場重視　｜　教育・学校重視 →", range=[-2.5, 2.5], zeroline=False, gridcolor='white'),
        yaxis=dict(title="↓ 資格・実学重視　｜　研究重視 ↑", range=[-2.5, 2.5], zeroline=False, gridcolor='white'),
        margin=dict(l=40, r=40, t=20, b=40)
    )
    st.plotly_chart(fig_quad, use_container_width=True)

with col2:
    st.subheader("分野別レーダーチャート")
    st.markdown("具体的な5つの指標のバランスを確認できます。")
    if selected_univs:
        fig_radar = go.Figure()
        colors = px.colors.qualitative.Safe
        
        for i, univ in enumerate(selected_univs):
            univ_data = df[df["大学名"] == univ].iloc[0]
            fig_radar.add_trace(go.Scatterpolar(
                r=[univ_data[cat] for cat in categories],
                theta=categories, 
                fill='toself', 
                name=univ,
                opacity=0.4,
                line=dict(width=2)
            ))
            
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5], gridcolor='lightgrey')), 
            height=450,
            colorway=colors,
            margin=dict(l=40, r=40, t=20, b=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("サイドバーから大学を選択してください。")

# --- 4. 詳細情報セクション ---
st.markdown("---")
st.subheader("選択した大学の詳細情報")

if selected_univs:
    cols = st.columns(len(selected_univs))
    
    for i, univ in enumerate(selected_univs):
        with cols[i]:
            univ_data = df[df["大学名"] == univ].iloc[0]
            st.markdown(f"### {univ}")
            
            # --- 募集要項リンクの動的生成（複数対応） ---
            st.markdown("**募集要項・入試情報**")
            urls = univ_data.get("募集要項", {})
            if isinstance(urls, dict):
                for name, url in urls.items():
                    # 形式ごとにボタンを生成
                    st.link_button(f"{name}の要項を見る", url, use_container_width=True)
            elif isinstance(urls, str):
                st.link_button("要項を見る", urls, use_container_width=True)
            
            st.write(f"**学部学科:** {univ_data['学部学科名']}")
            
            with st.expander("入試・科目の詳細を確認", expanded=True):
                st.write(f"**形式:** {univ_data['入試形式']}")
                st.write(f"**科目:** {univ_data['科目数']}")
                st.write(f"**対策:** {univ_data['入試対策']}")
            
            st.write(f"**立地:** {univ_data['立地']}")
            st.write(f"**科研費評価:** {univ_data['科研費の質']}")
            
            # リンク生成
            search_query = urllib.parse.quote(f"{univ} 心理")
            kenkyu_url = f"https://research-er.jp/researchers/search?q={search_query}"
            st.markdown(f"[日本の研究.com で分析する]({kenkyu_url})")
            
            # Google Map
            map_query = urllib.parse.quote(univ_data["マップ検索"])
            map_html = f"""
            <iframe 
                width="100%" 
                height="200" 
                frameborder="0" 
                style="border:0; border-radius: 4px;" 
                src="https://maps.google.com/maps?q={map_query}&t=m&z=14&output=embed">
            </iframe>
            """
            components.html(map_html, height=210)
else:
    st.info("左側のメニューから比較したい大学を選択してください。")
