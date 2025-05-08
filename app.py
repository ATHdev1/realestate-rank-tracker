import streamlit as st
import requests
import json
import os

LISTING_FILE = "my_listings.json"

# -----------------------
# ✅ 파일에서 매물 불러오기 / 저장
# -----------------------
# ❌ 캐싱 제거 (cache_data 없애기!)
def load_listings(file_path="my_listings.json"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_listings(listings, file_path=LISTING_FILE):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

# -----------------------
# ✅ 마커 안의 매물 목록 가져오기
# -----------------------
def get_article_list(marker_id, cookies, headers):
    url = f"https://new.land.naver.com/api/articles"
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

# -----------------------
# ✅ 매물 순위 찾기
# -----------------------
def find_article_rank(article_list, article_no):
    for idx, article in enumerate(article_list):
        if article["articleNo"] == article_no:
            return idx + 1
    return None

# -----------------------
# ✅ Streamlit 인터페이스
# -----------------------
st.set_page_config(page_title="네이버 부동산 순위 조회기", layout="wide")
st.title("📊 네이버 부동산 내 매물 순위 확인기")

# ✅ 1. 매물 목록 불러오기
my_articles = load_listings()

# ✅ 2. 매물 등록 폼
st.subheader("📝 새 매물 등록하기")
with st.form("add_listing_form"):
    new_name = st.text_input("매물 이름", "")
    new_marker_id = st.text_input("마커 ID", "")
    new_article_no = st.text_input("매물 ID", "")
    submitted = st.form_submit_button("추가")

    if submitted:
        if new_name and new_marker_id and new_article_no:
            new_item = {
                "name": new_name,
                "markerId": new_marker_id,
                "articleNo": new_article_no
            }
            my_articles.append(new_item)
            save_listings(my_articles)
            st.success(f"✅ 매물 '{new_name}' 추가 완료! 페이지를 새로고침하세요.")
        else:
            st.error("❌ 모든 항목을 입력해야 추가됩니다.")

# ✅ 3. 등록된 매물 보기
st.subheader("📄 등록된 매물 목록")

if not my_articles:
    st.warning("등록된 매물이 없습니다.")
else:
    for i, a in enumerate(my_articles):
        col1, col2 = st.columns([6, 1])  # 👉 삭제 버튼 오른쪽 정렬

        with col1:
            st.write(f"📌 {a['name']} | MarkerID: `{a['markerId']}` | ArticleNo: `{a['articleNo']}`")

        with col2:
            if st.button("❌", key=f"delete_{i}"):
                my_articles.pop(i)
                save_listings(my_articles)
                st.success(f"🗑️ '{a['name']}' 삭제됨")
                st.experimental_rerun()


# ✅ 4. 조회 버튼
if st.button("📥 순위 조회 시작"):
    # 💡 여기에 너의 진짜 쿠키/헤더 넣기

    # ⚠️ 쿠키/헤더는 따로 보관해야 함
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

    for item in my_articles:
        name = item["name"]
        marker_id = item["markerId"]
        article_no = item["articleNo"]

        article_list = get_article_list(marker_id, cookies, headers)
        rank = find_article_rank(article_list, article_no)

        if rank:
            st.success(f"✅ [{name}] : {rank}위")
        else:
            st.warning(f"❌ [{name}] 마커 내에서 매물 확인 불가")