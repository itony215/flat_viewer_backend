from flask import Flask, render_template
import requests
import json
from flask_cors import CORS
from datetime import datetime
# import os

app = Flask(__name__)
CORS(app)
@app.route("/")
def hello():
    return "Tony Stock"

@app.route('/api/info/<stock_id>')
def home_page(stock_id):
    r = requests.get('https://tw.stock.yahoo.com/_td-stock/api/resource/StockServices.stockList;fields=avgPrice%2Corderbook;symbols='+stock_id)
    data = json.loads(r.text)
    return render_template('test88.html', data=data)

@app.errorhandler(500)
def pageNotFound(error):
    return "stock id not found"

# @app.route('/api/draw/<stock_id>')
# def draw(stock_id):
#     SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
#     filename = "data_"+stock_id+".json"
#     json_url = os.path.join(SITE_ROOT, "static/json", filename)
#     data = json.load(open(json_url))
#     print(data['stock_data'])
#     return str(data['stock_data'])

@app.route('/api/draw2/<stock_id>')
def draw2(stock_id):
    r = requests.get('https://tw.stock.yahoo.com/_td-stock/api/resource/FinanceChartService.ApacLibraCharts;symbols=%5B%22'+stock_id+'.TW%22%5D;')
    data = json.loads(r.text)
    
    previousClose = data[0]['chart']['meta']['previousClose']
    #print(previousClose)
    limitUpPrice = data[0]['chart']['meta']['limitUpPrice']
    #print(limitUpPrice)
    limitDownPrice = data[0]['chart']['meta']['limitDownPrice']
    #print(limitDownPrice)
    timestamp = data[0]['chart']['timestamp']
    time_str = timestamp[0]
    date_time = datetime.fromtimestamp(time_str)
    Y = date_time.strftime("%Y")
    m = date_time.strftime("%m")
    d = date_time.strftime("%d")
    #print("Output 2:", Y,m,d)
    open_price=	data[0]['chart']['indicators']['quote'][0]['open']
    volume=	data[0]['chart']['indicators']['quote'][0]['volume']
    
    # print(timestamp)
    # print(open_price)
    # print(volume)
    result =[]
    for idx, time  in enumerate(timestamp):
        result.append([float(time)*1000,float(open_price[idx]),float(volume[idx])])
    # open_price = data[0]['chart']['timestamp']
    result.append([previousClose,limitUpPrice,limitDownPrice,Y,m,d])
    json_data = json.dumps(result)
    return json_data


app.run()