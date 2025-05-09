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

mode = st.radio("👁️ 모드 선택", ["내 매물 추적", "경쟁사 매물 추적"], horizontal=True)
listing_type = "mine" if mode == "내 매물 추적" else "competitor"

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

st.title(f"📊 {'내 매물' if listing_type == 'mine' else '경쟁사'} 순위 대시보드")

if listing_type == "competitor":
    st.markdown(
        "<h2 style='color: red;'>⚠️ 경쟁사 매물 추적모드 ON</h2>",
        unsafe_allow_html=True
    )

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
    'NNB': 'HGQLO5MZU3SWK',
    'ASID': '3b0617410000018e7de810270000006a',
    'NV_WETR_LOCATION_RGN_M': '"V0RKUE4wMDA0Nw=="',
    'NV_WETR_LAST_ACCESS_RGN_M': '"V0RKUE4wMDA0Nw=="',
    '_ga_8P4PY65YZ2': 'GS1.1.1721626196.1.1.1721626196.60.0.0',
    '_ga': 'GA1.2.255590847.1721626197',
    '_fwb': '216eIwZnTsTwBjLg00ov0y9.1736852003092',
    '_fwb': '1480C9OngmytGZxmBhGNXPn.1736852017398',
    'NAC': 'pA1KBkgahayV',
    'NACT': '1',
    'nid_inf': '2016950829',
    'NID_AUT': 'eMJ56KrwyKuphc3REVS0AOiQ/z16TSRc4dYaEKAoFCt4sl/BbWtyj8d5ikA9AMcs',
    'NID_JKL': 'wD6Vrju/VrGpglrDM+d51P1/7WfWFHG9VJJAxSWKDkg=',
    'SRT30': '1746706056',
    'page_uid': 'jtymBlqVN8ossOARQbRssssstxK-214519',
    'nhn.realestate.article.rlet_type_cd': 'A01',
    'nhn.realestate.article.trade_type_cd': '""',
    'nhn.realestate.article.ipaddress_city': '1100000000',
    'landHomeFlashUseYn': 'Y',
    'REALESTATE': 'Thu%20May%2008%202025%2021%3A20%3A37%20GMT%2B0900%20(Korean%20Standard%20Time)',
    'NID_SES': 'AAAB/cl995xnxkUB5IEmSqZ23w3C7cfo7Ypxioe0ak9XNhQWtJsRvH/oalXO8oHowanrnP7Rg9MHIOsbyUIvuzkmXbsxehSskxoIPEH1CRpwKZw0xw61TXKIl2PtzPNSfd5KgvA32De8q9fBwXyBa0kFVgZ4gDPX3q3Av7ESxNr16URTWoVvFEfFeMPcltlVo8SI4SlWGJ2v2I5z3Bd2p5IALVNSrDtCkgN5evXyMZnKqjsy9cHIdS350iSqO/a5iBBFOgVffcuEU1KqeLebBNMIcJH+3A3enbK1Gmrsxw9ttBGnH7BVYT1cbv/a3w74iHPIXCd1AXzTo4B/RMPtnUcU6YCDXEeLtWc+L9p3+FUG0ipyk80CylZbNwUENlNaREHTXUPiZx0CwvWmplqyVubezplZ/xQuDJJX6tujZ30Kn+rldWRttZW2eI/+nbna8+U7Zc8Bi2oRYmK9mYmFxy0hx3HHpqwT0Cc1K2pvj8pSlG5npxkDohmlLKO7ZX8yIVQp28Wk/FuZm+JiiecxUZ7okHeP2CyZilK0pP1tE4vctva8IE2F0sxa6KBDo1qms/oGP3JrwE/j4noFSC1x0eoo6pButhKud9Aj3OIomOH7K54UA+yw+2/7nS7bpmB++X+X1eaR0E4U5p5/KqQfKHD65UXFLycFlvzhlZAVqarMmv4o',
    'SRT5': '1746713273',
    'BUC': 'O1rhw8E8eFI0VhhG0MjmAlqmyaXqhlJTcanU8I_2gxA=',
}

        headers = {
        'accept': '*/*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NDY3MDY4MzcsImV4cCI6MTc0NjcxNzYzN30.To94dlVKl3bgzE72PomNsGW79Y73AGtrEiN11Q1S4RE',
        'priority': 'u=1, i',
        'referer': 'https://new.land.naver.com/offices?ms=37.5019107,126.9476819,18&a=SG:SMS:GJCG:APTHGJ:GM:TJ&e=RETAIL&ad=true&articleNo=2523591454',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        # 'cookie': 'NNB=HGQLO5MZU3SWK; ASID=3b0617410000018e7de810270000006a; NV_WETR_LOCATION_RGN_M="V0RKUE4wMDA0Nw=="; NV_WETR_LAST_ACCESS_RGN_M="V0RKUE4wMDA0Nw=="; _ga_8P4PY65YZ2=GS1.1.1721626196.1.1.1721626196.60.0.0; _ga=GA1.2.255590847.1721626197; _fwb=216eIwZnTsTwBjLg00ov0y9.1736852003092; _fwb=1480C9OngmytGZxmBhGNXPn.1736852017398; NAC=pA1KBkgahayV; NACT=1; nid_inf=2016950829; NID_AUT=eMJ56KrwyKuphc3REVS0AOiQ/z16TSRc4dYaEKAoFCt4sl/BbWtyj8d5ikA9AMcs; NID_JKL=wD6Vrju/VrGpglrDM+d51P1/7WfWFHG9VJJAxSWKDkg=; SRT30=1746706056; page_uid=jtymBlqVN8ossOARQbRssssstxK-214519; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=""; nhn.realestate.article.ipaddress_city=1100000000; landHomeFlashUseYn=Y; REALESTATE=Thu%20May%2008%202025%2021%3A20%3A37%20GMT%2B0900%20(Korean%20Standard%20Time); NID_SES=AAAB/cl995xnxkUB5IEmSqZ23w3C7cfo7Ypxioe0ak9XNhQWtJsRvH/oalXO8oHowanrnP7Rg9MHIOsbyUIvuzkmXbsxehSskxoIPEH1CRpwKZw0xw61TXKIl2PtzPNSfd5KgvA32De8q9fBwXyBa0kFVgZ4gDPX3q3Av7ESxNr16URTWoVvFEfFeMPcltlVo8SI4SlWGJ2v2I5z3Bd2p5IALVNSrDtCkgN5evXyMZnKqjsy9cHIdS350iSqO/a5iBBFOgVffcuEU1KqeLebBNMIcJH+3A3enbK1Gmrsxw9ttBGnH7BVYT1cbv/a3w74iHPIXCd1AXzTo4B/RMPtnUcU6YCDXEeLtWc+L9p3+FUG0ipyk80CylZbNwUENlNaREHTXUPiZx0CwvWmplqyVubezplZ/xQuDJJX6tujZ30Kn+rldWRttZW2eI/+nbna8+U7Zc8Bi2oRYmK9mYmFxy0hx3HHpqwT0Cc1K2pvj8pSlG5npxkDohmlLKO7ZX8yIVQp28Wk/FuZm+JiiecxUZ7okHeP2CyZilK0pP1tE4vctva8IE2F0sxa6KBDo1qms/oGP3JrwE/j4noFSC1x0eoo6pButhKud9Aj3OIomOH7K54UA+yw+2/7nS7bpmB++X+X1eaR0E4U5p5/KqQfKHD65UXFLycFlvzhlZAVqarMmv4o; SRT5=1746713273; BUC=O1rhw8E8eFI0VhhG0MjmAlqmyaXqhlJTcanU8I_2gxA=',
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
