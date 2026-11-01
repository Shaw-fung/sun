from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, date
import pytz
import astral
import astral.sun
import json
import os
import time
import urllib.request
from urllib.parse import urlencode
from geo_i18n import display_name, title_name, romanize

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
        "homeCrumb": "首页",
        "weatherHeader": "天气预报",
        "weatherFuture": "未来几天",
        "weatherHourly": "未来24小时",
        "weatherLoading": "天气预报加载中…",
        "weatherError": "天气数据获取失败，请稍后重试。",
        "weatherStale": "天气数据可能略有延迟（使用近期缓存）。",
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
        "homeCrumb": "Home",
        "weatherHeader": "Weather Forecast",
        "weatherFuture": "Next Days",
        "weatherHourly": "Next 24 hours",
        "weatherLoading": "Loading weather forecast…",
        "weatherError": "Failed to load weather. Please retry later.",
        "weatherStale": "Weather data may be slightly delayed (served from recent cache).",
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
        "homeCrumb": "首頁",
        "weatherHeader": "天氣預報",
        "weatherFuture": "未來幾天",
        "weatherHourly": "未來24小時",
        "weatherLoading": "天氣預報載入中…",
        "weatherError": "天氣資料取得失敗，請稍後重試。",
        "weatherStale": "天氣資料可能略有延遲（使用近期快取）。",
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
        "homeCrumb": "ホーム",
        "weatherHeader": "天気予報",
        "weatherFuture": "今後の天気",
        "weatherHourly": "今後24時間",
        "weatherLoading": "天気予報を読み込み中…",
        "weatherError": "天気データの取得に失敗しました。後ほどお試しください。",
        "weatherStale": "天気データはわずかに遅延している可能性があります（直近のキャッシュを使用）。",
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
        "homeCrumb": "Startseite",
        "weatherHeader": "Wettervorhersage",
        "weatherFuture": "Nächste Tage",
        "weatherHourly": "Nächste 24 Stunden",
        "weatherLoading": "Wettervorhersage wird geladen…",
        "weatherError": "Wetterdaten konnten nicht geladen werden. Bitte erneut versuchen.",
        "weatherStale": "Wetterdaten können leicht verzögert sein (aus aktuellem Cache).",
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
        "homeCrumb": "Главная",
        "weatherHeader": "Прогноз погоды",
        "weatherFuture": "Ближайшие дни",
        "weatherHourly": "Ближайшие 24 часа",
        "weatherLoading": "Загрузка прогноза погоды…",
        "weatherError": "Не удалось загрузить данные о погоде. Попробуйте позже.",
        "weatherStale": "Данные о погоде могут быть слегка устаревшими (используется кэш).",
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
        "homeCrumb": "Accueil",
        "weatherHeader": "Prévisions météo",
        "weatherFuture": "Prochains jours",
        "weatherHourly": "Prochaines 24 heures",
        "weatherLoading": "Chargement des prévisions…",
        "weatherError": "Échec du chargement météo. Veuillez réessayer.",
        "weatherStale": "Données météo potentiellement légèrement retardées (depuis le cache récent).",
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
        "homeCrumb": "Inicio",
        "weatherHeader": "Pronóstico del tiempo",
        "weatherFuture": "Próximos días",
        "weatherHourly": "Próximas 24 horas",
        "weatherLoading": "Cargando pronóstico…",
        "weatherError": "No se pudo cargar el clima. Inténtalo más tarde.",
        "weatherStale": "Los datos del clima pueden tener un leve retraso (desde caché reciente).",
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
        "homeCrumb": "الصفحة الرئيسية",
        "weatherHeader": "توقعات الطقس",
        "weatherFuture": "الأيام القادمة",
        "weatherHourly": "الساعات الـ 24 القادمة",
        "weatherLoading": "جارٍ تحميل توقعات الطقس…",
        "weatherError": "تعذر تحميل بيانات الطقس. حاول مرة أخرى لاحقًا.",
        "weatherStale": "قد تكون بيانات الطقس متأخرة قليلاً (مأخوذة من ذاكرة التخزين المؤقت الأخيرة).",
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


