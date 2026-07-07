import streamlit as st
import numpy as np

from structure_design.sections import GirderSection
from structure_design.loads import GirderLoads

st.set_page_config(page_title="PSC 설계 플랫폼", layout="wide")

st.title("🏗️ PSC 거더 설계 자동화 플랫폼_ver01")

# 사이드바 입력창
st.sidebar.header("설계 변수 입력")
B = st.sidebar.number_input("전체 폭 (B, mm)", value=1100)
B1 = st.sidebar.number_input("플랜지 제외 폭 (B1, mm)", value=300)
H = st.sidebar.number_input("전체 높이 (H, mm)", value=1080)
H2 = st.sidebar.number_input("하부 플랜지 높이 (H2, mm)", value=450)
span = st.sidebar.number_input("Span (m)", value=11.0)
live_load = st.sidebar.number_input("활하중 (kPa)", value=20.0)

# 설계 실행부
if st.button("설계 검증 실행"):
    # 1. 단면 분석
    girder = GirderSection(B, B1, H, H2)
    props = girder.calculate_properties()
    
    # 2. 하중 및 모멘트 분석
    loads_engine = GirderLoads(girder_area_mm2=props['A_PC'], span_m=span, live_load_kpa=live_load)
    dead_loads = loads_engine.calculate_dead_loads()
    
    # 모멘트 계산 로직 호출
    moments = loads_engine.calculate_moments(dead_loads)
    
    # 결과 시각화
    st.subheader("📊 휨 모멘트 산정 결과 (중앙부)")
    col1, col2, col3 = st.columns(3)
    col1.metric("사하중 모멘트", f"{moments['M_Dead']:.2f} kN·m")
    col2.metric("활하중 모멘트", f"{moments['M_Live']:.2f} kN·m")
    col3.metric("설계 모멘트 (Mu)", f"{moments['Mu_Total']:.2f} kN·m", delta_color="inverse")
