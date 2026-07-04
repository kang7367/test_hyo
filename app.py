import streamlit as st
import numpy as np

# 브라우저 탭 타이틀 및 레이아웃 설정
st.set_page_config(page_title="신효정 - PSC 거더 설계 검증 시스템", layout="wide")

# 애플리케이션 최상단 타이틀 추가
st.title("👤 신효정")
st.subheader("🏗️ PSC 거더 단계별 응력 및 검증 시스템 (KDS 기준)")
st.write("엑셀 시트의 KDS 설계 기준 연산 논리 및 수치를 검증하는 프로토타입 대시보드입니다.")

# 사이드바: 기본 스펙 및 재료 변수 입력
st.sidebar.header("1. 입력 변수 (Spec)")
fck_PC = st.sidebar.number_input("fck_PC (거더 강도, MPa)", value=40)
fck_RC = st.sidebar.number_input("fck_RC (토핑 강도, MPa)", value=27)

fci_factor = st.sidebar.slider("fci/fck 비율", 0.5, 1.0, 0.7)
fci_PC = fck_PC * fci_factor

# KDS 기준 배합강도(fcu) 자동 연산식
fcu_PC = fck_PC + 4 if fck_PC <= 40 else fck_PC + 6
fcu_RC = fck_RC + 4 if fck_RC <= 40 else fck_RC + 6

st.sidebar.markdown("---")
st.sidebar.write(f"🔹 **거더 배합강도(fcu_PC):** {fcu_PC} MPa")
st.sidebar.write(f"🔹 **도입시강도(fci_PC):** {fci_PC:.1f} MPa")

# KDS 탄성계수 간편식 ( 보통중량골재 기준 Ec = 8500 * fcu^(1/3) )
Ec_PC = 8500 * (fcu_PC ** (1/3))
Eci_PC = 8500 * (fci_PC ** (1/3))
Ec_RC = 8500 * (fcu_RC ** (1/3))

st.sidebar.write(f"🔹 **거더 탄성계수(Ec):** {Ec_PC:.0f} MPa")
st.sidebar.write(f"🔹 **도입시 탄성계수(Eci):** {Eci_PC:.0f} MPa")

st.sidebar.markdown("---")
st.sidebar.subheader("단면 변수")
L = st.sidebar.number_input("부재 길이 Span (m)", value=17.6)
A_cross = st.sidebar.number_input("단면적 A (mm²)", value=500000)
Z_top = st.sidebar.number_input("단면계수 Z_top (mm³)", value=150000000)
Z_bot = st.sidebar.number_input("단면계수 Z_bot (mm³)", value=150000000)

# 메인 화면: 결과값 입력 및 크로스 검증
col1, col2 = st.columns(2)
with col1:
    st.subheader("📌 검증용 엔지니어 응력 결과값 입력")
    st.caption("엑셀 시트의 Stress Sum 혹은 각 단계별 최종 응력값을 입력하세요.")
    user_top_transfer = st.number_input("도입 시 상단 응력 (MPa)", value=-2.1)
    user_bot_transfer = st.number_input("도입 시 하단 응력 (MPa)", value=22.5)
    user_top_service = st.number_input("사용 상태 상단 응력 (MPa)", value=16.5)
    user_bot_service = st.number_input("사용 상태 하단 응력 (MPa)", value=-1.5)

with col2:
    st.subheader("⚖️ KDS 기준 자동 판별 리포트")
    
    # 허용응력 계산 규정
    allow_comp_transfer = 0.6 * fci_PC
    allow_tens_transfer = -0.5 * np.sqrt(fci_PC)
    allow_comp_service = 0.45 * fck_PC
    allow_tens_service = -0.5 * np.sqrt(fck_PC)
    
    st.markdown("### 1. 도입 시 (At Release / Transfer Stage) 검증")
    # 상단 인장응력 검증 (음수 영역 비교)
    if user_top_transfer < allow_tens_transfer:
        st.error(f"❌ 상단 인장응력 과다: {user_top_transfer} MPa (허용 한계: {allow_tens_transfer:.2f} MPa) -> [철근보강 NEED]")
    else:
        st.success(f"🟢 상단 응력 적정: {user_top_transfer} MPa (허용 한계: {allow_tens_transfer:.2f} MPa)")
        
    # 하단 압축응력 검증
    if user_bot_transfer > allow_comp_transfer:
        st.error(f"❌ 하단 압축응력 초과 (NG): {user_bot_transfer} MPa (허용 한계: {allow_comp_transfer:.2f} MPa)")
    else:
        st.success(f"🟢 하단 응력 적정 (OK): {user_bot_transfer} MPa (허용 한계: {allow_comp_transfer:.2f} MPa)")

    st.markdown("---")
    st.markdown("### 2. 사용 상태 (Service Stage) 검증")
    # 상단 압축응력 검증
    if user_top_service > allow_comp_service:
        st.error(f"❌ 상단 압축응력 초과 (NG): {user_top_service} MPa (허용 한계: {allow_comp_service:.2f} MPa)")
    else:
        st.success(f"🟢 상단 응력 적정 (OK): {user_top_service} MPa (허용 한계: {allow_comp_service:.2f} MPa)")
        
    # 하단 인장응력 검증
    if user_bot_service < allow_tens_service:
        st.info(f"ℹ️ 하단 인장 상태 판별: {user_bot_service} MPa (균열등급 및 인장 철근 보강 확인 필요)")
    else:
        st.success(f"🟢 하단 응력 적정 (OK): {user_bot_service} MPa (허용 한계: {allow_tens_service:.2f} MPa)")
