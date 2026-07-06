class GirderLoads:
    """PC 거더 하중 산정 및 휨 모멘트 계산 클래스"""
    def __init__(self, girder_area_mm2, span_m, live_load_kpa):
        self.area_m2 = girder_area_mm2 / 1_000_000
        self.span = span_m
        self.live_load = live_load_kpa
        
    def calculate_moments(self, dead_loads, live_load_factor=1.2, dead_load_factor=1.2):
        """
        엑셀 시트 로직: M = factor * w * L^2 / 8 (단순보 기준)
        factor는 위험단면별 위치 계수 (End: 0.125, Cen: 0.5 등)
        """
        # 단위 폭(B)을 고려한 등분포 하중 w (kN/m)
        w_dead = sum(dead_loads.values())
        w_live = self.live_load * 1.1 # 엑셀의 분담폭 고려
        
        # 휨 모멘트 산정 (예: 중앙부 M_cen = w * L^2 / 8)
        # 엑셀의 M_cen 계산 로직을 반영한 계수 적용
        m_dead_cen = (w_dead * (self.span**2)) / 8
        m_live_cen = (w_live * (self.span**2)) / 8
        
        total_m_factored = (dead_load_factor * m_dead_cen) + (live_load_factor * m_live_cen)
        
        return {
            "M_Dead": m_dead_cen,
            "M_Live": m_live_cen,
            "Mu_Total": total_m_factored
        }
