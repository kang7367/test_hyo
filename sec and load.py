"""POI 주소/장소 검색 Streamlit 테스트 페이지."""

from __future__ import annotations

import uuid

import requests
import streamlit as st

API_URL = "http://220.95.208.145:41024/api/v1/poi"
ENTITY_MAP = {
    "주소": "LCC",
    "장소": "AFP",
}

DEFAULT_HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
}


def build_payload(
    word: str,
    entity: str,
    *,
    search_type: str = "kakao",
    location: str = "seai",
    use_rawdata: bool = True,
    gis_x: str = "0",
    gis_y: str = "0",
    radius: int = 0,
) -> dict:
    return {
        "master": {
            "domain_id": 1,
            "user_id": 1,
            "request_id": uuid.uuid4().hex[:16],
            "reply_to": "AOM_POI_SEARCH_RESULT",
        },
        "content": {
            "token_id": str(uuid.uuid4()),
            "caller_info": {
                "gis_x": gis_x,
                "gis_y": gis_y,
                "coord_system_type": "4326",
                "radius": radius,
            },
            "ner_histories": [
                {
                    "seq": 1,
                    "ner_list": [
                        {
                            "entity": entity,
                            "score": 1.0,
                            "index": 0,
                            "word": word,
                            "start": 0,
                            "end": len(word),
                            "entity_type": "30",
                        }
                    ],
                }
            ],
            "use_rawdata": use_rawdata,
            "location": location,
            "search_type": search_type,
        },
        "result_status": {
            "code": "200",
            "message": "Success",
            "detail": "Success",
        },
        "task": "poi_search",
    }


RESULT_FIELDS = ("poi_name", "gis_x", "gis_y", "law_address", "road_address")


def search_poi(payload: dict, timeout: float = 10.0) -> tuple[int, dict | list | str]:
    response = requests.post(API_URL, headers=DEFAULT_HEADERS, json=payload, timeout=timeout)
    try:
        body = response.json()
    except ValueError:
        body = response.text
    return response.status_code, body


def extract_poi_results(body: dict | list | str) -> list[dict]:
    """content.address_analysis_results 에서 필요한 필드만 추출."""
    if not isinstance(body, dict):
        return []

    results = body.get("content", {}).get("address_analysis_results") or []
    if not isinstance(results, list):
        return []

    rows: list[dict] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        rows.append({field: item.get(field) for field in RESULT_FIELDS})
    return rows


st.set_page_config(page_title="POI 검색 테스트", page_icon="📍", layout="wide")
st.title("POI 주소 / 장소 검색")
st.caption(f"API: `{API_URL}` · 주소=`LCC`, 장소=`AFP`")

with st.sidebar:
    st.header("옵션")
    search_type = st.selectbox("search_type", ["kakao", "naver", "tmap"], index=0)
    location = st.text_input("location", value="seai")
    use_rawdata = st.checkbox("use_rawdata", value=True)
    timeout = st.number_input("timeout (초)", min_value=1.0, max_value=60.0, value=10.0, step=1.0)
    with st.expander("caller_info"):
        gis_x = st.text_input("gis_x", value="0")
        gis_y = st.text_input("gis_y", value="0")
        radius = st.number_input("radius", min_value=0, value=0, step=100)

col_type, col_word = st.columns([1, 3])
with col_type:
    search_kind = st.radio("검색 유형", list(ENTITY_MAP.keys()), horizontal=True)
with col_word:
    word = st.text_input(
        "검색어 (word)",
        placeholder="예: 갈현로 300 / 강남역",
        value="",
    )

entity = ENTITY_MAP[search_kind]
st.write(f"entity: `{entity}`")

if st.button("검색", type="primary"):
    if not word.strip():
        st.warning("검색어를 입력하세요.")
    else:
        payload = build_payload(
            word.strip(),
            entity,
            search_type=search_type,
            location=location,
            use_rawdata=use_rawdata,
            gis_x=gis_x,
            gis_y=gis_y,
            radius=int(radius),
        )

        with st.expander("요청 payload", expanded=False):
            st.json(payload)

        with st.spinner("검색 중..."):
            try:
                status, body = search_poi(payload, timeout=float(timeout))
            except requests.RequestException as exc:
                st.error(f"요청 실패: {exc}")
            else:
                st.subheader(f"검색 결과 (HTTP {status})")
                if not isinstance(body, dict):
                    st.code(body)
                else:
                    rows = extract_poi_results(body)
                    if rows:
                        st.dataframe(rows, use_container_width=True, hide_index=True)
                    else:
                        st.info("address_analysis_results 가 비어 있습니다.")

                    with st.expander("원본 응답", expanded=False):
                        st.json(body)
