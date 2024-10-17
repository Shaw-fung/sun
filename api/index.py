# coding=utf-8

###  http://localhost:5000/sun?latitude=29.00319&longitude=109.87862&date=2024-10-17&timezone=Asia/Shanghai
###  curl -X POST -H "Content-Type: application/json" -d '{"latitude": 29.00319, "longitude": 109.87862, "date": "2024-10-17", "timezone": "Asia/Shanghai"}' http://localhost:5000/sun

from flask import Flask, request, jsonify
from datetime import datetime, timedelta, date
import pytz
import astral
import astral.sun
import json

app = Flask(__name__)

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

        result[event] = localized_time.strftime('%Y-%m-%d %H:%M:%S')
        
    result = {'天亮': result['dawn'], '日出': result['sunrise'], '中午': result['noon'],'日落':  result['sunset'],'天黑':result['dusk']}
    json_data = json.dumps(result, ensure_ascii=False)
    return json_data

@app.route('/')
def index():
    return("http://www.mydomain.com/sun?latitude=29.00319&longitude=109.87862&date=2024-10-17&timezone=Asia/Shanghai")

@app.route('/sun', methods=['POST', 'GET'])
def get_sun_info():
    if request.method == 'POST':
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']
        date_str = data['date']
        tz_name = data['timezone']
    elif request.method == 'GET':
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        date_str = request.args.get('date')
        tz_name = request.args.get('timezone')

    result = calculate_sun_info(latitude, longitude, date_str, tz_name)
    return result,200,{"content-type":"application/json"}

if __name__ == '__main__':
    app.run()
