from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, date
import pytz
import astral
import astral.sun
import json
import os
from urllib.parse import urlencode

app = Flask(__name__)

# 定义支持的语言和翻译内容
translations = {
    "zh-CN": {
        "title": "跑途网 - 经纬网，日出、日落查询",
        "header": "在线经纬度查询工具",
        "currentLocation": "当前位置：查询工具 > 经纬度查询",
        "provinceHeader": "省市级:",
        "cityHeader": "城市:",
        "areaHeader": "区域:",
        "townHeader": "乡镇/街道:",
        "coordinatesHeader": "定位坐标:",
        "sunHeader": "日出、日落:",
        "isnightHeader": "是否夜晚:",
        "Date": "日期",
        "Dawn": "天亮",
        "Sunrise": "日出",
        "Noon": "正午",
        "Sunset": "日落",
        "Dusk": "天黑",
        "backButton": "返回上一页",
        "homeButton": "返回首页",
        "footerText": "Copyright © 2021-2024 跑途网. All Rights Reserved.",
        "metaDescription": "跑途网提供全国省、市、区县、乡镇街道的经纬度坐标查询，以及任意地点的日出、日落、天亮、天黑时间与当前是否夜晚的精准计算。",
        "metaKeywords": "经纬度查询,日出日落,天亮天黑,是否夜晚,乡镇街道坐标,跑途网",
        "ogSiteName": "跑途网",
        "ogLocale": "zh_CN",
        "isNightYes": "是",
        "isNightNo": "否",
        "homeCrumb": "首页"
    },
    "en": {
        "title": "Paotu Net - Coordinate Query Tool, Sunrise and Sunset",
        "header": "Online Coordinate Query Tool",
        "currentLocation": "Current Location: Query Tool > Coordinate Query",
        "provinceHeader": "Provinces:",
        "cityHeader": "Cities:",
        "areaHeader": "Areas:",
        "townHeader": "Towns/Streets:",
        "coordinatesHeader": "Location Coordinates:",
        "sunHeader": "Sunrise and Sunset:",
        "isnightHeader": "Is it Night:",
        "Date": "Date",
        "Dawn": "Dawn",
        "Sunrise": "Sunrise",
        "Noon": "Noon",
        "Sunset": "Sunset",
        "Dusk": "Dusk",
        "backButton": "Go Back",
        "homeButton": "Home",
        "footerText": "Copyright © 2021-2024 Paotu Net. All Rights Reserved.",
        "metaDescription": "Paotu Net provides latitude/longitude lookup for provinces, cities, districts, towns and streets across China, plus accurate sunrise, sunset, dawn, dusk times and day/night status for any location.",
        "metaKeywords": "coordinate query,sunrise sunset,dawn dusk,day night,china towns coordinates,paotu",
        "ogSiteName": "跑途网",
        "ogLocale": "en_US",
        "isNightYes": "Yes",
        "isNightNo": "No",
        "homeCrumb": "Home"
    },
    "zh-TW": {
        "title": "跑途網 - 經緯網，日出、日落查詢",
        "header": "在線經緯度查詢工具",
        "currentLocation": "當前位置：查詢工具 > 經緯度查詢",
        "provinceHeader": "省市級:",
        "cityHeader": "城市:",
        "areaHeader": "區域:",
        "townHeader": "鄉鎮/街道:",
        "coordinatesHeader": "定位坐標:",
        "sunHeader": "日出、日落:",
        "isnightHeader": "是否夜晚:",
        "Date": "日期",
        "Dawn": "天亮",
        "Sunrise": "日出",
        "Noon": "正午",
        "Sunset": "日落",
        "Dusk": "天黑",
        "backButton": "返回上一頁",
        "homeButton": "返回首頁",
        "footerText": "Copyright © 2021-2024 跑途網. All Rights Reserved.",
        "metaDescription": "跑途網提供全國省、市、區縣、鄉鎮街道的經緯度座標查詢，以及任意地點的日出、日落、天亮、天黑時間與目前是否夜晚的精準計算。",
        "metaKeywords": "經緯度查詢,日出日落,天亮天黑,是否夜晚,鄉鎮街道座標,跑途網",
        "ogSiteName": "跑途网",
        "ogLocale": "zh_TW",
        "isNightYes": "是",
        "isNightNo": "否",
        "homeCrumb": "首頁"
    },
    "ja": {
        "title": "パオツネット - 緯度経度、日の出、日の入りの問い合わせ",
        "header": "オンライン緯度経度問い合わせツール",
        "currentLocation": "現在の位置：問い合わせツール > 緯度経度問い合わせ",
        "provinceHeader": "省・市:",
        "cityHeader": "都市:",
        "areaHeader": "地域:",
        "townHeader": "町・街道:",
        "coordinatesHeader": "位置座標:",
        "sunHeader": "日の出、日の入り:",
        "isnightHeader": "夜ですか？:",
        "Date": "日付",
        "Dawn": "明け方",
        "Sunrise": "日の出",
        "Noon": "Noon",
        "Sunset": "日の入り",
        "Dusk": "夕暮れ",
        "backButton": "前のページに戻る",
        "homeButton": "ホーム",
        "footerText": "Copyright © 2021-2024 パオツネット. All Rights Reserved.",
        "metaDescription": "パオツネットは中国全土の省・市・区・町・街道の緯度経度検索と、任意の地点の日の出・日の入り・明け方・夕暮れの時刻および昼夜判定を提供します。",
        "metaKeywords": "緯度経度検索,日の出日の入り,夜かどうか,中国の町座標,パオツネット",
        "ogSiteName": "跑途网",
        "ogLocale": "ja_JP",
        "isNightYes": "はい",
        "isNightNo": "いいえ",
        "homeCrumb": "ホーム"
    },
    "de": {
        "title": "Paotu-Netz - Koordinatenabfrage, Sonnenaufgang und -untergang",
        "header": "Online-Koordinatenabfrage-Tool",
        "currentLocation": "Aktueller Standort: Abfragewerkzeug > Koordinatenabfrage",
        "provinceHeader": "Provinzen:",
        "cityHeader": "Städte:",
        "areaHeader": "Bereiche:",
        "townHeader": "Gemeinden/Straßen:",
        "coordinatesHeader": "Standortkoordinaten:",
        "sunHeader": "Sonnenaufgang und -untergang:",
        "isnightHeader": "Ist es Nacht:",
        "Date": "Datum",
        "Dawn": "Dämmerung",
        "Sunrise": "Sonnenaufgang",
        "Noon": "Mittag",
        "Sunset": "Sonnenuntergang",
        "Dusk": "Dämmerung",
        "backButton": "Zurück",
        "homeButton": "Startseite",
        "footerText": "Copyright © 2021-2024 Paotu-Netz. Alle Rechte vorbehalten.",
        "metaDescription": "Paotu-Netz bietet Längen- und Breitengrade für Provinzen, Städte, Bezirke, Gemeinden und Straßen in China sowie genaue Sonnenaufgang-, Sonnenuntergang- und Dämmerungszeiten und Tag/Nacht-Status.",
        "metaKeywords": "Koordinaten,Paotu-Netz,Sonnenaufgang,Sonnenuntergang,Tag Nacht,China",
        "ogSiteName": "跑途网",
        "ogLocale": "de_DE",
        "isNightYes": "Ja",
        "isNightNo": "Nein",
        "homeCrumb": "Startseite"
    },
    "ru": {
        "title": "Пауто Сеть - Запрос координат, восход и заход солнца",
        "header": "Онлайн инструмент запроса координат",
        "currentLocation": "Текущее местоположение: Инструмент запроса > Запрос координат",
        "provinceHeader": "Провинции:",
        "cityHeader": "Города:",
        "areaHeader": "Районы:",
        "townHeader": "Волости/Улицы:",
        "coordinatesHeader": "Координаты местоположения:",
        "sunHeader": "Восход и заход солнца:",
        "isnightHeader": "Ночь ли сейчас:",
        "Date": "Дата",
        "Dawn": "Рассвет",
        "Sunrise": "Восход солнца",
        "Noon": "Полдень",
        "Sunset": "Закат",
        "Dusk": "Сумерки",
        "backButton": "Назад",
        "homeButton": "На главную",
        "footerText": "Copyright © 2021-2024 Пауто Сеть. Все права защищены.",
        "metaDescription": "Пауто Сеть предоставляет координаты провинций, городов, районов, волостей и улиц Китая, а также точное время восхода, захода солнца и статус день/ночь для любой точки.",
        "metaKeywords": "координаты,восход заход,день ночь,Пауто Сеть,Китай",
        "ogSiteName": "跑途网",
        "ogLocale": "ru_RU",
        "isNightYes": "Да",
        "isNightNo": "Нет",
        "homeCrumb": "Главная"
    },
    "fr": {
        "title": "Paotu Net - Outil de recherche de coordonnées, lever et coucher de soleil",
        "header": "Outil de recherche de coordonnées en ligne",
        "currentLocation": "Emplacement actuel : Outil de recherche > Recherche de coordonnées",
        "provinceHeader": "Provinces :",
        "cityHeader": "Villes :",
        "areaHeader": "Zones :",
        "townHeader": "Cantons/Rues :",
        "coordinatesHeader": "Coordonnées géographiques :",
        "sunHeader": "Lever et coucher du soleil :",
        "isnightHeader": "Est-ce la nuit :",
        "Date": "Date",
        "Dawn": "Aube",
        "Sunrise": "Lever du soleil",
        "Noon": "Midi",
        "Sunset": "Coucher de soleil",
        "Dusk": "Crépuscule",
        "backButton": "Retour",
        "homeButton": "Accueil",
        "footerText": "Copyright © 2021-2024 Paotu Net. Tous droits réservés.",
        "metaDescription": "Paotu Net propose la recherche de coordonnées pour les provinces, villes, districts, cantons et rues de Chine, ainsi que les heures précises de lever/coucher du soleil et le statut jour/nuit.",
        "metaKeywords": "coordonnées,lever coucher soleil,jour nuit,Paotu Net,Chine",
        "ogSiteName": "跑途网",
        "ogLocale": "fr_FR",
        "isNightYes": "Oui",
        "isNightNo": "Non",
        "homeCrumb": "Accueil"
    },
    "es": {
        "title": "Paotu Net - Herramienta de consulta de coordenadas, amanecer y atardecer",
        "header": "Herramienta de consulta de coordenadas en línea",
        "currentLocation": "Ubicación actual: Herramienta de consulta > Consulta de coordenadas",
        "provinceHeader": "Provincias:",
        "cityHeader": "Ciudades:",
        "areaHeader": "Áreas:",
        "townHeader": "Pueblos/Calles:",
        "coordinatesHeader": "Coordenadas de ubicación:",
        "sunHeader": "Amanecer y atardecer:",
        "isnightHeader": "¿Es de noche?",
        "Date": "Fecha",
        "Dawn": "Amanecer",
        "Sunrise": "Salida del sol",
        "Noon": "Mediodía",
        "Sunset": "Puesta del sol",
        "Dusk": "Anochecer",
        "backButton": "Volver",
        "homeButton": "Inicio",
        "footerText": "Copyright © 2021-2024 Paotu Net. Todos los derechos reservados.",
        "metaDescription": "Paotu Net ofrece coordenadas para provincias, ciudades, distritos, pueblos y calles de China, además de horas precisas de amanecer/atardecer y estado día/noche.",
        "metaKeywords": "coordenadas,amanecer atardecer,día noche,Paotu Net,China",
        "ogSiteName": "跑途网",
        "ogLocale": "es_ES",
        "isNightYes": "Sí",
        "isNightNo": "No",
        "homeCrumb": "Inicio"
    },
    "ar": {
        "title": "شبكة باوتو - أداة استعلام خط العرض والطول، شروق وغروب الشمس",
        "header": "أداة استعلام خط العرض والطول على الإنترنت",
        "currentLocation": "الموقع الحالي: أداة الاستعلام > استعلام خط العرض والطول",
        "provinceHeader": "المقاطعات:",
        "cityHeader": "المدن:",
        "areaHeader": "المناطق:",
        "townHeader": "البلدات/الشوارع:",
        "coordinatesHeader": "إحداثيات الموقع:",
        "sunHeader": "شروق وغروب الشمس:",
        "isnightHeader": "هل هو ليل:",
        "Date": "تاريخ",
        "Dawn": "فجر",
        "Sunrise": "شروق الشمس",
        "Noon": "ظهر",
        "Sunset": "غروب الشمس",
        "Dusk": "غسق",
        "backButton": "العودة إلى الصفحة السابقة",
        "homeButton": "العودة إلى الصفحة الرئيسية",
        "footerText": "حقوق الطبع والنشر © 2021-2024 شبكة باوتو. جميع الحقوق محفوظة.",
        "metaDescription": "شبكة باوتو توفر إحداثيات المقاطعات والمدن والمناطق والبلدات في الصين، مع أوقات دقيقة للشروق والغروب وحالة الليل والنهار.",
        "metaKeywords": "إحداثيات,شروق غروب,ليل نهار,شبكة باوتو,الصين",
        "ogSiteName": "跑途网",
        "ogLocale": "ar_AR",
        "isNightYes": "نعم",
        "isNightNo": "لا",
        "homeCrumb": "الصفحة الرئيسية"
    }
    # 可以添加其他语言的翻译内容...
}

