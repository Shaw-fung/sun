# 跑途网 · 经纬度 / 日出日落 / 是否夜晚查询

一个面向全国（省 → 市 → 区县 → 乡镇/街道）的经纬度坐标查询工具，并基于坐标提供**未来 15 天日出、日落、天亮、天黑**以及**当前是否夜晚**的精准计算。支持 9 种语言，已做服务端渲染（SSR）便于搜索引擎收录，并带完整的社交分享卡片（Open Graph / Twitter Card）。

## 功能特性

- **四级下钻查询**：省 → 市 → 区县 → 乡镇/街道 → 经纬度坐标。
- **日出日落**：任一地点显示未来 15 天（可配置）的日期 / 天亮 / 日出 / 正午 / 日落 / 天黑，逐日累加自动跨月、跨年。
- **是否夜晚**：基于当地日出日落实时判断，返回 `True` / `False`。
- **多语言**：简体中文、繁体中文、English、日本語、Deutsch、Русский、Français、Español、العربية，切换语言时停留在当前所在页面。
- **服务端渲染（SSR）**：每一级页面由 Flask 直接输出完整 HTML 与真实 `<a href>` 链接，搜索引擎和爬虫可直接抓取具体地点页（不再依赖前端 AJAX 空容器）。
- **SEO / 社交分享**：
  - 动态 `<title>`、`<meta description>`、`<link canonical>`、Open Graph、Twitter Card、JSON-LD 结构化数据。
  - `robots.txt` 与 `sitemap.xml`（含首页 + 9 语言 + 全部省/市级入口，约 400+ 条）。
  - 分享封面图 `static/og-image.png`（1200×630）。
- **API 接口**：`/sun`、`/isnight`、`/location` 均保留，方便其它程序直接调用。

## 技术架构

- 后端：Python + Flask
- 天文计算：`astral`（日出/日落）+ `pytz`（时区，统一使用 `asia/shanghai`）
- 前端：原生 HTML + Bootstrap 4（CDN）+ jQuery（仅做渐进增强）
- 部署：Vercel（Python Serverless Function），`vercel.json` 将全部流量重写到 `/api`

## 目录结构

```
sun-main/
├── vercel.json              # Vercel 重写规则：/(.*) -> /api
├── README.md
└── api/
    ├── index.py             # Flask 应用：SSR 路由 + /sun /isnight /location /robots.txt /sitemap.xml
    ├── requirements.txt     # flask / pytz / astral
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
pip install flask pytz astral

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
| `timezone` | 是 | 时区，如 `asia/shanghai` |
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
| `timezone` | 是 | 时区 |
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
