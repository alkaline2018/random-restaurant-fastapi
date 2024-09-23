import random


async def extrack_random(nearby_restaurants):
    return random.sample(nearby_restaurants, min(3, len(nearby_restaurants)))
