"""由可查證的公式與數據推導 HydroWatch 與 ChannelWatch 的參數。

每個輸入標示來源狀態：
  [查證] 搜尋到出處的數據或公式    [假設] 找不到實際數據，採用合理範圍內的值，需要時請以實測取代
輸出的數字寫在 docs/parameters.md，程式裡的常數要與這裡一致。
執行：python scripts/derive_parameters.py
"""
import math

# --- 流域（以鯉魚潭水庫集水區為參考）---------------------------------------
AREA_KM2 = 52.77            # [查證] 鯉魚潭水庫集水區面積，data.gov.tw/dataset/58345
HACK_C, HACK_R = 1.4, 0.6   # [查證] Hack (1957)：L = 1.4 A^0.6；原式單位為英里與平方英里（單位為我的記憶，搜尋結果未確認）
MEAN_SLOPE = 0.03           # [假設] 山區主流平均坡降；景山溪的實測值查不到

a_mi2 = AREA_KM2 / 2.58999
L_km = 1.60934 * HACK_C * a_mi2 ** HACK_R                      # 主流長度
tc_min = 0.0195 * (L_km * 1000) ** 0.77 * MEAN_SLOPE ** -0.385  # [查證] Kirpich SI 式：L [m]、S [m/m]、tc [min]
tlag_h = 0.6 * tc_min / 60                                      # [查證] 經驗法則 Tlag = 0.6 Tc
K_HOURS = tlag_h            # [假設] 單一線性水庫的退水常數取近似於滯時；此對應關係出自水文教科書，未在搜尋結果確認

# --- 水量 -------------------------------------------------------------------
RAIN_MM, RUNOFF_FRAC = 2458.0, 63.37 / 88.50     # [查證] 水利署：近十年平均降雨 2458 mm；可用逕流 633.7 億噸 / 降雨 885 億噸
annual_runoff_mm = RAIN_MM * RUNOFF_FRAC
mean_q = annual_runoff_mm / 1000 * AREA_KM2 * 1e6 / (365 * 86400)
BASEFLOW_INDEX = 0.4        # [假設] 枯水期基流約為年平均流量的 0.4 倍
baseflow = BASEFLOW_INDEX * mean_q
RUNOFF_COEF = 0.4           # [假設] 實測洪峰逕流係數範圍 0.21 至 1.0（臺北市山坡地研究），取山區森林集水區偏低值

# --- 量測誤差 ----------------------------------------------------------------
RAIN_GAUGE_ERR = 0.05       # [查證] WMO 雨量計等級 ±3% 至 ±10%（資料來源間不一致），取 5%
FLOW_ERR = 0.08             # [查證] 水位流量曲線 95% 不確定度中位數流量約 3% 至 17%，取標準差 8%

# --- 河道（明渠水力）---------------------------------------------------------
B_M, S0, N_MANN = 30.0, 0.01, 0.050   # 河寬 [假設]、河床坡降 [假設]、Manning n [查證] Chow：卵石夾大塊石 0.040 至 0.070，取 0.050
Q_REF = 100.0                         # 參考洪水流量 [m3/s]
q = Q_REF / B_M
h = (q * N_MANN / S0 ** 0.5) ** 0.6   # 寬淺渠道 Manning 正常水深
v = q / h
froude = v / math.sqrt(9.81 * h)
celerity = 5 / 3 * v                  # 運動波波速，Manning 紊流寬渠道 beta=5/3（[查證] 指數；波速 = beta × 流速為我的推導）
diffusivity = Q_REF / (2 * B_M * S0)  # [查證] Hayami：D = q0 / (2 S0)

# --- 水庫與發電 ----------------------------------------------------------------
CAPACITY_MM3 = 126.0        # [查證] 鯉魚潭水庫總容量 12,600 萬 m3
DAM_HEIGHT = 96.0           # [查證] 壩高 96 m
ETA = 0.90                  # [查證] Pelton 整體效率 0.85 至 0.90；Francis 廠商宣稱高於 0.90
Q_TURBINE = round(mean_q, 1)  # [假設] 發電放流量取年平均入流量
HEAD = 70.0                 # [假設] 有效水頭，小於壩高 96 m
power_mw = 1000 * 9.81 * Q_TURBINE * HEAD * ETA / 1e6

if __name__ == "__main__":
    print(f"流域面積 {AREA_KM2} km2；Hack 主流長度 L = {L_km:.1f} km")
    print(f"Kirpich tc = {tc_min:.0f} min = {tc_min/60:.2f} h；滯時 {tlag_h:.2f} h；採用 k = {K_HOURS:.1f} h")
    print(f"年逕流深 {annual_runoff_mm:.0f} mm；年平均流量 {mean_q:.2f} m3/s；基流 {baseflow:.2f} m3/s")
    print(f"河道：Q={Q_REF} m3/s, B={B_M} m, S0={S0}, n={N_MANN} → 水深 {h:.2f} m, 流速 {v:.2f} m/s, Fr={froude:.2f}")
    print(f"  運動波波速 {celerity:.2f} m/s = {celerity*3.6:.1f} km/h；Hayami 擴散係數 {diffusivity:.0f} m2/s = {diffusivity*3.6e-3:.2f} km2/h")
    print(f"發電：Q={Q_TURBINE} m3/s, H={HEAD} m, eta={ETA} → P = {power_mw:.2f} MW（台電 10 處小水力合計 26.0 MW，平均 2.6 MW）")
