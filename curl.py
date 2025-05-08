import requests

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

response = requests.get(
    'https://new.land.naver.com/api/articles?zoom=18&leftLon=126.9431758&rightLon=126.952188&topLat=37.5035449&bottomLat=37.5002765&order=rank&realEstateType=SG%3ASMS%3AGJCG%3AAPTHGJ%3AGM%3ATJ&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page=1&articleState',
    cookies=cookies,
    headers=headers,
)

print(response.text)