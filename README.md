# 寶寶副食食材庫（Baby First Foods）

一個「AI 友善 + Google 友善」的利基資料型網站。每種副食品食材一頁，答案放最前面、
結構化資料 + FAQ + Schema 標記，目標是成為 AI 與搜尋引擎在「某食材幾個月可以吃」
這類問題上會引用的來源。

> 定位：這是要養大、之後可轉售的**商業資產**，使用獨立品牌（非又瑄個人 Yuzu 品牌）。
> 權威來源為 WHO、AAP、CDC、台灣兒科醫學會等公開指引，不以個人名義掛保證。

---

## 架構：資料驅動的生成器（重要）

整站由「一份資料檔 + 一支生成腳本」產生，**不要手改 HTML**：

```
data/foods.json   ← 唯一的內容來源（single source of truth）
generate.py       ← 讀 JSON，產生所有頁面
   └─> foods/*.html、index.html、sitemap.xml、llms.txt
```

改內容、加食材，一律改 `data/foods.json`，然後重跑：

```bash
python generate.py
```

手改 `foods/*.html` 會在下次生成時被覆蓋。

---

## 目前內容（21 種食材）

- **水果類**：酪梨、香蕉、蘋果、梨子、木瓜、葡萄（嗆噎提醒）
- **根莖類**：地瓜、南瓜、馬鈴薯
- **蔬菜類**：紅蘿蔔、綠花椰菜、豌豆
- **穀物類**：嬰兒米精、燕麥
- **蛋白質類**：雞蛋（致敏）、豆腐（致敏）、雞肉、鮭魚（致敏）、花生（致敏）
- **特別注意**：蜂蜜（未滿 1 歲禁）、牛奶（1 歲後當主飲）

致敏原與高風險食材（蜂蜜、牛奶、雞蛋、花生、鮭魚、葡萄）的關鍵事實已對照
WHO / AAP（HealthyChildren）/ CDC 查證。

---

## 怎麼新增一種食材

1. 在 `data/foods.json` 的 `foods` 陣列加一筆，欄位參考既有食材：
   - `slug / name_zh / name_en / emoji / category`
   - `card_meta / card_tag / card_tag_class`（`low` 綠 / `allergen` 琥珀 / `warn` 紅）
   - `answer`（答案優先一句話）、`facts`（自訂事實欄位陣列）
   - `prep_heading / prep`（步驟）、`nutrition`、`faq`
   - 可選 `safety_title / safety_note`（紅色警告框）
   - 可選 `sources_key`：`"allergen_sources"`（致敏/高風險食材用，會引用 AAP/CDC）
2. 重跑 `python generate.py`。
3. index、sitemap、llms.txt 會自動一起更新。

> **內容正確性**：結構性事實（月齡、致敏、處理、嗆噎、蜂蜜/牛奶時程）以指引為準；
> **熱量／營養為概估值**，規模化時建議對照 USDA 或衛福部食藥署「食品營養成分資料庫」核對。

---

## 🚀 上線步驟（C）

1. 決定正式網域與 repo 名稱。
2. 改 `generate.py` 最上方的 `DOMAIN`（例如 `https://firstbites.tw`），
   並把 `robots.txt` 最後一行 `Sitemap:` 的網域一併改成相同網域。
3. 重跑 `python generate.py`（會更新所有 canonical 與 sitemap）。
4. 推到一個**獨立的 GitHub repo**（不要混進個人 Yuzu hub），開啟 GitHub Pages。
   - 本機無 `gh` CLI、git 全域無 user：commit 前在 repo 內設
     `git config user.email ianian22493@gmail.com` / `user.name ianian22493`。
   - 若用自訂網域，於 repo 加 `CNAME` 檔並在網域商設定 DNS。
5. 到 Google Search Console 驗證網站、提交 `sitemap.xml`。
6. 用 [Rich Results Test](https://search.google.com/test/rich-results) 驗證
   FAQ / MedicalWebPage 結構化資料被正確解析。

---

## AI 友善地基（已內建）

- `robots.txt`：放行 GPTBot、ClaudeBot、PerplexityBot、Google-Extended 等 AI 爬蟲。
- `llms.txt`：給 AI 的網站導覽（生成器自動更新食材清單）。
- 每頁 `MedicalWebPage` + `FAQPage` 結構化標記、`citation`（WHO/AAP/台兒醫）、canonical、OG。
- 答案優先排版（結論放最上面，AI 最容易整段引用）。
- 純靜態、無需 JS 即可讀取主要內容，載入快、爬蟲友善。

---

## 本機預覽

`.claude/launch.json` 已有 `babyfood` 設定（python http.server，port 3010，
指向本資料夾）。改完內容重跑 `generate.py` 後重整即可。