# 默认语言
default_language = 'en'


# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'towns.json')

# 检查文件是否存在
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

# 读取json数据
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取去重后的province
provinces = list(set([d['province'] for d in data]))

def calculate_sun_info(latitude, longitude, date_str, tz_name):
    tz = pytz.timezone(tz_name)
    for_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    l = astral.LocationInfo('Custom Name', 'My Region', tz_name, latitude, longitude)
    s = astral.sun.sun(l.observer, date=for_date)

    result = {}
    for event, time in s.items():
        localized_time = time.astimezone(tz)
        if time < datetime.combine(for_date, datetime.min.time()).replace(tzinfo=tz):
            localized_time += timedelta(days=1)
        elif time > datetime.combine(for_date, datetime.max.time()).replace(tzinfo=tz):
            localized_time -= timedelta(days=1)

        result[event] = localized_time.strftime('%H:%M')
    date = for_date.strftime("%Y-%m-%d")
    sunrise = datetime.strptime(result["sunrise"], "%H:%M")
    sunset = datetime.strptime(result["sunset"], "%H:%M")
    # 计算昼长
    day_length = sunset - sunrise
    day_length_hours = day_length.seconds // 3600
    day_length_minutes = (day_length.seconds % 3600) // 60
    result = {'日期':date, '天亮': result['dawn'], '日出': result['sunrise'], '正午': result['noon'],'日落':  result['sunset'],'天黑':result['dusk'],'昼长': f"{day_length_hours}小时{day_length_minutes}分钟"}
    json_data = json.dumps(result, ensure_ascii=False)
    return json_data