def alt_href(lang):
    """构造同一地点、不同语言版本的完整 URL（用于 hreflang / 多语言 sitemap）。
    保留当前省/市/区县/乡镇路径，仅替换 lang 参数。"""
    q = {}
    for k in ('province', 'city', 'area', 'town'):
        v = request.args.get(k)
        if v:
            q[k] = v
    q['lang'] = lang
    return request.host_url.rstrip('/') + '/?' + urlencode(q)


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

# WMO 天气代码 -> (emoji, [9 语言文案]) 标准映射（Open-Meteo 返回数值代码）
# 语言顺序固定为 LANGS，新增语言时同步维护
LANGS = ['zh-CN', 'zh-TW', 'en', 'ja', 'de', 'ru', 'fr', 'es', 'ar']
WMO = {
    0:  ('☀️', ['晴', '晴', 'Clear sky', '晴れ', 'Klar', 'Ясно', 'Ciel dégagé', 'Despejado', 'صافٍ']),
    1:  ('🌤️', ['大致晴朗', '大致晴朗', 'Mainly clear', '大体晴れ', 'Überwiegend klar', 'Преимущественно ясно', 'Plutôt dégagé', 'Principalmente despejado', 'صافٍ تقريبًا']),
    2:  ('⛅', ['局部多云', '局部多雲', 'Partly cloudy', '薄曇り', 'Teilweise bewölkt', 'Переменная облачность', 'Partiellement nuageux', 'Parcialmente nublado', 'غائم جزئياً']),
    3:  ('☁️', ['阴', '陰', 'Overcast', '曇り', 'Bewölkt', 'Пасмурно', 'Nuageux', 'Nublado', 'غائم']),
    45: ('🌫️', ['雾', '霧', 'Fog', '霧', 'Nebel', 'Туман', 'Brouillard', 'Niebla', 'ضباب']),
    48: ('🌫️', ['雾凇', '霧凇', 'Rime fog', '樹霜', 'Reifnebel', 'Изморозь', 'Brouillard givrant', 'Niebla helada', 'ضباب متجمد']),
    51: ('🌦️', ['小毛毛雨', '小毛毛雨', 'Light drizzle', '弱い霧雨', 'Leichter Nieselregen', 'Слабая морось', 'Bruine faible', 'Llovizna leve', 'رذاذ خفيف']),
    53: ('🌦️', ['毛毛雨', '毛毛雨', 'Moderate drizzle', '霧雨', 'Mäßiger Nieselregen', 'Умеренная морось', 'Bruine modérée', 'Llovizna moderada', 'رذاذ معتدل']),
    55: ('🌧️', ['大毛毛雨', '大毛毛雨', 'Dense drizzle', '強い霧雨', 'Dichter Nieselregen', 'Сильная морось', 'Bruine dense', 'Llovizna densa', 'رذاذ كثيف']),
    56: ('🌧️', ['冻毛毛雨', '凍毛毛雨', 'Light freezing drizzle', '弱い着氷性霧雨', 'Leichter gefrierender Niesel', 'Слабая ледяная морось', 'Bruine verglaçante faible', 'Llovizna congelante leve', 'رذاذ متجمد خفيف']),
    57: ('🌧️', ['强冻毛毛雨', '強凍毛毛雨', 'Dense freezing drizzle', '強い着氷性霧雨', 'Dichter gefrierender Niesel', 'Сильная ледяная морось', 'Bruine verglaçante dense', 'Llovizna congelante densa', 'رذاذ متجمد كثيف']),
    61: ('🌧️', ['小雨', '小雨', 'Slight rain', '弱い雨', 'Leichter Regen', 'Небольшой дождь', 'Pluie faible', 'Lluvia leve', 'مطر خفيف']),
    63: ('🌧️', ['中雨', '中雨', 'Moderate rain', '雨', 'Mäßiger Regen', 'Умеренный дождь', 'Pluie modérée', 'Lluvia moderada', 'مطر معتدل']),
    65: ('🌧️', ['大雨', '大雨', 'Heavy rain', '強い雨', 'Starker Regen', 'Сильный дождь', 'Pluie forte', 'Lluvia intensa', 'مطر غزير']),
    66: ('🌧️', ['冻雨', '凍雨', 'Light freezing rain', '弱い着氷性の雨', 'Leichter Gefrierregen', 'Слабый ледяной дождь', 'Pluie verglaçante faible', 'Lluvia engelante leve', 'مطر متجمد خفيف']),
    67: ('🌧️', ['强冻雨', '強凍雨', 'Heavy freezing rain', '強い着氷性の雨', 'Starker Gefrierregen', 'Сильный ледяной дождь', 'Pluie verglaçante forte', 'Lluvia engelante intensa', 'مطر متجمد غزير']),
    71: ('🌨️', ['小雪', '小雪', 'Slight snow', '弱い雪', 'Leichter Schneefall', 'Небольшой снег', 'Neige faible', 'Nieve leve', 'ثلج خفيف']),
    73: ('🌨️', ['中雪', '中雪', 'Moderate snow', '雪', 'Mäßiger Schneefall', 'Умеренный снег', 'Neige modérée', 'Nieve moderada', 'ثلج معتدل']),
    75: ('🌨️', ['大雪', '大雪', 'Heavy snow', '強い雪', 'Starker Schneefall', 'Сильный снег', 'Neige forte', 'Nieve intensa', 'ثلج غزير']),
    77: ('🌨️', ['雪粒', '雪粒', 'Snow grains', '雪粒', 'Schneegriesel', 'Снежная крупа', 'Grains de neige', 'Granos de nieve', 'حبيبات ثلجية']),
    80: ('🌦️', ['小阵雨', '小陣雨', 'Slight rain showers', '弱いにわか雨', 'Leichte Regenschauer', 'Кратковременный небольшой дождь', 'Averses de pluie faibles', 'Chubascos leves', 'زخات مطر خفيفة']),
    81: ('🌦️', ['阵雨', '陣雨', 'Moderate rain showers', 'にわか雨', 'Mäßige Regenschauer', 'Кратковременный дождь', 'Averses de pluie modérées', 'Chubascos moderados', 'زخات مطر معتدلة']),
    82: ('🌧️', ['强阵雨', '強陣雨', 'Violent rain showers', '強いにわか雨', 'Heftige Regenschauer', 'Сильный ливень', 'Fortes averses', 'Chubascos violentos', 'زخات مطر غزيرة']),
    85: ('🌨️', ['小阵雪', '小陣雪', 'Slight snow showers', '弱いにわか雪', 'Leichte Schneeschauer', 'Кратковременный небольшой снег', 'Averses de neige faibles', 'Chubascos de nieve leves', 'زخات ثلج خفيفة']),
    86: ('🌨️', ['大阵雪', '大陣雪', 'Heavy snow showers', '強いにわか雪', 'Heftige Schneeschauer', 'Сильный снегопад', 'Fortes averses de neige', 'Chubascos de nieve intensos', 'زخات ثلج غزيرة']),
    95: ('⛈️', ['雷阵雨', '雷陣雨', 'Thunderstorm', '雷雨', 'Gewitter', 'Гроза', 'Orage', 'Tormenta', 'عاصفة رعدية']),
    96: ('⛈️', ['雷阵雨伴小冰雹', '雷陣雨伴小冰雹', 'Thunderstorm w/ slight hail', '雷雨（小さなひょう）', 'Gewitter mit leichtem Hagel', 'Гроза с небольшим градом', 'Orage avec grêle faible', 'Tormenta con granizo leve', 'عاصفة رعدية مع برد خفيف']),
    99: ('⛈️', ['雷阵雨伴大冰雹', '雷陣雨伴大冰雹', 'Thunderstorm w/ heavy hail', '雷雨（大きなひょう）', 'Gewitter mit starkem Hagel', 'Гроза с крупным градом', 'Orage avec grêle forte', 'Tormenta con granizo intenso', 'عاصفة رعدية مع برد غزير']),
}
UNKNOWN = {'zh-CN': '未知', 'zh-TW': '未知', 'en': 'Unknown', 'ja': '不明', 'de': 'Unbekannt',
           'ru': 'Неизвестно', 'fr': 'Inconnu', 'es': 'Desconocido', 'ar': 'غير معروف'}


