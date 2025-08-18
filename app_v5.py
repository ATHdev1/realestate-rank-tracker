import streamlit as st
import pandas as pd
import requests
from supabase import create_client

# ------------------------------
# Supabase 연결 설정
# ------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ------------------------------
# Supabase 연동 함수
# ------------------------------
def load_listings(listing_type):
    res = supabase.table("listings").select("*").eq("type", listing_type).order("created_at").execute()
    return res.data if res.data else []

def add_listing(name, marker_id, article_no, listing_type):
    supabase.table("listings").insert({
        "name": name,
        "marker_id": marker_id,
        "article_no": article_no,
        "type": listing_type
    }).execute()

def update_listing(id, name, marker_id, article_no):
    supabase.table("listings").update({
        "name": name,
        "marker_id": marker_id,
        "article_no": article_no
    }).eq("id", id).execute()

def delete_listing(id):
    supabase.table("listings").delete().eq("id", id).execute()

# ------------------------------
# 네이버 부동산 매물 순위 조회
# ------------------------------
def get_article_list(marker_id, cookies, headers):
    url = "https://new.land.naver.com/api/articles"
    all_articles = []
    page = 1

    while True:
        params = {
            "markerId": marker_id,
            "markerType": "LGEOHASH_MIX_ARTICLE",
            "order": "rank",
            "realEstateType": "SG:SMS:GJCG:APTHGJ:GM:TJ",
            "priceType": "RETAIL",
            "page": page,
            "sameAddressGroup": "false",
            "articleState": ""
        }

        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        if response.status_code != 200:
            break

        data = response.json()
        articleList = data.get("articleList", [])

        filtered = [
            a for a in articleList
            if a.get("isLocationShow", True)
            and a.get("articleStatus") == "R0"
            and a.get("realEstateTypeCode") != "GM"
        ]

        all_articles.extend(filtered)

        if not data.get("isMoreData"):
            break

        page += 1

    return all_articles

def find_article_rank(article_list, article_no):
    for idx, article in enumerate(article_list):
        if article["articleNo"] == article_no:
            return idx + 1
    return None

# ------------------------------
# Streamlit UI 시작
# ------------------------------
st.set_page_config("매물 순위 대시보드", layout="wide")

mode = st.radio("👁️ 모드 선택", ["내 매물 추적1", "내 매물 추적2"], horizontal=True)
listing_type = "mine" if mode == "내 매물 추적1" else "competitor"

custom_style = """
    <style>
    h1 { font-size: 2.6rem; }
    .rank-good { background-color: #d0f5e8; }
    .rank-missing { color: #aaa; font-style: italic; }
    .listing-table td { padding: 0.6rem 1rem; }
    body { background-color: %s; }
    </style>
""" % ("#fefefe" if listing_type == "mine" else "#fff5e5")
st.markdown(custom_style, unsafe_allow_html=True)

st.title(f"📊 {'내 매물 1 ' if listing_type == 'mine' else '내 매물 2 '} 순위 대시보드")

my_articles = load_listings(listing_type)

col_left, col_right = st.columns([3, 2])

# 매물 추가 폼
with col_right:
    st.subheader("➕ 매물 추가")
    with st.form("add_form"):
        name = st.text_input("이름")
        marker = st.text_input("마커 ID")
        article = st.text_input("매물 ID")
        add_btn = st.form_submit_button("등록")
        if add_btn and name and marker and article:
            add_listing(name, marker, article, listing_type)
            st.success("✅ 등록 완료!")
            st.rerun()

