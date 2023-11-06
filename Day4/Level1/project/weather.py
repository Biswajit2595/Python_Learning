
import json
from flask import Flask,request,jsonify

app=Flask(__name__)

weather_data = {
    'San Francisco': {'temperature': 14, 'weather': 'Cloudy'},
    'New York': {'temperature': 20, 'weather': 'Sunny'},
    'Los Angeles': {'temperature': 24, 'weather': 'Sunny'},
    'Seattle': {'temperature': 10, 'weather': 'Rainy'},
    'Austin': {'temperature': 32, 'weather': 'Hot'},
}


@app.route("/")
def home():
    return "Weather app"

@app.route("/get")
def get_all():
    return jsonify(weather_data)


@app.route("/weather/<string:city>",methods=["GET","PUT","DELETE"])
def get_weather(city):
    if request.method=="GET":
        if city in weather_data:
            return jsonify({city:weather_data[city]}),200
        else:
            return jsonify({'error': 'City not found'}), 404
    
    elif request.method=="PUT":
        data=request.get_json()
        if city in weather_data:
            weather_data[city]["temperature"]=data.get("temperature",weather_data[city]["temperature"])
            weather_data[city]["weather"]=data.get("weather",weather_data[city]["weather"])
            return jsonify({"city":city,"data":weather_data[city]}),201
        else:
            return jsonify({'error': 'City not found'}), 404
        
    elif request.method=="DELETE":
        if city in weather_data:
            del weather_data[city]
            return jsonify({"data":"City has been deleted"}),200
        else:
            return jsonify({'error': 'City not found'}), 404



@app.route("/weather/",methods=["POST"])
def post_weather():
    data=request.get_json()
    city=data["city"]
    new_city={
        "temperature":data["temperature"],
        "weather":data["weather"],
    }
    weather_data[city]=new_city
    return jsonify({"city":city,"data":new_city}),201


if __name__=='__main__':
    app.run(debug=True)