def wmo(code, lang):
    """返回 (emoji, 该语言文案)。code 为 WMO 数值代码。"""
    entry = WMO.get(code)
    if entry is None:
        return ('🌡️', UNKNOWN.get(lang, 'Unknown'))
    emoji, texts = entry
    try:
        idx = LANGS.index(lang)
    except ValueError:
        idx = 2  # 默认英文
    return (emoji, texts[idx])


# ---- 天气预报：超时 + 内存缓存(备用) 机制 ----
# 为避免 Open-Meteo 网络问题/波动把本服务拖垮：
# 1) 请求设超时，最长 WEATHER_TIMEOUT 秒即放弃；
# 2) 成功结果写入内存缓存，TTL 内复用；
# 3) 上游异常时，若有未过期缓存则回退缓存(标注 stale)，否则返回 None 由页面优雅降级。
# 注：缓存仅存于进程内存（非落盘），符合「不保存本地」约定，仅作容灾备用。
WEATHER_TIMEOUT = 6          # 单次请求超时（秒）
WEATHER_RETRIES = 2           # 实时拉取重试次数（应对瞬时网络抖动）
WEATHER_CACHE_TTL = 1800     # 备用缓存有效期（秒，30 分钟）
_WEATHER_CACHE = {}


def _shape_weather(raw, tz_iana, lang):
    """把 Open-Meteo 原始 JSON 整理为页面所需结构（含 9 语言文案）。"""
    hourly = raw.get('hourly', {})
    daily = raw.get('daily', {})
    htimes = hourly.get('time', [])
    htemps = hourly.get('temperature_2m', [])
    hcodes = hourly.get('weather_code', [])
    hhum = hourly.get('relative_humidity_2m', [])
    hwind = hourly.get('wind_speed_10m', [])
    try:
        today_dt = datetime.now(pytz.timezone(tz_iana))
    except Exception:
        today_dt = datetime.now()
    # 取当前时区的“墙钟时间”（去掉时区信息，与 Open-Meteo 返回的本地时间字符串对齐）
    now_local = today_dt.replace(tzinfo=None)
    today_str = now_local.strftime('%Y-%m-%d')
    # 窗口：当前整点起，未来 24 小时（含当前小时，共 24 个逐小时节点）
    window_start = now_local.replace(minute=0, second=0, microsecond=0)
    window_end = window_start + timedelta(hours=24)

    today_hours = []
    for i, ts in enumerate(htimes):
        try:
            dt = datetime.strptime(ts, '%Y-%m-%dT%H:%M')
        except Exception:
            continue
        if window_start <= dt < window_end:
            code = int(hcodes[i]) if i < len(hcodes) and hcodes[i] is not None else None
            emoji, txt = wmo(code, lang)
            today_hours.append({
                'time': dt.strftime('%m-%d %H:%M'),
                'temp': htemps[i] if i < len(htemps) else None,
                'text': txt,
                'emoji': emoji,
                'humidity': hhum[i] if i < len(hhum) else None,
                'wind': hwind[i] if i < len(hwind) else None,
            })

    days_list = []
    dtimes = daily.get('time', [])
    dcodes = daily.get('weather_code', [])
    dtmax = daily.get('temperature_2m_max', [])
    dtmin = daily.get('temperature_2m_min', [])
    for i, ds in enumerate(dtimes):
        code = int(dcodes[i]) if i < len(dcodes) and dcodes[i] is not None else None
        emoji, txt = wmo(code, lang)
        days_list.append({
            'date': ds,
            'text': txt,
            'emoji': emoji,
            'tmax': dtmax[i] if i < len(dtmax) else None,
            'tmin': dtmin[i] if i < len(dtmin) else None,
        })

    cur = raw.get('current')
    current = None
    if cur:
        code = cur.get('weather_code')
        emoji, txt = wmo(code, lang)
        current = {
            'temp': cur.get('temperature_2m'),
            'text': txt,
            'emoji': emoji,
            'humidity': cur.get('relative_humidity_2m'),
            'wind': cur.get('wind_speed_10m'),
        }

    return {'today': today_str, 'current': current, 'hours': today_hours, 'days': days_list}


