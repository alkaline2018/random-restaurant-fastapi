from typing import Dict, Tuple, List
import random

from main import cache

# 캐시 만료 시간 (5분)
CACHE_TTL = 300  # 초 단위로 설정 (5분 = 300초)
def read_cache(cache_key: (float, float, int), current_time):
    if cache_key in cache:
        cached_data, timestamp = cache[cache_key]

        # 캐시가 유효한지 확인 (TTL 초과 여부)
        if current_time - timestamp < CACHE_TTL:
            return cached_data
        else:
            # 캐시가 만료되었으면 캐시에서 제거
            del cache[cache_key]


def save_cache(cache_key: (float, float, int), current_time, nearby_restaurants: List):
    cache[cache_key] = (nearby_restaurants, current_time)
