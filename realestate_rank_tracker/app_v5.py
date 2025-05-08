import streamlit as st
import pandas as pd
import requests
import json
import os

LISTING_FILE = "my_listings.json"

# ------------------
# 파일 로드/저장
# ------------------
def load_listings():
    if not os.path.exists(LISTING_FILE):
        return []
    with open(LISTING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_listings(listings):
    with open(LISTING_FILE, "w", encoding="utf-8") as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

# ------------------
# API 호출
# ------------------
def get_article_list(marker_id, cookies, headers):
    url = "https://new.land.naver.com/api/articles"
    params = {
        "markerId": marker_id,
        "markerType": "LGEOHASH_MIX_ARTICLE",
        "order": "rank",
        "realEstateType": "SG:SMS:GJCG:APTHGJ:GM:TJ",
        "priceType": "RETAIL",
        "page": 1,
        "articleState": ""
    }
    response = requests.get(url, params=params, headers=headers, cookies=cookies)
    if response.status_code == 200:
        return response.json().get("articleList", [])
    return []

def find_article_rank(article_list, article_no):
    for idx, article in enumerate(article_list):
        if article["articleNo"] == article_no:
            return idx + 1
    return None

# ------------------
# Streamlit 시작
# ------------------
st.set_page_config("내 매물 순위 대시보드", layout="wide")
st.markdown("""
    <style>
    h1 {
        font-size: 2.8rem;
    }
    .rank-good { background-color: #d0f5e8; }
    .rank-missing { color: #aaa; font-style: italic; }
    .listing-table td { padding: 0.6rem 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 내 매물 순위 대시보드")

my_articles = load_listings()

# ------------------
# 매물 추가
# ------------------
st.subheader("➕ 매물 추가")
with st.form("add_form"):
    name = st.text_input("이름")
    marker = st.text_input("마커 ID")
    article = st.text_input("매물 ID")
    add_btn = st.form_submit_button("등록")
    if add_btn:
        if name and marker and article:
            my_articles.append({"name": name, "markerId": marker, "articleNo": article})
            save_listings(my_articles)
            st.success("✅ 등록 완료!")
            st.rerun() 
        else:
            st.error("❌ 모든 값을 입력해주세요")

# ------------------
# 매물 수정/삭제 (표 기반)
# ------------------
st.subheader("🛠️ 매물 수정 및 삭제")
df_edit = pd.DataFrame(my_articles)
edited_df = st.data_editor(df_edit, use_container_width=True, num_rows="dynamic", key="editor")

if st.button("💾 변경사항 저장"):
    my_articles = edited_df.to_dict(orient="records")
    save_listings(my_articles)
    st.success("저장 완료!")
    st.rerun() 

# ------------------
# 순위 조회
# ------------------
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
        articles = get_article_list(item["markerId"], cookies, headers)
        rank = find_article_rank(articles, item["articleNo"])
        total = len(articles)
        if rank:
            rank_str = f"{rank}위 (총 {total}개 중)"
        else:
            rank_str = "❌ 없음"

        results.append({
            "이름": item["name"],
            "마커 ID": item["markerId"],
            "매물 ID": item["articleNo"],
            "순위": rank_str
        })

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True, height=720)
else:
    st.info("👈 위 버튼을 눌러 순위를 조회해보세요.")
