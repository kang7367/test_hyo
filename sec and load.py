import requests

url = "http://220.95.208.145:41024/api/v1/poi"

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

payload = {
    "master": {
        "domain_id": 1,
        "user_id": 1,
        "request_id": "eadifdsafdhjk153",
        "reply_to": "AOM_POI_SEARCH_RESULT",
    },
    "content": {
        "token_id": "aa0443a2-65a8-4ae1-9e64-c7577ee4ba5c",
        "caller_info": {
            "gis_x": "0",
            "gis_y": "0",
            "coord_system_type": "4326",
            "radius": 0,
        },
        "ner_histories": [
            {
                "seq": 1,
                "ner_list": [
                    {
                        "entity": "LCC",
                        "score": 0.8626434206962585,
                        "index": 13,
                        "word": "갈현로 300",
                        "start": 27,
                        "end": 32,
                        "entity_type": "30",
                    }
                ],
            }
        ],
        "use_rawdata": True,
        "location": "seai",
        "search_type": "kakao",
    },
    "result_status": {
        "code": "200",
        "message": "Success",
        "detail": "Success",
    },
    "task": "poi_search",
}

response = requests.post(url, headers=headers, json=payload, timeout=10)

print(response.status_code)
print(response.json())