def fetch_weather(lat, lng, tz_iana, days=16, lang='en'):
    """获取天气预报，带超时、重试与内存缓存(备用)机制。
    返回整理后的 dict（含 stale 标记）；完全不可达且无缓存时返回 None。
    lat/lng 可能来自 JSON 字符串，先统一转 float，避免 round() 抛异常。"""
    try:
        lat = float(lat)
        lng = float(lng)
    except (TypeError, ValueError):
        return None
    key = (round(lat, 3), round(lng, 3), lang)
    url = ('https://api.open-meteo.com/v1/forecast'
           '?latitude=%.5f&longitude=%.5f'
           '&current=temperature_2m,weather_code,relative_humidity_2m,wind_speed_10m'
           '&hourly=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m'
           '&daily=weather_code,temperature_2m_max,temperature_2m_min'
           '&timezone=%s&forecast_days=%d' % (lat, lng, tz_iana, days))
    raw = None
    last_err = None
    # 重试：应对瞬时网络抖动（最多 WEATHER_RETRIES 次，每次独立超时）
    for attempt in range(WEATHER_RETRIES):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'paotu-sun/1.0'})
            with urllib.request.urlopen(req, timeout=WEATHER_TIMEOUT) as resp:
                raw = json.loads(resp.read().decode('utf-8'))
            break
        except Exception as e:
            last_err = e
            continue
    if raw is not None:
        data = _shape_weather(raw, tz_iana, lang)
        data['stale'] = False
        _WEATHER_CACHE[key] = {'ts': time.time(), 'data': data}
        return data
    # 实时拉取失败：回退到未过期的内存缓存（标注 stale）；无缓存则降级
    cached = _WEATHER_CACHE.get(key)
    if cached and (time.time() - cached['ts']) < WEATHER_CACHE_TTL:
        d = dict(cached['data'])
        d['stale'] = True
        return d
    return None

