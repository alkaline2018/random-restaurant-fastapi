from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Tuple, List
import time

from utils.extrack_random import extrack_random
from utils.mongodb_crud import find_nearby_store

cache: Dict[Tuple[float, float], Tuple[List[dict], float]] = {}
from utils.cache_utils import read_cache, save_cache

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처에서의 요청 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 캐시를 저장할 딕셔너리: 좌표를 키로 하고 결과와 타임스탬프 저장

@app.get("/restaurants")
async def get_nearby_restaurants(
    latitude: float = Query(..., description="사용자 위도"),
    longitude: float = Query(..., description="사용자 경도"),
    distance: int = Query(300, description="거리 범위 (미터)", le=1000, ge=0)
):
    cache_key = (latitude, longitude, distance)  # 좌표를 튜플로 사용
    current_time = time.time()

    # 1. 캐시 확인 (필요시 캐시는 redis로 대체할 수 있다.)
    nearby_restaurants = read_cache(cache_key=cache_key, current_time=current_time)
    if nearby_restaurants is None:
        # 2. 캐시에 없거나 만료되었으면 MongoDB에서 조회
        nearby_restaurants = await find_nearby_store(distance, latitude, longitude)

        # 3. 조회된 결과를 캐시에 저장
        save_cache(cache_key=cache_key, current_time=current_time, nearby_restaurants=nearby_restaurants)

    # 4. 조회된 결과에서 랜덤하게 3개 선택하여 반환
    return await extrack_random(nearby_restaurants)


