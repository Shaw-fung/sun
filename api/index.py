from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, date
import pytz
import astral
import astral.sun
import json
import os

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
        "footerText": "Copyright © 2021-2024 跑途网. All Rights Reserved."
    },
    "en": {
        "title": "Paotu Net - Coordinate Query Tool, Sunrise and Sunset",
        "header": "Online Coordinate Query Tool",
        "currentLocation": "Current Location: Query Tool > Coordinate Query",
        "provinceHeader": "Provinces:",
        "cityHeader": "Cities:",
        "areaHeader": "Areas:",
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
        "footerText": "Copyright © 2021-2024 Paotu Net. All Rights Reserved."
    },
    "zh-TW": {
        "title": "跑途網 - 經緯網，日出、日落查詢",
        "header": "在線經緯度查詢工具",
        "currentLocation": "當前位置：查詢工具 > 經緯度查詢",
        "provinceHeader": "省市級:",
        "cityHeader": "城市:",
        "areaHeader": "區域:",
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
        "footerText": "Copyright © 2021-2024 跑途網. All Rights Reserved."
    },
    "ja": {
        "title": "パオツネット - 緯度経度、日の出、日の入りの問い合わせ",
        "header": "オンライン緯度経度問い合わせツール",
        "currentLocation": "現在の位置：問い合わせツール > 緯度経度問い合わせ",
        "provinceHeader": "省・市:",
        "cityHeader": "都市:",
        "areaHeader": "地域:",
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
        "footerText": "Copyright © 2021-2024 パオツネット. All Rights Reserved."
    },
    "de": {
        "title": "Paotu-Netz - Koordinatenabfrage, Sonnenaufgang und -untergang",
        "header": "Online-Koordinatenabfrage-Tool",
        "currentLocation": "Aktueller Standort: Abfragewerkzeug > Koordinatenabfrage",
        "provinceHeader": "Provinzen:",
        "cityHeader": "Städte:",
        "areaHeader": "Bereiche:",
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
        "footerText": "Copyright © 2021-2024 Paotu-Netz. Alle Rechte vorbehalten."
    },
    "ru": {
        "title": "Пауто Сеть - Запрос координат, восход и заход солнца",
        "header": "Онлайн инструмент запроса координат",
        "currentLocation": "Текущее местоположение: Инструмент запроса > Запрос координат",
        "provinceHeader": "Провинции:",
        "cityHeader": "Города:",
        "areaHeader": "Районы:",
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
        "footerText": "Copyright © 2021-2024 Пауто Сеть. Все права защищены."
    },
    "fr": {
        "title": "Paotu Net - Outil de recherche de coordonnées, lever et coucher de soleil",
        "header": "Outil de recherche de coordonnées en ligne",
        "currentLocation": "Emplacement actuel : Outil de recherche > Recherche de coordonnées",
        "provinceHeader": "Provinces :",
        "cityHeader": "Villes :",
        "areaHeader": "Zones :",
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
        "footerText": "Copyright © 2021-2024 Paotu Net. Tous droits réservés."
    },
    "es": {
        "title": "Paotu Net - Herramienta de consulta de coordenadas, amanecer y atardecer",
        "header": "Herramienta de consulta de coordenadas en línea",
        "currentLocation": "Ubicación actual: Herramienta de consulta > Consulta de coordenadas",
        "provinceHeader": "Provincias:",
        "cityHeader": "Ciudades:",
        "areaHeader": "Áreas:",
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
        "footerText": "Copyright © 2021-2024 Paotu Net. Todos los derechos reservados."
    },
    # 可以添加其他语言的翻译内容...
}

# 默认语言
default_language = 'en'


# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'data.json')

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
    result = {'日期':date, '天亮': result['dawn'], '日出': result['sunrise'], '正午': result['noon'],'日落':  result['sunset'],'天黑':result['dusk']}
    json_data = json.dumps(result, ensure_ascii=False)
    return json_data

@app.route('/')
def index():
    # 从请求参数中获取语言，如果没有则从请求头中获取
    user_lang = request.args.get('lang')
    
    # 根据请求头判断用户的默认语言
    if not user_lang:
        user_lang = request.accept_languages.best_match(translations.keys(), default=default_language)

    # 检查语言是否在支持的语言中
    if user_lang not in translations:
        user_lang = default_language

    return render_template('index.html', translations=translations, language=user_lang, provinces=provinces)


#@app.route('/')
#def index():
#    return render_template('index.html', provinces=provinces)

@app.route('/location')
def location():
    province = request.args.get('province')
    city = request.args.get('city')
    area = request.args.get('area')

    if province and city and area:
        coordinates = [d for d in data if d['province'] == province and d['city'] == city and d['area'] == area]
        return jsonify(coordinates)
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

    result = calculate_sun_info(latitude, longitude, date_str, tz_name)
    return result,200,{"content-type":"application/json"}

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