def make_href(lang, province=None, city=None, area=None, town=None):
    """构造带语言与层级参数的站内链接（已做 URL 编码，利于 SEO 与爬虫）。"""
    q = {'lang': lang}
    if province:
        q['province'] = province
    if city:
        q['city'] = city
    if area:
        q['area'] = area
    if town:
        q['town'] = town
    return '/?' + urlencode(q)


def get_sun_days(latitude, longitude, tz_name, days=15):
    """返回未来 days 天的日出日落数据（列表），逐日累加自动跨月/跨年。"""
    tz = pytz.timezone(tz_name)
    base = datetime.now(tz).date()
    rows = []
    for i in range(days):
        d = base + timedelta(days=i)
        rows.append(json.loads(calculate_sun_info(latitude, longitude, d.strftime('%Y-%m-%d'), tz_name)))
    return rows


def compute_isnight(latitude, longitude, tz_name):
    tz = pytz.timezone(tz_name)
    today = datetime.now(tz).strftime('%Y-%m-%d')
    info = json.loads(calculate_sun_info(latitude, longitude, today, tz_name))
    sunrise = datetime.strptime(info['日出'], '%H:%M').time()
    sunset = datetime.strptime(info['日落'], '%H:%M').time()
    now = datetime.now(tz).time()
    return 'True' if (now < sunrise or now > sunset) else 'False'


