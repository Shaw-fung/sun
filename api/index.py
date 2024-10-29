from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, date
import pytz
import astral
import astral.sun
import json

app = Flask(__name__)

# 读取json数据
with open('data.json', 'r', encoding='utf-8') as f:
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
    return render_template('index.html', provinces=provinces)

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