# 전체 순위 조회
with col_left:
    st.subheader("📥 전체 순위 조회")
    if st.button("순위 불러오기"):
        cookies = {
    'NAC': 'NKgGBsQeTHfzA',
    'NACT': '1',
    'NNB': 'ZFNC75J44CRGQ',
    'SRT30': '1755504700',
    'SRT5': '1755504700',
    'BUC': 'wxZ1PzgW3K1j2-fyJvKD5fdFehEoTj8gaSG4lzOaOfs=',
    'page_uid': 'j67lnwqo1awss7PNbm4ssssstgK-355462',
    '_naver_usersession_': 'UX4g2NwMO26sMm9Lf50AVQ==',
    'nhn.realestate.article.rlet_type_cd': 'A01',
    'nhn.realestate.article.trade_type_cd': '""',
    'nhn.realestate.article.ipaddress_city': '2600000000',
    '_fwb': '55MJ4BmmkBJuDKMGlmuNgr.1755504705977',
    'landHomeFlashUseYn': 'Y',
    '_ga_451MFZ9CFM': 'GS2.1.s1755504708$o1$g0$t1755504709$j59$l0$h0',
    '_ga': 'GA1.1.1211837318.1755504709',
    'REALESTATE': 'Mon%20Aug%2018%202025%2017%3A11%3A56%20GMT%2B0900%20(Korean%20Standard%20Time)',
    'PROP_TEST_KEY': '1755504716127.1166d121925afea4faa5636f1d7dbeba8768a149294d01ddef746a2fe206b347',
    'PROP_TEST_ID': '9c8d0d90d54cca9536f20a587e65781cef6b55ad05b3dd34ab2c6212b808274e',
    '_fwb': '55MJ4BmmkBJuDKMGlmuNgr.1755504705977',
}

        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': '*/*',
    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://new.land.naver.com/offices?ms=37.3595704,127.105399,16&a=SG:SMS:GJCG:APTHGJ:GM:TJ&e=RETAIL',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NTU1MDQ3MDksImV4cCI6MTc1NTUxNTUwOX0.Rdg0IrJN2RoVObTxjwsZfjQAAJ3V0sxffyrg8Fh8vVM',
    'Connection': 'keep-alive',
    # 'Cookie': 'NAC=NKgGBsQeTHfzA; NACT=1; NNB=ZFNC75J44CRGQ; SRT30=1755504700; SRT5=1755504700; BUC=wxZ1PzgW3K1j2-fyJvKD5fdFehEoTj8gaSG4lzOaOfs=; page_uid=j67lnwqo1awss7PNbm4ssssstgK-355462; _naver_usersession_=UX4g2NwMO26sMm9Lf50AVQ==; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=""; nhn.realestate.article.ipaddress_city=2600000000; _fwb=55MJ4BmmkBJuDKMGlmuNgr.1755504705977; landHomeFlashUseYn=Y; _ga_451MFZ9CFM=GS2.1.s1755504708$o1$g0$t1755504709$j59$l0$h0; _ga=GA1.1.1211837318.1755504709; REALESTATE=Mon%20Aug%2018%202025%2017%3A11%3A56%20GMT%2B0900%20(Korean%20Standard%20Time); PROP_TEST_KEY=1755504716127.1166d121925afea4faa5636f1d7dbeba8768a149294d01ddef746a2fe206b347; PROP_TEST_ID=9c8d0d90d54cca9536f20a587e65781cef6b55ad05b3dd34ab2c6212b808274e; _fwb=55MJ4BmmkBJuDKMGlmuNgr.1755504705977',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }

        results = []
        for item in my_articles:
            articles = get_article_list(item["marker_id"], cookies, headers)
            rank = find_article_rank(articles, item["article_no"])
            total = len(articles)
            rank_str = f"{rank}위 (총 {total}개 중)" if rank else "❌ 없음"
            results.append({
                "id": item["id"],
                "이름": item["name"],
                "마커 ID": item["marker_id"],
                "매물 ID": item["article_no"],
                "순위": rank_str
            })

        df = pd.DataFrame(results)
        st.dataframe(df.drop(columns=["id"]), use_container_width=True, height=600)
    else:
        st.info("👈 왼쪽에서 순위를 조회해보세요.")

# 등록된 매물 일괄 수정/삭제
st.markdown("---")
st.subheader("🛠 등록된 매물 관리")

df_edit = pd.DataFrame(my_articles)
if not df_edit.empty:
    df_edit["삭제"] = False
    df_edit_display = st.data_editor(
        df_edit[["id", "name", "marker_id", "article_no", "삭제"]],
        use_container_width=True,
        num_rows="dynamic",
        key="editable_table"
    )

    if st.button("💾 수정 저장"):
        for row in df_edit_display.itertuples():
            update_listing(row.id, row.name, row.marker_id, row.article_no)
        st.success("✅ 모든 수정사항 저장 완료!")
        st.rerun()

    if st.button("🗑 선택된 매물 삭제"):
        to_delete = df_edit_display[df_edit_display["삭제"] == True]
        for row in to_delete.itertuples():
            delete_listing(row.id)
        st.success("🧹 삭제 완료")
        st.rerun()
else:
    st.info("매물이 아직 등록되어 있지 않습니다.")
