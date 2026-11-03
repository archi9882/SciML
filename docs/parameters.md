# 參數來源與推導

HydroWatch 與 ChannelWatch 的參數，以鯉魚潭水庫集水區為參考，能查到的數據就用查到的，查不到的才採用假設，並標示出來。推導的計算在 `scripts/derive_parameters.py`，重新執行會得到同樣的數字。

**狀態說明**：查證＝搜尋到出處；推導＝由查證的公式與數據計算；假設＝找不到實際數據，採用合理範圍內的值，有實測時請取代；估計＝來源間說法不一或我未能確認單位或對應關係。

**這是練習用的合成資料，不是任何真實測站的紀錄。** 測站座標是示意位置，降雨事件與流量由程式產生。

## 流域與水文

| 參數 | 值 | 狀態 | 來源與推導 |
|---|---|---|---|
| 流域面積 A | 52.77 km² | 查證 | 鯉魚潭水庫集水區面積，[政府資料開放平台](https://data.gov.tw/dataset/58345) |
| 主流長度 L | 13.7 km | 推導（估計） | Hack 定律 L = 1.4 A^0.6，[Hack's law](https://en.wikipedia.org/wiki/Hack%27s_law)。原式用英里與平方英里，這個單位是我的記憶，搜尋結果未確認；係數與測量比例尺有關 |
| 平均坡降 S | 0.03 | 假設 | 景山溪的實測坡降查不到；山區河流的合理值 |
| 集流時間 tc | 116 分鐘 | 推導 | Kirpich 公式（SI）tc = 0.0195 L^0.77 S^-0.385（L 為公尺、tc 為分鐘），[TxDOT](https://www.txdot.gov/manuals/des/hyd/chapter-4--hydrology/section-11--time-of-concentration/the-kirpich-method.html) |
| 滯時 Tlag | 1.16 小時 | 推導 | Tlag = 0.6 tc 的經驗法則，[LMNO](https://www.lmnoeng.com/Hydrology/TimeConc.php) |
| 退水常數 k | 1.2 小時 | 估計 | 單一線性水庫的 k 取近似於滯時；這個對應關係出自水文教科書，未在搜尋結果確認 |
| 逕流係數 C | 0.4 | 假設 | 實測洪峰逕流係數的範圍很寬（臺北市山坡地研究約 0.21 至 1.0），取山區森林集水區偏低值，[論文](https://etheses.lib.ntust.edu.tw/thesis/detail/655a098bc42b7e5a3503346dba20a1c1/?seq=4) |
| 年平均降雨與逕流 | 2,458 mm；逕流比 0.716 | 查證 | 水利署近十年平均降雨 2,458 mm，降雨總量 885 億噸、可用逕流 633.7 億噸，[WRA](https://www.wra.gov.tw/en/cp.aspx?n=5155) |
| 年平均流量 | 2.95 m³/s | 推導 | 2,458 mm × 0.716 × 52.77 km² ÷ 一年；把全臺平均套用在這個集水區，山區實際可能更高 |
| 基流 | 1.18 m³/s | 假設 | 枯水期基流取年平均流量的 0.4 倍 |
| 降雨事件強度 | 午後雷雨 10–30 mm/hr；颱風包絡線 15 mm/hr | 假設 | 臺灣歷史 1 小時雨量紀錄約 200 mm（2010 年蘇澳，轉述自[綠色和平引用的氣象局資料](https://www.greenpeace.org/taiwan/press/25260)，我未核對原始紀錄）；本資料的強度遠低於紀錄值，但沒有以實測事件校準 |
| 資料期間 | 2026 年 8 月 | 假設 | 臺灣夏季為雨季與颱風季；1 月是乾季，不適合用大雨事件 |

## 量測誤差

| 參數 | 值 | 狀態 | 來源 |
|---|---|---|---|
| 雨量計相對誤差 | 5% | 估計 | 傾斗式雨量計準確度等級約 ±3% 至 ±10%，資料來源間說法不一，[JMA 簡報](https://www.jma.go.jp/jma/en/Activities/qmws_2018/Presentation/3.2/Accuracy%20of%20precipitation%20measurements.pdf)；高雨強時傾斗翻轉期間的漏計會造成低估，[Lelièvre](https://observator.com/wp-content/uploads/2019/08/Tipping_Bucket_Rain_Gauges_-_Claude_Lelievre.pdf) |
| 雨量計解析度 | 0.5 mm | 假設 | 常見規格，未查證 |
| 流量相對誤差 | 8% | 估計 | 水位流量曲線 95% 不確定度：簡單斷面中位數流量約 3% 至 17%，外插的高流量可達 41% 至 200%，[USGS](https://pubs.usgs.gov/publication/70169002) |
| 流量站曲線偏移 | +12% | 假設 | 落在上述不確定度範圍內，用來模擬曲線隨時間老化 |

## 河道（明渠水力）

| 參數 | 值 | 狀態 | 來源與推導 |
|---|---|---|---|
| Manning n | 0.050 | 查證 | Chow (1959)：礫石、卵石少量大塊石 0.030–0.050；卵石夾大塊石 0.040–0.070，[Chow 表](https://www.un-spider.org/sites/default/files/Table_Surface_roughness_Manning_n_Chow_1959.pdf)。有實務文章指出陡峭河流與低流量時 Chow 值可能偏低，[Kleinschmidt](https://kleinschmidtgroup.com/ras-post/n-values-in-steep-streams) |
| 河寬 B、坡降 S0 | 30 m、0.01 | 假設 | 山區河道的示意值 |
| 洪水波速 | 14.7 km/hr（4.09 m/s） | 推導 | Manning 寬渠道 β = 5/3，波速 = (5/3) × 流速；β 的來源見 [Ponce](https://ponce.sdsu.edu/is_the_dynamic_hydraulic_diffusivity.html)，「波速等於 β 倍流速」是我的推導，搜尋結果未直接確認。Q = 100 m³/s 時水深 1.36 m、流速 2.45 m/s、Froude 數 0.67 |
| 水力擴散係數 | 167 m²/s = 0.60 km²/hr | 查證 | Hayami：D = q0 / (2 S0)，q0 為單寬流量，[Ponce](https://ponce.sdsu.edu/is_the_dynamic_hydraulic_diffusivity.html)、[mizuRoute](https://mizuroute.readthedocs.io/en/latest/tech_note/diffusive_wave_derivation.html) |

## 水庫與發電

| 參數 | 值 | 狀態 | 來源 |
|---|---|---|---|
| 庫容 | 1.26 億 m³ | 查證 | 鯉魚潭水庫總容量 12,600 萬 m³、壩高 96 m，[經濟部公報水庫分級表](https://gazette2.nat.gov.tw/EG_FileManager/eguploadpub/eg028181/ch04/type2/gov31/num12/images/Eg01.pdf)。設計有效容量查不到 |
| 機組效率 | 0.90 | 查證 | Pelton 整體效率 0.85–0.90，[課程講義與 Verbund](https://www.verbund.com/en-at/about-verbund/power-plants/turbines)；Francis 廠商宣稱高於 90%，[香港機電工程署](https://re.emsd.gov.hk/english/other/hydroelectric/Turbine_types.html) |
| 水頭 | 50–90 m | 假設 | 壩高 96 m 為上限；鯉魚潭的實際發電水頭查不到 |
| 發電放流量 | 2.9 m³/s | 假設 | 取年平均入流量 |
| 發電功率 | 約 1.8–2.3 MW | 推導 | P = ρ g Q H η。作為量級檢查：台電執行中的 10 處小水力（含鯉魚潭景山計畫）合計 26,011 kW，平均約 2.6 MW，[中央社](https://www.cna.com.tw/news/firstnews/202110310023.aspx)；景山個別容量查不到 |

## 尚未查證、需要實測取代的項目

景山溪的主流長度與坡降、鯉魚潭水庫的設計有效容量與發電水頭、實際雨量站與流量站的位置與紀錄、逕流係數的實測值、颱風事件的實測雨型。要取代它們，可向水利署與氣象署申請或下載開放資料。
