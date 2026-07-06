import streamlit as st
from structure_design.sections import GirderSection
from structure_design.loads import GirderLoads

st.set_page_config(page_title="PSC 설계 플랫폼", layout="wide")

st.title("🏗️ PSC 거더 설계 자동화 플랫폼")

# 사이드바 입력창
st.sidebar.header("설계 변수 입력")
B = st.sidebar.number_input("전체 폭 (B, mm)", value=1100)
B1 = st.sidebar.number_input("플랜지 제외 폭 (B1, mm)", value=300)
H = st.sidebar.number_input("전체 높이 (H, mm)", value=1080)
H2 = st.sidebar.number_input("하부 플랜지 높이 (H2, mm)", value=450)
span = st.sidebar.number_input("Span (m)", value=11.0)
live_load = st.sidebar.number_input("활하중 (kPa)", value=20.0)

# 설계 실행
if st.button("설계 검증 실행"):
    # 1. 단면 성질 계산
    girder = GirderSection(B, B1, H, H2)
    props = girder.calculate_properties()
    
    # 2. 하중 산정
    loads_engine = GirderLoads(girder_area_mm2=props['A_PC'], span_m=span, live_load_kpa=live_load)
    dead_loads = loads_engine.calculate_dead_loads()
    comb = loads_engine.get_load_combination(dead_loads)
    
    # 3. 결과 표시
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📌 단면 성질 결과")
        st.write(props)
    with col2:
        st.subheader("⚖️ 하중 산정 결과")
        st.write(comb)
