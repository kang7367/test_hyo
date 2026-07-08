import streamlit as st
import numpy as np

# 페이지 설정
st.set_page_config(page_title="PC Girder 설계 플랫폼 (정밀 연동)", layout="wide")

st.title("🏗️ PC Girder 구조설계 및 하중계산 플랫폼_rev.01")
st.markdown("---")

# -----------------------------------------------------------------------------
# 사이드바: 1. 재료 제원 (Spec) 입력
# -----------------------------------------------------------------------------
st.sidebar.header("1. 재료 제원 (Spec)")

fck_PC = st.sidebar.number_input("PC 거더 설계기준강도 (fck_PC, MPa)", value=45)
fck_RC = st.sidebar.number_input("RC 슬래브 설계기준강도 (fck_RC, MPa)", value=27)

Ec_PC = 8500 * (fck_PC ** (1/3))
Ec_RC = 8500 * (fck_RC ** (1/3))
fci_PC = fck_PC * 0.75  

st.sidebar.markdown(f"**PC 탄성계수 (Ec_PC):** {Ec_PC:.0f} MPa")
st.sidebar.markdown(f"**RC 탄성계수 (Ec_RC):** {Ec_RC:.0f} MPa")
st.sidebar.markdown("---")

fy = st.sidebar.number_input("철근 항복강도 (fy, MPa)", value=600)
fpu = st.sidebar.number_input("강연선 인장강도 (fpu, MPa)", value=1860)
fpe = fpu * 0.75 * (1 - 0.15)

# -----------------------------------------------------------------------------
# 메인 화면: 단면 및 하중 계산
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📐 정밀 단면 제원", "⚖️ 하중 및 부재력 산정 (완전 연동)", "📊 응력 검토"])

with tab1:
    st.header("凸형 단면 및 합성 단면 제원")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("PC 거더 凸형 기하형상 입력")
        B = st.number_input("상부 플랜지 총 폭 (B, mm)", value=1400) 
        B2 = st.number_input("복부 폭 (B2, mm)", value=1100) 
        H = st.number_input("거더 전체 높이 (H, mm)", value=1200) 
        h2 = st.number_input("하부 변수 (h2, mm)", value=680) 
        
        B1 = (B - B2) / 2 if B != B2 else 0 
        h1 = H - h2 
        
    with col2:
        st.subheader("슬래브 및 강연선 배치")
        slab_type = st.selectbox("PC 슬래브 종류", ["HCS350 (N)", "HCS300 (E)", "HCS320 (N)", "HCS400 (N)", "HCS500 (N)"])
        hcs_weight_map = {"HCS300 (E)": 3.51, "HCS320 (N)": 3.73, "HCS350 (N)": 3.91, "HCS400 (N)": 4.29, "HCS500 (N)": 5.29}
        hcs_weight = hcs_weight_map.get(slab_type, 3.91) 
        
        top_g = st.number_input("토핑 두께 (Top'g, mm)", value=150)
        n_strand = st.number_input("강연선 개수 (ea)", value=46)
        aps_total = n_strand * 138.7

    st.markdown("---")
    A_PC = (B * H) - (B1 * h1) * 2 
    st.subheader("단면 성능 계산 결과")
    st.metric(label="정밀 PC 거더 단면적 ($A_{PC}$)", value=f"{A_PC:,.0f} mm²")

with tab2:
    st.header("하중 설정 및 위험단면 부재력 결과")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("배치 및 스팬 제원")
        span = st.number_input("기준 지간 (Span, m)", value=17.2) 
        trib_width = st.number_input("분담폭 (m)", value=10.8) 
        col_width = st.number_input("기둥 폭 (m)", value=1.1)
        girder_set_len = st.number_input("거더 거치 길이 (mm)", value=50)
        
    with col2:
        st.subheader("설계 하중 입력 ($kN/m^2$)")
        finished_load = st.number_input("마감 고정하중 (Finished)", value=8.4) 
        live_load = st.number_input("설계 활하중 (Live Load)", value=25.0) 

    # 1. 등분포하중 산정 (kN/m)
    w_girder = (A_PC / 10**6) * 24 
    w_hcs = hcs_weight * trib_width
    w_topping = (top_g / 1000) * 24 * trib_width
    w_fin = finished_load * trib_width
    w_live = live_load * trib_width
    
    st.markdown("---")