# Open-Meteo 使用 IANA 时区（Asia/Shanghai），本应用内部用 asia/shanghai
TZ_IANA = {
    'asia/shanghai': 'Asia/Shanghai',
}


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
    # 非中文语言下，地名显示为「外文（中文）」形式，便于外国用户识别与被搜索到
    breadcrumb = [(t['homeCrumb'], None if level == 'provinces' else home_href)]
    if province:
        breadcrumb.append((display_name(province, lang), make_href(lang, province=province)))
    if city:
        breadcrumb.append((display_name(city, lang), make_href(lang, province=province, city=city)))
    if area:
        breadcrumb.append((display_name(area, lang), make_href(lang, province=province, city=city, area=area)))
    if town:
        breadcrumb.append((display_name(town, lang), None))

    # ---- 当前层级的下钻列表 / 坐标数据 ----
    links = []
    lat = lng = None
    sun_rows = []
    isnight = None
    weather = None
    parent_href = None

    if level == 'provinces':
        links = [(display_name(p, lang), make_href(lang, province=p)) for p in sorted(provinces)]
    elif level == 'cities':
        items = sorted(set(d['city'] for d in data if d['province'] == province))
        links = [(display_name(c, lang), make_href(lang, province=province, city=c)) for c in items]
        parent_href = home_href
    elif level == 'areas':
        items = sorted(set(d['area'] for d in data if d['province'] == province and d['city'] == city))
        links = [(display_name(a, lang), make_href(lang, province=province, city=city, area=a)) for a in items]
        parent_href = make_href(lang, province=province)
    elif level == 'towns':
        items = sorted(set(d['town'] for d in data if d['province'] == province and d['city'] == city and d['area'] == area))
        links = [(display_name(w, lang), make_href(lang, province=province, city=city, area=area, town=w)) for w in items]
        parent_href = make_href(lang, province=province, city=city)
    elif level == 'coordinates':
        coords = [d for d in data if d['province'] == province and d['city'] == city and d['area'] == area and d['town'] == town]
        if coords:
            lat = coords[0]['lat']
            lng = coords[0]['lng']
            sun_rows = get_sun_days(lat, lng, TZ, days)
            isnight = compute_isnight(lat, lng, TZ)
            # 服务端渲染天气预报（带超时 + 内存缓存备用机制，失败优雅降级）
            tz_iana = TZ_IANA.get(TZ, TZ)
            try:
                weather = fetch_weather(lat, lng, tz_iana, 16, lang)
            except Exception:
                weather = None
        parent_href = make_href(lang, province=province, city=city, area=area)

    # ---- 动态标题与描述（利于搜索引擎收录具体地点页） ----
    raw_names = [x for x in [province, city, area, town] if x]
    # 直辖市等 province==city 会出现连续重复，去掉相邻重复让标题/面包屑更干净
    path_names = []
    for n in raw_names:
        if not path_names or path_names[-1] != n:
            path_names.append(n)
    # 非中文语言下，标题使用外文/拼音名（不含中文），更利于外语搜索结果显示
    path_titles = [title_name(n, lang) for n in path_names]
    if level == 'provinces':
        page_title = t['title']
    else:
        page_title = ' '.join(path_titles) + ' - ' + t['ogSiteName']

    if level == 'coordinates' and sun_rows:
        if lang in ('zh-CN', 'zh-TW'):
            page_description = ('%s（%s）的经纬度为 %s, %s；未来%d天日出约 %s、日落约 %s。提供精准的日出日落与昼夜查询。'
                                % (town, area, lat, lng, days, sun_rows[0]['日出'], sun_rows[0]['日落']))
        else:
            # 外语版本：外文名（中文）并含经纬度与日出日落，兼顾中文与外文检索
            page_description = ('%s (%s): latitude %s, longitude %s. Sunrise around %s, sunset around %s. %s'
                                % (title_name(town, lang), town, lat, lng,
                                   sun_rows[0]['日出'], sun_rows[0]['日落'], t['metaDescription']))
    else:
        page_description = t['metaDescription']

    # ---- 规范链接 / OG 链接（去掉 partial 参数） ----
    clean_q = request.args.to_dict()
    clean_q.pop('partial', None)
    page_url = request.base_url
    if clean_q:
        page_url += '?' + urlencode(clean_q)

    # ---- 多语言 hreflang 备用链接（同一地点各语言版本的 URL，用于 SEO 收录） ----
    hreflangs = [(code, alt_href(code)) for code in LANGS]
    hreflangs.append(('x-default', alt_href(default_language)))
    # 坐标页标题处用到的地名展示（外文（中文）/ 中文）
    town_disp = display_name(town, lang) if town else ''

    ctx = dict(translations=translations, language=lang, t=t, level=level,
               breadcrumb=breadcrumb, links=links,
               province=province, city=city, area=area, town=town, town_disp=town_disp,
               lat=lat, lng=lng, sun_rows=sun_rows, isnight=isnight, weather=weather,
               home_href=home_href, parent_href=parent_href,
               page_title=page_title, page_description=page_description,
               page_url=page_url, days=days, hreflangs=hreflangs)

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
        tz_name = req.get('timezone') or TZ
        tz = pytz.timezone(tz_name)
        date_param = req.get('date')
        if date_param == 'today' or not date_param:
            date_str = datetime.now(tz).strftime("%Y-%m-%d")
        else:
            date_str = date_param
        try:
            days = int(req.get('days', 1))
        except (ValueError, TypeError):
            days = 1
    elif request.method == 'GET':
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        tz_name = request.args.get('timezone') or TZ
        tz = pytz.timezone(tz_name)
        date_param = request.args.get('date')
        if date_param == 'today' or not date_param:
            date_str = datetime.now(tz).strftime("%Y-%m-%d")
        else:
            date_str = date_param
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
        tz_name = data.get('timezone') or TZ
        tz = pytz.timezone(tz_name)
        date_param = data.get('date')
        if date_param == 'today' or not date_param:
            date_str = datetime.now(tz).strftime("%Y-%m-%d")
        else:
            date_str = date_param
    elif request.method == 'GET':
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        tz_name = request.args.get('timezone') or TZ
        tz = pytz.timezone(tz_name)
        date_param = request.args.get('date')
        if date_param == 'today' or not date_param:
            date_str = datetime.now(tz).strftime("%Y-%m-%d")
        else:
            date_str = date_param
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


