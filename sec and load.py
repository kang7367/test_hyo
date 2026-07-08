import streamlit as st
import numpy as np

# 페이지 설정
st.set_page_config(page_title="PC Girder 설계 플랫폼", layout="wide")

st.title("🏗️ PC Girder 구조설계 및 하중계산 플랫폼_rev.01")
st.markdown("---")

# -----------------------------------------------------------------------------
# 사이드바: 1. 재료 제원 (Spec) 입력
# -----------------------------------------------------------------------------
st.sidebar.header("1. 재료 제원 (Spec)")

# 콘크리트 강도
fck_PC = st.sidebar.number_input("PC 거더 설계기준강도 (fck_PC, MPa)", value=45)
fck_RC = st.sidebar.number_input("RC 슬래브 설계기준강도 (fck_RC, MPa)", value=27)

# 콘크리트 탄성계수 자동 계산 (KDS 기준 반영 수식)
Ec_PC = 8500 * (fck_PC ** (1/3))
Ec_RC = 8500 * (fck_RC ** (1/3))
fci_PC = fck_PC * 0.75  # 긴장재 인장 시 강도 (75%)

st.sidebar.markdown(f"**PC 탄성계수 (Ec_PC):** {Ec_PC:.0f} MPa")
st.sidebar.markdown(f"**RC 탄성계수 (Ec_RC):** {Ec_RC:.0f} MPa")
st.sidebar.markdown(f"**인장 시 PC강도 (fci_PC):** {fci_PC:.1f} MPa")

st.sidebar.markdown("---")

# 강재 제원
fy = st.sidebar.number_input("철근 항복강도 (fy, MPa)", value=600)
fys = st.sidebar.number_input("전단철근 항복강도 (fys, MPa)", value=500)
fpu = st.sidebar.number_input("강연선 인장강도 (fpu, MPa)", value=1860)

# 긴장력 및 손실률
fpj_ratio = 0.75
fpj = fpu * fpj_ratio
initial_loss = 0.10
final_loss = 0.05
fpi = fpj * (1 - initial_loss)
fpe = fpj * (1 - (initial_loss + final_loss))

st.sidebar.markdown(f"**초기 긴장응력 (fpj):** {fpj:.1f} MPa")
st.sidebar.markdown(f"**정착 직후 응력 (fpi):** {fpi:.1f} MPa")
st.sidebar.markdown(f"**유효 응력 (fpe):** {fpe:.1f} MPa")


# -----------------------------------------------------------------------------
# 메인 화면: 단면 및 하중 계산
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📐 단면 제원 입력 및 계산", "⚖️ 하중 및 부재력 산정", "📊 응력 검토 수치"])

with tab1:
    st.header("凸형 단면 및 합성 단면 제원")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("PC 거더 기하형상 입력")
        B = st.number_input("상부 플랜지 폭 (B, mm)", value=1400)
        B2 = st.number_input("복부 폭 (B2, mm)", value=1100)
        H = st.number_input("거더 전체 높이 (H, mm)", value=1200)
        h2 = st.number_input("하부 플랜지 높이 관련 변수 (h2, mm)", value=680)
        
        # 凸형 보 단면 자동 계산을 위한 보조 변수 설정 (시트 수식 반영)
        H1 = 950
        H2 = H - H1
        B1 = (B - B2) / 2 if B != B2 else 0
        h1 = H1 - h2
        
    with col2:
        st.subheader("슬래브 및 강연선 배치")
        slab_type = st.selectbox("PC 슬래브 종류", ["HCS350 (N)", "HCS300 (E)", "HCS320 (N)", "HCS400 (N)", "HCS500 (N)"])
        # HCS 자중 매핑 (시트 내 VLOOKUP 대용)
        hcs_weight_map = {"HCS300 (E)": 3.51, "HCS320 (N)": 3.73, "HCS350 (N)": 3.91, "HCS400 (N)": 4.29, "HCS500 (N)": 5.29}
        hcs_weight = hcs_weight_map.get(slab_type, 3.91)
        
        top_g = st.number_input("토핑 두께 (Top'g, mm)", value=150)
        aps_ea = 138.7  # Φ15.2 단면적
        n_strand = st.number_input("강연선 개수 (ea)", value=46)
        aps_total = n_strand * aps_ea
        
        st.markdown(f"**선택된 HCS 자중:** {hcs_weight} $kN/m^2$")
        st.markdown(f"**총 강연선 단면적 ($A_{{ps}}$):** {aps_total:.1f} $mm^2$")

    st.markdown("---")
    st.subheader("단면 성능 계산 결과 (Section Properties)")
    
    # 텍스트 내 수식 기반 단면적 계산 복원
    # A_PC = (B * H1) - (B1 * h1) * 2  (형상 수식 유추 반영)
    A_PC = (B * H) - (B1 * h1) * 2 
    
    # 예시용 도심 및 단면이차모멘트 (정밀 기하학 수식 대입 가능 구역)
    yb = H / 2  # 임시 대칭 기준 도심
    yt = H - yb
    I_PC = (B * (H**3)) / 12  # 임시 사각 단순화 수식 (추후 돌출형 상세수식 치환 가능)
    Zb = I_PC / yb
    Zt = I_PC / yt
    
    # 합성 단면 성능 (토핑 슬래브 포함)
    b_f = B2  # T형보 유효폭 등 기준 적용 변수
    A_composite = A_PC + (top_g * b_f) # 임시 합성 면적 수식
    
    c1, c2, c3 = st.columns(3)
    c1.metric(label="PC 기더 단면적 ($A_{PC}$)", value=f"{A_PC:,.0f} mm²")
    c2.metric(label="단면이차모멘트 ($I_{PC}$)", value=f"{I_PC:,.3e} mm⁴")
    c3.metric(label="합성 단면적 ($A_{composite}$)", value=f"{A_composite:,.0f} mm²")