TZ = 'asia/shanghai'


@app.route('/')
def index():
    # ---- 语言 ----
    user_lang = request.args.get('lang')
    if not user_lang:
        user_lang = request.accept_languages.best_match(translations.keys(), default=default_language)
    if user_lang not in translations:
        user_lang = default_language
    lang = user_lang
    t = translations[lang]

    # ---- 层级参数 ----
    province = request.args.get('province')
    city = request.args.get('city')
    area = request.args.get('area')
    town = request.args.get('town')
    try:
        days = max(1, min(int(request.args.get('days', 15)), 60))
    except (ValueError, TypeError):
        days = 15

    home_href = make_href(lang)

    # ---- 判定当前层级： provinces -> cities -> areas -> towns -> coordinates ----
    if not province:
        level = 'provinces'
    elif not city:
        level = 'cities'
    elif not area:
        level = 'areas'
    elif not town:
        level = 'towns'
    else:
        level = 'coordinates'

    # ---- 面包屑（最后一项为当前页，不可点；首页在首层时也不做链接） ----
    breadcrumb = [(t['homeCrumb'], None if level == 'provinces' else home_href)]
    if province:
        breadcrumb.append((province, make_href(lang, province=province)))
    if city:
        breadcrumb.append((city, make_href(lang, province=province, city=city)))
    if area:
        breadcrumb.append((area, make_href(lang, province=province, city=city, area=area)))
    if town:
        breadcrumb.append((town, None))

    # ---- 当前层级的下钻列表 / 坐标数据 ----
    links = []
    lat = lng = None
    sun_rows = []
    isnight = None
    parent_href = None

    if level == 'provinces':
        links = [(p, make_href(lang, province=p)) for p in sorted(provinces)]
    elif level == 'cities':
        items = sorted(set(d['city'] for d in data if d['province'] == province))
        links = [(c, make_href(lang, province=province, city=c)) for c in items]
        parent_href = home_href
    elif level == 'areas':
        items = sorted(set(d['area'] for d in data if d['province'] == province and d['city'] == city))
        links = [(a, make_href(lang, province=province, city=city, area=a)) for a in items]
        parent_href = make_href(lang, province=province)
    elif level == 'towns':
        items = sorted(set(d['town'] for d in data if d['province'] == province and d['city'] == city and d['area'] == area))
        links = [(w, make_href(lang, province=province, city=city, area=area, town=w)) for w in items]
        parent_href = make_href(lang, province=province, city=city)
    elif level == 'coordinates':
        coords = [d for d in data if d['province'] == province and d['city'] == city and d['area'] == area and d['town'] == town]
        if coords:
            lat = coords[0]['lat']
            lng = coords[0]['lng']
            sun_rows = get_sun_days(lat, lng, TZ, days)
            isnight = compute_isnight(lat, lng, TZ)
        parent_href = make_href(lang, province=province, city=city, area=area)

    # ---- 动态标题与描述（利于搜索引擎收录具体地点页） ----
    raw_names = [x for x in [province, city, area, town] if x]
    # 直辖市等 province==city 会出现连续重复，去掉相邻重复让标题/面包屑更干净
    path_names = []
    for n in raw_names:
        if not path_names or path_names[-1] != n:
            path_names.append(n)
    if level == 'provinces':
        page_title = t['title']
    else:
        page_title = ' '.join(path_names) + ' - ' + t['ogSiteName']

    if level == 'coordinates' and lang in ('zh-CN', 'zh-TW') and sun_rows:
        page_description = ('%s（%s）的经纬度为 %s, %s；未来%d天日出约 %s、日落约 %s。提供精准的日出日落与昼夜查询。'
                            % (town, area, lat, lng, days, sun_rows[0]['日出'], sun_rows[0]['日落']))
    else:
        page_description = t['metaDescription']

    # ---- 规范链接 / OG 链接（去掉 partial 参数） ----
    clean_q = request.args.to_dict()
    clean_q.pop('partial', None)
    page_url = request.base_url
    if clean_q:
        page_url += '?' + urlencode(clean_q)

    ctx = dict(translations=translations, language=lang, t=t, level=level,
               breadcrumb=breadcrumb, links=links,
               province=province, city=city, area=area, town=town,
               lat=lat, lng=lng, sun_rows=sun_rows, isnight=isnight,
               home_href=home_href, parent_href=parent_href,
               page_title=page_title, page_description=page_description,
               page_url=page_url, days=days)

    # AJAX 局部刷新：只返回主体内容
    if request.args.get('partial') == '1':
        return render_template('content.html', **ctx), 200, {'Content-Type': 'text/html; charset=utf-8'}

    return render_template('index.html', **ctx)


