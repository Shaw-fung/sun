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

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="https://www.paoto.com/favicon.ico">
    <title>日出、日落查询使用说明</title>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: #fff;
            padding: 20px 0;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .container {
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }
        .content {
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            padding: 20px 0;
            background-color: #333;
            color: #fff;
        }
        pre {
            background-color: #272822;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        code {
            font-family: 'Source Code Pro', monospace;
        }
        a {
            font-weight: bold;
            color: #ffffff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        @media (max-width: 600px) {
            .container {
                margin: 20px;
                padding: 15px;
            }
            .header {
                padding: 15px 0;
            }
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Source+Code+Pro:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="header">
        <h1>日出、日落查询使用说明</h1>
    </div>
    <div class="container">
        <div class="content">
          <h3>基础说明</h3>
          <p>1.参数说明</p>
          <pre><code>1)纬度 latitude=29.00319
          
2)经度 longitude=109.87862
                     
3)需要查询的日期 date=2024-10-17
                     
4)时区 timezone=Asia/Shanghai
</code></pre><p>2.GET使用方法</p>
          <pre><code>https://sun.paoto.com/sun?latitude=29.00319&longitude=109.87862&date=2024-10-17&timezone=Asia/Shanghai
          </code></pre>
          <p>3.Post使用方法</p>
          <pre><code>curl -X POST -H "Content-Type: application/json" -d '{"latitude": 29.00319, "longitude": 109.87862, "date": "2024-10-17", "timezone": "Asia/Shanghai"}' https://sun.paoto.com/sun
          </code></pre>当地经纬度获取网址，<a href="http://www.maps4gis.com/xiangzhen/jingweidu/index.html">点这里</a>👈🏻。
        </div>
    </div>
    <div class="footer">
        <p>©2024 <a href="https://paoto.com">paoto.com</a>. All rights reserved. Powered by <a href="https://vercel.com/">Vercel</a>.</p>
    </div>
</body>
</html>
'''

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
    return html

@app.route('/sun', methods=['POST', 'GET'])
def get_sun_info():
    if request.method == 'POST':
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']
        if data['date'] == 'today':
            today = datetime.today()
            date_str = today.strftime("%Y-%m-%d")
        else:
            date_str = data['date']
        tz_name = data['timezone']
    elif request.method == 'GET':
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        if request.args.get('date') == 'today':
            today = datetime.today()
            date_str = today.strftime("%Y-%m-%d")
        else:
            date_str = request.args.get('date')
        tz_name = request.args.get('timezone')

    result = calculate_sun_info(latitude, longitude, date_str, tz_name)
    return result,200,{"content-type":"application/json"}

if __name__ == '__main__':
    app.run()
