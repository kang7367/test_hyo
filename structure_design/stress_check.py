import numpy as np

class PSCStressChecker:
    """엑셀 image_682661.png의 단계별 응력 합산 및 KDS 허용응력 판정 클래스"""
    def __init__(self, fck_PC, fci_PC, fck_RC=27):
        self.fck_PC = fck_PC
        self.fci_PC = fci_PC
        self.fck_RC = fck_RC
        
    def evaluate_stage(self, stage_name, location, is_top, P_A, M_Z, Pe_Zp=0.0):
        """
        각 단계별/위치별 응력 조합 및 판정
        - M_Z 및 Pe_Zp의 부호는 엑셀 수식의 인장/압축 방향 기준을 따름
        """
        # 1. Stress Sum (엑셀 수식 반영: 각 응력 성분 합산)
        # 인장은 (-), 압축은 (+)로 통일하여 연산
        stress_sum = P_A + Pe_Zp + M_Z
        
        # 2. 단계별 KDS 허용응력(Allowable Stress) 및 판정 기준 설정 (Calculation 열 수식 반영)
        if "Transfer" in stage_name:
            # 도입 시 (At Release)
            allow_comp = 0.60 * self.fci_PC
            allow_tens = -0.5 * np.sqrt(self.fci_PC) if "Center" in location else -0.5 * np.sqrt(self.fci_PC)
            # 엑셀 단면 위치(End/Cen) 특이 수식 반영
            if "Center" in location and is_top:
                allow_tens = -0.25 * np.sqrt(self.fci_PC)
        else:
            # 사용 상태 (At Service)
            if "Topping" in location: # 토핑 콘크리트 구간
                allow_comp = 0.45 * self.fck_RC
                allow_tens = -0.5 * np.sqrt(self.fck_RC)
            else:
                allow_comp = 0.45 * self.fck_PC
                allow_tens = -0.5 * np.sqrt(self.fck_PC)

        # 3. Decision (판정 및 철근보강 여부)
        # 압축응력이 허용압축을 초과하면 NG, 인장응력이 허용인장보다 작으면(절대값이 크면) 철근보강
        if stress_sum > allow_comp:
            decision = "❌ NG (압축 초과)"
            status = "NG"
        elif stress_sum < allow_tens:
            decision = "⚠️ 철근보강 NEED"
            status = "REBAR"
        else:
            decision = "🟢 OK"
            status = "OK"
            
        # 4. Areq (필요 철근량 계산 - 인장 초과 시 소요 단면적 계산식 인하)
        # 엑셀 수식: As = T / (0.6 * fy) 논리 기반 간략화 구조 선행 반영
        areq = 0.0
        if status == "REBAR":
            # 임의의 인장력 T 계산 및 보강면적 도출 예시 수식
            tension_force = abs(stress_sum - allow_tens) * 1000 # 변형량 환산
            areq = tension_force / (0.6 * 500) # fy=500 기준
            
        return {
            "Stress_Sum": stress_sum,
            "Allowable_Stress": allow_comp if stress_sum > 0 else allow_tens,
            "Decision": decision,
            "Areq": areq
        }
