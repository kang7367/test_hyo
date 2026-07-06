import streamlit as st
import pandas as pd
import numpy as np

# 1. 앱 제목과 간단한 텍스트
st.title('내 생애 첫 Streamlit 앱 🎈')
st.write('Streamlit을 사용하면 파이썬 코드로 쉽게 웹 대시보드를 만들 수 있습니다.')

st.divider() # 구분선

# 2. 사용자 입력 위젯 (텍스트 입력 및 슬라이더)
st.header('사용자 입력 테스트')
name = st.text_input('이름을 입력하세요:', '홍길동')
age = st.slider('나이를 선택하세요:', 0, 100, 25)

st.success(f'안녕하세요, **{name}**님! 선택하신 나이는 **{age}**세입니다.')

# 3. 간단한 데이터프레임 및 차트 시각화
st.header('간단한 데이터 시각화')
st.write('Numpy를 이용해 생성한 랜덤 데이터를 라인 차트로 그립니다.')

# 랜덤 데이터 생성 (20행 3열)
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A (서울)', 'B (부산)', 'C (제주)']
)

# 데이터프레임 표출
st.dataframe(chart_data)

# 라인 차트 표출
st.line_chart(chart_data)
