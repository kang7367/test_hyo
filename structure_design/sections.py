class GirderSection:
    """PC 거더 단면 성질 자동 계산 클래스 (KDS 기준 기반)"""
    def __init__(self, B, B1, H, H2):
        self.B = B      # 전체 폭
        self.B1 = B1    # 좌우 플랜지 제외 폭 (수식 기반)
        self.H = H      # 전체 높이
        self.H2 = H2    # 하부 플랜지 높이
        
    def calculate_properties(self):
        # A_PC = (H*B) - (B1 * H2 * 2) 
        area = (self.B * self.H) - (self.B1 * self.H2 * 2)
        
        # I_PC 로직 (엑셀 수식 기반 관성모멘트 계산)
        inertia = (self.B * (self.H**3) / 12) - ((self.B - 2*self.B1) * (self.H2**3) / 12)
        
        yb = self.H / 2
        yt = self.H - yb
        
        return {
            "A_PC": area,
            "I_PC": inertia,
            "yb": yb,
            "yt": yt,
            "Zb": inertia / yb,
            "Zt": inertia / yt
        }
