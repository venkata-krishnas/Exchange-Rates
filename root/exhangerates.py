import requests
import sys
import ast
from flask import Flask, request, jsonify, render_template
import json
from datetime import date, timedelta
import requests
from flask_sqlalchemy import SQLAlchemy
from db import connecter as conn
app = Flask(__name__)


@app.route("/home", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/get_symbols",methods=["GET"])
def get_symbols():
    if request.method == "GET":
        response= requests.get("https://api.apilayer.com/exchangerates_data/symbols",headers={"apikey": "*******************"})
        data = json.loads(response.text)
        print(type(data))
        data = json.dumps(data)
        print(type(data))
        with open("sample.json", "w") as outfile:
          outfile.write(data)
    return(data)

@app.route("/store_data",methods=["POST"])
def store_data_symbols():
    if request.method == "POST":
        today = date.today()
        start = timedelta(days = 0)
        end = timedelta(days = 0)
        url = "https://api.apilayer.com/exchangerates_data/timeseries?start_date="+str(today - start)+"&end_date="+str(today - end)
        payload = {}
        headers= {"apikey": "*********************"}
        response = requests.get( url, headers=headers, data = payload)
        status_code = response.status_code
        result = response.text
        data = json.loads(response.text)
        data = (data["rates"])
        keys = list(data.keys())
        for key in keys:
            rates = data[key]
            rates = json.dumps((rates))
            print(rates)
            conn.insert(str(key), rates)
    return(data)

@app.route("/get_data_fromdate",methods=["GET","POST"])
def get_data():
    if request.method == "GET" or request.method == "POST":
       today = date.today()-timedelta(days = 4)
       rates = []
       for i in range(0,10):
           days = timedelta(days = i)
           d = conn.get(str(today - days))
           for r in d:
                r= str(r)
                rlen = len(r)-3
                r = r[2:rlen]
                r = json.loads(r)
                for key in r.keys():
                    r[key] = str(round(float(r[key]), 2))
                dateadd = {}
                dateadd["DATE"] = str(today - days)
                dateadd.update(r)
                rates.append(dateadd)
    # return rates
    return render_template("currency.html", r = rates)



@app.route("/update",methods=["POST"])
def update():
    if request.method == "POST":
        formitems = dict(request.form)
        day = str(formitems["DATE"])
        del formitems['DATE']
        formitems = json.dumps(formitems)
        print(formitems)
        conn.update(day, formitems)
        # print((formitems))
        # print(day)
    return ('', 204)

if __name__ == "__main__":
    app.debug =True
    app.run(host="127.0.0.1",port=9999)