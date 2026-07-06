class GirderLoads:
    """PC 거더 하중 산정 및 조합 계산 클래스"""
    def __init__(self, girder_area_mm2, span_m, live_load_kpa):
        self.area_m2 = girder_area_mm2 / 1_000_000  # mm2 to m2
        self.span = span_m
        self.live_load = live_load_kpa
        
    def calculate_dead_loads(self, concrete_density=25.0):
        """
        고정하중 산정: Girder S.W, PC Slab S.W, Finished
        density: kN/m3 (일반적으로 25.0 적용)
        """
        sw_girder = self.area_m2 * concrete_density
        # 예시로 고정 하중값들 정의 (엑셀 시트 연동 가능)
        dead_loads = {
            "Girder_SW": sw_girder,
            "Finished": 1.1  # 기본값 kN/m
        }
        return dead_loads

    def get_load_combination(self, dead_loads, live_load_factor=1.2, dead_load_factor=1.2):
        """
        사용하중 및 계수하중 조합 (image_a5b649.png 로직 반영)
        """
        sum_dead = sum(dead_loads.values())
        service_load = sum_dead + self.live_load
        factored_load = (dead_load_factor * sum_dead) + (live_load_factor * self.live_load)
        
        return {
            "Service_Load": service_load,
            "Factored_Load": factored_load
        }
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
