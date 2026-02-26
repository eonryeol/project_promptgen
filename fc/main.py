from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
from bs4 import BeautifulSoup
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 (가격 조회)
@app.get("/api/price")
def get_player_price(spid: int, n1strong: int = 1):
    url = "https://fconline.nexon.com/datacenter/PlayerPriceGraph"
    payload = {"spid": spid, "n1strong": n1strong, "rd": random.random()}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"https://fconline.nexon.com/datacenter/PlayerInfo?spid={spid}&n1strong={n1strong}"
    }
    
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price_tag = soup.select_one('.txt strong')
        if price_tag:
            return {
                "status": "success", "spid": spid,
                "price_text": price_tag.text.strip(),
                "price_number": price_tag.get('alt')
            }
        return {"status": "error", "message": "가격 정보를 찾을 수 없음"}
    return {"status": "error", "message": f"넥슨 서버 에러: {response.status_code}"}

# 주의: API 라우터들을 먼저 선언하고, 가장 마지막에 StaticFiles를 마운트해야 해.
# 이 코드가 있는 폴더 안의 모든 파일(html, json)을 웹 서버로 제공함.
app.mount("/", StaticFiles(directory=".", html=True), name="static")