@app.route('/weather')
def weather():
    """代理 Open-Meteo 天气预报（免密钥、直接实时调用网络，不落本地存储）。
    按经纬度返回：current 当前实况 / hours 当前时间起未来24小时逐小时 / days 后续日期整天概要。
    带超时 + 内存缓存(备用)机制，上游异常时回退缓存并标记 stale；完全不可用返回 ok=False。"""
    try:
        lat = float(request.args.get('latitude'))
        lng = float(request.args.get('longitude'))
    except (TypeError, ValueError):
        return jsonify({'ok': False, 'error': 'invalid coordinates'}), 400

    tz_in = request.args.get('timezone', 'asia/shanghai')
    tz_iana = TZ_IANA.get(tz_in, tz_in)
    lang = request.args.get('lang', 'en')
    try:
        days = max(1, min(int(request.args.get('days', 16)), 16))
    except (ValueError, TypeError):
        days = 16

    data = fetch_weather(lat, lng, tz_iana, days, lang)
    if data is None:
        return jsonify({'ok': False, 'error': 'weather service unavailable'}), 503
    out = dict(data)
    out['ok'] = True
    out['tz'] = tz_iana
    return jsonify(out)


@app.route('/robots.txt')
def robots():
    body = "User-agent: *\nAllow: /\nSitemap: " + request.host_url + "sitemap.xml\n"
    return body, 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/sitemap.xml')