with tab2:
    st.header("하중 설정 및 부재력(모멘트/전단력) 산정")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("배치 및 스팬 제원")
        span = st.number_input("지간 (Span, m)", value=17.2)
        trib_width = st.number_input("분담폭 (m)", value=10.8)
        col_width = st.number_input("기둥 폭 (m)", value=1.1)
        
    with col2:
        st.subheader("설계 하중 입력 ($kN/m^2$)")
        finished_load = st.number_input("마감 고정하중 (Finished)", value=8.4)
        live_load = st.number_input("설계 활하중 (Live Load)", value=25.0)

    # 하중 계산 처리 (kN/m 단위 변환)
    # 1. 거더 자중 = 단면적(m^2) * 24 kN/m^3
    girder_sw_knm = (A_PC / 10**6) * 24 
    # 2. HCS 자중 = 자중 * 분담폭
    hcs_sw_knm = hcs_weight * trib_width
    # 3. 토핑 자중 = 두께(m) * 분담폭 * 24 kN/m^3
    topping_sw_knm = (top_g / 1000) * trib_width * 24
    # 4. 마감 하중 = 마감 * 분담폭
    fin_load_knm = finished_load * trib_width
    # 5. 활하중 = 활하중 * 분담폭
    live_load_knm = live_load * trib_width
    
    total_dl_knm = girder_sw_knm + hcs_sw_knm + topping_sw_knm + fin_load_knm
    factored_load_knm = (1.2 * total_dl_knm) + (1.6 * live_load_knm)
    
    st.markdown("---")
    st.subheader("계산된 등분포하중 ($kN/m$)")
    
    lc1, lc2, lc3, lc4 = st.columns(4)
    lc1.markdown(f"**PC 거더 자중:** {girder_sw_knm:.2f} kN/m")
    lc2.markdown(f"**PC 슬래브 자중:** {hcs_sw_knm:.2f} kN/m")
    lc3.markdown(f"**토핑 콘크리트 자중:** {topping_sw_knm:.2f} kN/m")
    lc4.markdown(f"**마감 고정하중:** {fin_load_knm:.2f} kN/m")
    
    st.info(f"👉 **계수설계하중 ($w_u$):** {factored_load_knm:.2f} kN/m  (1.2DL + 1.6LL)")
    
    st.markdown("---")
    st.subheader("위험단면 부재력 결과")
    
    # 중앙부 최대 휨모멘트 (M = w * L^2 / 8)
    M_max = (factored_load_knm * (span**2)) / 8
    # 단부 최대 전단력 (V = w * L / 2)
    V_max = (factored_load_knm * span) / 2
    
    mc1, mc2 = st.columns(2)
    mc1.metric(label="✨ 중앙부 계수모멘트 ($M_u$)", value=f"{M_max:,.1f} kN·m")
    mc2.metric(label="⚡ 단부 계수전단력 ($V_u$)", value=f"{V_max:,.1f} kN")

with tab3:
    st.header("프리스트레스 힘 및 허용응력 검토")
    
    # 긴장력 계산 (kN 변환)
    Pj = (fpj * aps_total) / 1000
    Pi = (fpi * aps_total) / 1000
    Pe = (fpe * aps_total) / 1000
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("단계별 긴장력 (Prestressed Force)")
        st.markdown(f"**초기 긴장력 ($P_j$):** {Pj:,.1f} kN")
        st.markdown(f"**정착 직후 긴장력 ($P_i$):** {Pi:,.1f} kN")
        st.markdown(f"**유효 긴장력 ($P_e$):** {Pe:,.1f} kN")
        
    with col2:
        st.subheader("콘크리트 허용 응력 기준 (KDS)")
        crack_limit_1 = 0.63 * np.sqrt(fck_PC)
        crack_limit_2 = 1.0 * np.sqrt(fck_PC)
        comp_limit = 0.45 * fck_PC
        
        st.markdown(f"**인장 균열 응력 기준 1 ($0.63\sqrt{{f_{{ck}}}}$):** {crack_limit_1:.2f} MPa")
        st.markdown(f"**인장 균열 응력 기준 2 ($1.0\sqrt{{f_{{ck}}}}$):** {crack_limit_2:.2f} MPa")
        st.markdown(f"**압축 허용 응력 기준 ($0.45f_{{ck}}$):** {comp_limit:.2f} MPa")
        
    st.success("💡 설계 자동화 준비 완료: 위 탭의 입력 파라미터를 변경하면 하중과 부재력이 실시간 연동됩니다.")
