import requests
from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():
    return render_template(f'index.html')

@app.route("/calculation", methods = ['POST', 'GET'])
def calculation():
    form_values = request.form
    number_one = form_values['number_one'] 
    number_two = form_values['number_two'] 
    
    add_response = requests.get(
        f'http://add-app/?number_one={number_one}&number_two={number_two}'
    )
    add_response = json.loads(add_response.content)

    multi_response = requests.get(
        f'http://multi-app/?number_one={number_one}&number_two={number_two}'
    )
    multi_response = json.loads(multi_response.content)

    context = {
        'number_one': number_one,
        'number_two': number_two,
        'add_hostname': add_response['hostname'],
        'add_result': add_response['result'],
        'multi_hostname': multi_response['hostname'],
        'multi_result' : multi_response['result']
    }
    return render_template(f'result.html', **context)

@app.route("/metrics", methods= ['GET'])
def status():
    status = requests.get('http://127.0.0.1/server-status?auto')
    status_split = status.text.split()
    for i, _ in enumerate(status_split):
        if _ == 'ConnsTotal:':
            conn_total = status_split[i + 1]
            break
    try:    
        return f'http_requests_total {conn_total}'
    except:
        return status.text

@app.route("/load", methods= ['GET'])
def load():
    try:
        requests.get("http://add-app/load",timeout=0.0000000001)
    except: 
        pass
    try:
        requests.get("http://multi-app/load",timeout=0.0000000001)
    except: 
        pass
    return "Load enabled"


if __name__ == '__main__':
   app.run(port=8080)