def sitemap():
    base = request.host_url.rstrip('/')

    def entry(loc_params):
        """构造一个 sitemap 条目：主 loc + 各语言 alternate 链接。"""
        loc = base + '/?' + urlencode(loc_params)
        alts = []
        for code in LANGS:
            p = dict(loc_params)
            p['lang'] = code
            alts.append((code, base + '/?' + urlencode(p)))
        # x-default 指向默认语言版本
        d = dict(loc_params)
        d['lang'] = default_language
        alts.append(('x-default', base + '/?' + urlencode(d)))
        return loc, alts

    entries = []
    # 首页（含各语言）
    entries.append(entry({'lang': default_language}))
    # 省级入口
    for p in provinces:
        entries.append(entry({'lang': default_language, 'province': p}))
    # 市级入口：爬虫从这些页面顺着真实 <a href> 链接即可爬到区县/乡镇/街道
    seen = set()
    for d in data:
        key = (d['province'], d['city'])
        if key in seen:
            continue
        seen.add(key)
        entries.append(entry({'lang': default_language, 'province': d['province'], 'city': d['city']}))

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '\
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    for loc, alts in entries:
        xml += '  <url><loc>' + loc + '</loc>'
        for code, u in alts:
            xml += '<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (code, u)
        xml += '</url>\n'
    xml += '</urlset>\n'
    return xml, 200, {'Content-Type': 'application/xml; charset=utf-8'}


if __name__ == '__main__':
    # 端口优先读取环境变量 PORT（Vercel 会自动注入），本地调试可指定以避开占用端口
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
