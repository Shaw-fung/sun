# 跑途网 · 经纬度 / 日出日落 / 是否夜晚查询

一个面向全国（省 → 市 → 区县 → 乡镇/街道）的经纬度坐标查询工具，并基于坐标提供**未来 15 天日出、日落、天亮、天黑**、**当前是否夜晚**，以及**天气预报**（当前时间起未来 24 小时逐小时 + 后续日期整天概要）的精准查询。支持 9 种语言，已做服务端渲染（SSR）便于搜索引擎收录，并带完整的社交分享卡片（Open Graph / Twitter Card）。

## 功能特性

- **四级下钻查询**：省 → 市 → 区县 → 乡镇/街道 → 经纬度坐标。
- **日出日落**：任一地点显示未来 15 天（可配置）的日期 / 天亮 / 日出 / 正午 / 日落 / 天黑，逐日累加自动跨月、跨年。
- **是否夜晚**：基于当地日出日落实时判断，返回 `True` / `False`。
- **天气预报（服务端渲染 + 容错）**：在乡镇/街道坐标页**服务端直接渲染**当前实况 + 当前时间起未来 24 小时逐小时预报（具体时间点）+ 后续日期整天概要（日期 / 天气 / 最高最低温），搜索引擎可直接收录。数据由后端代理 [Open-Meteo](https://open-meteo.com/)（免密钥、直接实时调用网络，不落本地磁盘），按 WMO 标准天气代码映射为文字与 emoji，并**完整翻译为 9 种语言**，随页面语言切换。
  - **容错机制**：① 单次请求超时（默认 6 秒）即放弃，避免拖垮本服务；② 超时后自动重试（默认 2 次）应对瞬时抖动；③ 成功结果写入**进程内存缓存**（TTL 30 分钟）作为备用，上游异常且无缓存时回退缓存并标注「数据可能略有延迟」；④ 完全不可达且无缓存时优雅显示「暂无法获取」，绝不 500 / 卡死。
- **多语言**：简体中文、繁体中文、English、日本語、Deutsch、Русский、Français、Español、العربية，切换语言时停留在当前所在页面。
  - **地名随语言切换**：除界面文案外，**各级地名（省 / 市 / 区县 / 乡镇 / 街道）也会随语言变化**。中文界面保持纯中文；其它语言下：省级行政区使用通用英文名（如 Beijing / Shanghai / Guangdong），其余层级自动转为拼音罗马化（如 Guang Zhou / Tian He / Hua Ting），并以「外文（中文）」形式展示，便于外国用户识别、也利于非中文搜索引擎收录。
- **服务端渲染（SSR）**：每一级页面由 Flask 直接输出完整 HTML 与真实 `<a href>` 链接，搜索引擎和爬虫可直接抓取具体地点页（不再依赖前端 AJAX 空容器）。
- **SEO / 社交分享**：
  - 动态 `<title>`、`<meta description>`、`<link canonical>`、Open Graph、Twitter Card、JSON-LD 结构化数据（`WebSite` + 含 `inLanguage` 的 `WebPage`）。
  - **多语言 hreflang 备用链接**：每个页面在 `<head>` 输出全部 9 种语言 + `x-default` 的 `<link rel="alternate" hreflang="…">`，指向同一地点的各语言版本，帮助 Google 等正确匹配语种。
  - `robots.txt` 与 `sitemap.xml`：`sitemap.xml` 在每条省/市级入口下附带 9 语言 + `x-default` 的 `<xhtml:link rel="alternate" hreflang="…">`（约 400 条 loc、近 4000 条 hreflang 备用链接）。
  - 非中文页面的标题/描述会包含地名的英文或拼音形式（如 `Guangdong`、`Hua Ting`），正文保留「外文（中文）」，兼顾中文与外文检索。
  - 分享封面图 `static/og-image.png`（1200×630）。
- **API 接口**：`/sun`、`/isnight`、`/location` 均保留，方便其它程序直接调用。

## 技术架构

- 后端：Python + Flask
- 地名多语言：`pypinyin`（拼音罗马化，带进程内缓存）+ 省级英文名映射表（`api/geo_i18n.py`）
- 天文计算：`astral`（日出/日落）+ `pytz`（时区，统一使用 `asia/shanghai`）
- 天气数据：[Open-Meteo](https://open-meteo.com/) 免密钥天气预报 API（后端 `/weather` 路由实时代理，按经纬度直查；含超时 6s、重试 2 次、内存缓存 TTL 30 分钟作容错备用，不落本地磁盘）
- 前端：原生 HTML + Bootstrap 4（CDN）+ jQuery（仅做渐进增强）
- 部署：Vercel（Python Serverless Function），`vercel.json` 将全部流量重写到 `/api`

## 目录结构

```
sun-main/
├── vercel.json              # Vercel 重写规则：/(.*) -> /api
├── README.md
└── api/
    ├── index.py             # Flask 应用：SSR 路由 + /sun /isnight /location /weather /robots.txt /sitemap.xml
    ├── geo_i18n.py          # 地名多语言显示/拼音罗马化（省级英文名 + 拼音），多语言 SEO 关键模块
    ├── requirements.txt     # flask / pytz / astral / pypinyin
    ├── towns.json           # 数据源（约 4.3 万条，含 town 乡镇/街道字段，约 8MB）
    ├── templates/
    │   ├── index.html       # 整页外壳：<head> 动态 SEO/OG 标签 + 语言选择 + #main 容器
    │   └── content.html     # 各层级主体内容（面包屑 + 列表 / 坐标表 + 接口链接），整页与 partial 共用
    └── static/
        ├── sun.js           # 渐进增强：点击下钻走 AJAX+pushState；语言切换保留路径
        ├── og-image.png     # 分享封面图 1200×630
        └── favicon.ico
```

> 注：`api/data.json` 为早期旧数据源（已被 `towns.json` 取代），当前代码不再引用，可安全删除以减少部署体积。

## 数据源说明

- `towns.json` 每条记录字段：`province`（省）、`city`（市）、`area`（区县）、`town`（乡镇/街道）、`lat`、`lng`。
- 每个 `(province, city, area, town)` 唯一且自带经纬度，因此乡镇/街道一级能取到对应坐标再计算日出日落。
- 文件在应用启动时一次性读入内存，后续请求直接基于内存计算，响应通常在毫秒级。

## 本地运行

```bash
# 1. 安装依赖（建议用虚拟环境）
pip install flask pytz astral pypinyin

# 2. 启动（端口走环境变量 PORT，便于避开本机被占用的 5000 端口）
cd api
PORT=5055 python index.py

# 3. 浏览器打开
#    http://127.0.0.1:5055/
```

> 首次启动需要把 8MB 的 `towns.json` 读入内存，会有几秒卡顿，属正常。

## API 接口文档

所有接口均支持 `GET`（部分支持 `POST`）。

### `GET /sun` —— 日出日落查询

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `latitude` | 是 | 纬度 |
| `longitude` | 是 | 经度 |
| `timezone` | 否 | 时区，如 `asia/shanghai`，默认 `asia/shanghai` |
| `date` | 否 | `today` 或 `YYYY-MM-DD`，默认 `today` |
| `days` | 否 | 返回未来天数，1–60，默认 `1` |

- `days=1`：返回单条对象（兼容旧调用）。
- `days>1`：返回数组，逐日累加自动跨月/跨年。

示例：

```
GET /sun?latitude=39.97814&longitude=116.32316&date=today&days=15&timezone=asia/shanghai
```

### `GET /isnight` —— 是否夜晚判断

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `latitude` | 是 | 纬度 |
| `longitude` | 是 | 经度 |
| `timezone` | 否 | 时区，默认 `asia/shanghai` |
| `date` | 否 | `today` 或 `YYYY-MM-DD`，默认 `today` |

返回纯文本 `True` 或 `False`（当前时间早于日出或晚于日落即为夜晚）。

示例：

```
GET /isnight?latitude=39.97814&longitude=116.32316&date=today&timezone=asia/shanghai
```

### `GET /location` —— 层级数据查询

| 参数 | 说明 |
| --- | --- |
| `province` | 传省 → 返回该省下城市列表 |
| `city` | 加传市 → 返回该省市下区县列表 |
| `area` | 加传区县 → 返回该区县下乡镇/街道列表 |
| `town` | 加传乡镇 → 返回该乡镇的经纬度坐标数组 |

不传任何参数返回全国省份列表。

### `GET /weather` —— 天气预报（代理 Open-Meteo）

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `latitude` | 是 | 纬度 |
| `longitude` | 是 | 经度 |
| `timezone` | 否 | 时区，如 `asia/shanghai`，默认 `asia/shanghai` |
| `lang` | 否 | 返回文案语言，`zh-CN`/`zh-TW` 返回中文，其余返回英文，默认 `en` |
| `days` | 否 | 预报天数 1–16，默认 16 |

返回 JSON：

```json
{
  "ok": true,
  "today": "2026-11-01",
  "current": { "temp": 15.6, "text": "晴", "emoji": "☀️", "humidity": 28, "wind": 11.9 },
  "hours": [
    { "time": "00:00", "temp": 7.3, "text": "阴", "emoji": "☁️", "humidity": 78, "wind": 0.7 }
  ],
  "days": [
    { "date": "2026-11-01", "text": "晴", "emoji": "☀️", "tmax": 16.0, "tmin": 5.0 },
    { "date": "2026-11-02", "text": "晴", "emoji": "☀️", "tmax": 14.9, "tmin": 3.0 }
  ]
}
```

- `hours`：含**当前时间起未来 24 小时**逐小时（具体时间点，时间格式 `MM-DD HH:MM`）。
- `days`：含当天在内的整天概要；坐标页展示时从**第二天起**作为「后续日期」展示。
- `stale`：布尔值。`true` 表示本次数据来自内存缓存（上游实时拉取失败时的容错备用），页面会提示「数据可能略有延迟」。
- 天气代码采用 [WMO 标准](https://open-meteo.com/en/docs)（0=晴、3=阴、61=小雨、95=雷阵雨…），由后端映射为 9 种语言的文字 + emoji，`lang` 参数决定返回语言。
- 失败返回 `{"ok": false, "error": "..."}`（非法坐标 400，上游完全不可达且无缓存 503）。

坐标页天气由服务端**直接渲染进 HTML**（SSR，便于收录）；本接口同时保留，供其它程序直接调用。容错机制：单次超时 6s、重试 2 次、内存缓存 TTL 30 分钟作备用（不落本地磁盘）。

示例：

```
GET /weather?latitude=39.97814&longitude=116.32316&timezone=asia/shanghai&lang=zh-CN&days=16
```

### `GET /robots.txt` 与 `GET /sitemap.xml`

分别输出爬虫协议与站点地图（含语言与省/市级入口），供搜索引擎发现与收录。

## SEO 与社交分享说明

- 每个具体地点页都由服务端渲染，标题、描述、规范链接、OG 链接均按当前 URL 动态生成。
- `og:image`、`og:url` 使用 `request.host_url` / `request.url` **动态生成绝对地址**，部署到 Vercel 后自动变为你的真实 https 域名，无需手动修改。
- 微信分享卡片依赖**公网可访问 + 绝对图片地址**。微信有 OG 缓存，上线后首次分享可能仍是旧样式，可用微信公众平台「网页调试工具 / 链接校验」刷新一次再看。

## 部署到 Vercel

1. 把整个 `sun-main/` 推送到 Git 仓库并导入 Vercel，或执行 `vercel` 命令行部署。
2. 确保 `vercel.json` 中的重写规则存在：`{ "rewrites": [{ "source": "/(.*)", "destination": "/api" }] }`。
3. Vercel 会自动安装 `requirements.txt` 中的依赖，并将 `api/index.py` 作为 Python Serverless Function 运行。
4. 部署完成后访问分配的域名即可。

## 注意事项

- **备案号占位**：`index.html` 页脚默认写的是 `ICP备0000号` 占位文本，上线前请替换为你的真实备案号。
- **静态资源**：当前 `static/` 下的文件经 Flask 内置静态路由随函数返回（可用，但非 CDN 加速）。如对加载速度有更高要求，可将 `og-image.png`、`sun.js`、`favicon.ico` 改为 Vercel 静态托管。
- **默认天数**：首页默认展示未来 15 天日出日落，可通过 URL 加 `&days=N`（1–60）调整，或直接改 `index.py` 里的默认值。
- **天气数据来源**：天气预报由后端 `/weather` 实时代理 [Open-Meteo](https://open-meteo.com/)（免费、免密钥）。按你的要求**不落本地存储**，每次请求都实时调用网络；若担心高并发下的速率限制，可在 `/weather` 内加一层短时内存缓存（注意这会与「不保存本地」的约定相冲突，按需取舍）。