#@app.route('/')
#def index():
#    return render_template('index.html', provinces=provinces)

@app.route('/location')
def location():
    province = request.args.get('province')
    city = request.args.get('city')
    area = request.args.get('area')
    town = request.args.get('town')

    if province and city and area and town:
        coordinates = [d for d in data if d['province'] == province and d['city'] == city and d['area'] == area and d['town'] == town]
        return jsonify(coordinates)
    elif province and city and area:
        towns = list(set([d['town'] for d in data if d['province'] == province and d['city'] == city and d['area'] == area]))
        return jsonify(towns)
    elif province and city:
        areas = list(set([d['area'] for d in data if d['province'] == province and d['city'] == city]))
        return jsonify(areas)
    elif province:
        cities = list(set([d['city'] for d in data if d['province'] == province]))
        return jsonify(cities)
    else:
        return jsonify(provinces)

@app.route('/sun', methods=['POST', 'GET'])
def get_sun_info():
    if request.method == 'POST':
        req = request.get_json()
        latitude = req['latitude']
        longitude = req['longitude']
        tz_name = req['timezone']
        tz = pytz.timezone(tz_name)
        if req['date'] == 'today':
            date_str = datetime.now(tz).strftime("%Y-%m-%d")
        else:
            date_str = req['date']
        try:
            days = int(req.get('days', 1))
        except (ValueError, TypeError):
            days = 1
    elif request.method == 'GET':
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        tz_name = request.args.get('timezone')
        tz = pytz.timezone(tz_name)
        if request.args.get('date') == 'today':
            date_str = datetime.now(tz).strftime("%Y-%m-%d")
        else:
            date_str = request.args.get('date')
        try:
            days = int(request.args.get('days', 1))
        except (ValueError, TypeError):
            days = 1

    # 限制天数范围，避免异常参数
    days = max(1, min(days, 60))
    # 以本地“今天”为基准，逐日累加，自动处理跨月/跨年
    base_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    results = []
    for i in range(days):
        d = base_date + timedelta(days=i)
        results.append(json.loads(calculate_sun_info(latitude, longitude, d.strftime('%Y-%m-%d'), tz_name)))

    # days==1 时仍返回单条对象，保持对旧调用（直接打开 /sun 链接）的兼容
    payload = json.dumps(results[0], ensure_ascii=False) if days == 1 else json.dumps(results, ensure_ascii=False)
    return payload, 200, {"content-type": "application/json"}

