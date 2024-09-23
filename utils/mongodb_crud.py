from pymongo import MongoClient

# MongoDB 연결
# 공인ip 49.50.173.55
client = MongoClient("mongodb://49.50.173.55:27017/")
# client = MongoClient("mongodb://10.41.143.83:27017/")
db = client['nice_kibisis']
restaurant_collection = db['naver_place_202409_restorant']

async def find_nearby_store(distance, latitude, longitude):
    geo_near_query = await get_nearby_query(distance, latitude, longitude)
    nearby_restaurants = list(restaurant_collection.aggregate([
        geo_near_query,
        {
            "$match": {
                "categoryCodeList": {"$nin": ["220052"]}
            }
        },
        {"$project":
             {"_id": 0}
         }
    ]))
    return nearby_restaurants

async def find_nearby_cafe(distance, latitude, longitude):
    geo_near_query = await get_nearby_query(distance, latitude, longitude)
    nearby_restaurants = list(restaurant_collection.aggregate([
        geo_near_query,
        {
            "$match": {
                "categoryCodeList": {"$in": ["220052"]}
            }
        },
        {"$project":
             {"_id": 0}
         }
    ]))
    return nearby_restaurants


async def get_nearby_query(distance, latitude, longitude):
    return {
        "$geoNear": {
            "near": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            },
            "distanceField": "dist.calculated",
            "maxDistance": distance,
            "spherical": True
        }
    }