@app.route('/isnight', methods=['POST', 'GET'])
def isnight():
    if request.method == 'POST':
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']
        tz_name = data['timezone']
        tz = pytz.timezone(tz_name)
        if data['date'] == 'today':
            today = datetime.now(tz)
            date_str = today.strftime("%Y-%m-%d")
        else:
            date_str = data['date']
    elif request.method == 'GET':
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        tz_name = request.args.get('timezone')
        tz = pytz.timezone(tz_name)
        if request.args.get('date') == 'today':
            today = datetime.now(tz)
            date_str = today.strftime("%Y-%m-%d")
        else:
            date_str = request.args.get('date')
    current_time = datetime.now(tz).strftime('%H:%M')
    result = calculate_sun_info(latitude, longitude, date_str, tz_name)
    data = json.loads(result)

    # 解析日出和日落时间
    sunrise_time = datetime.strptime(data['日出'], '%H:%M').time()
    sunset_time = datetime.strptime(data['日落'], '%H:%M').time()

    if datetime.strptime(current_time, '%H:%M').time() < sunrise_time or datetime.strptime(current_time, '%H:%M').time() > sunset_time:
        result = 'True'
    else:
        result = 'False'
    return result


@app.route('/robots.txt')
def robots():
    body = "User-agent: *\nAllow: /\nSitemap: " + request.host_url + "sitemap.xml\n"
    return body, 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/sitemap.xml')
def sitemap():
    base = request.host_url.rstrip('/')
    urls = [base + '/']
    for lang in translations.keys():
        urls.append(base + '/?lang=' + lang)
    # 省级与市级入口：爬虫从这些页面顺着真实 <a href> 链接即可爬到乡镇/街道
    for p in provinces:
        urls.append(base + '/?' + urlencode({'lang': default_language, 'province': p}))
    seen = set()
    for d in data:
        key = (d['province'], d['city'])
        if key in seen:
            continue
        seen.add(key)
        urls.append(base + '/?' + urlencode({'lang': default_language, 'province': d['province'], 'city': d['city']}))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml += '  <url><loc>' + u + '</loc></url>\n'
    xml += '</urlset>\n'
    return xml, 200, {'Content-Type': 'application/xml; charset=utf-8'}


if __name__ == '__main__':
    # 端口优先读取环境变量 PORT（Vercel 会自动注入），本地调试可指定以避开占用端口
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
