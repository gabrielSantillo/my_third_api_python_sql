from flask import Flask, request, make_response
from dbhelpers import run_statement
from apihelpers import check_endpoint_info
import json

app = Flask(__name__)

@app.get('/api/philosopher')
def get_all_philosophers():
    results = run_statement('CALL get_all_philosophers()')

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 400)

@app.post('/api/philosopher')
def add_philosopher():
    invalid = check_endpoint_info(request.json, ['name', 'bio', 'date_of_birth', 'date_of_death', 'image_url'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400) 

    results = run_statement('CALL insert_philosopher(?,?,?,?,?)',
    [request.json.get('name'), request.json.get('bio'), request.json.get('date_of_birth'), request.json.get('date_of_death'), request.json.get('image_url')])

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    elif(results.startswith('Duplicate entry')):
        return "This username already exists. Please, pick other."
    else:
        return make_response(json.dumps(results, default=str), 400)

@app.get('/api/quote')
def get_quotes_by_philosopher_id():
    invalid = check_endpoint_info(request.json, ['philosopher_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400) 

    results = run_statement('CALL get_quotes_by_phylosopher_id(?)', [request.json.get('philosopher_id')])

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    elif(results.startswith('Duplicate entry')):
        return "This username already exists. Please, pick other."
    else:
        return make_response(json.dumps(results, default=str), 400)

@app.post('/api/quote')
def add_quote():
    invalid = check_endpoint_info(request.json, ['philosopher_id', 'content'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400) 

    results = run_statement('CALL insert_quote(?,?)', [request.json.get('philosopher_id'), request.json.get('content')])

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    elif(results.startswith('Duplicate entry')):
        return "This username already exists. Please, pick other."
    else:
        return make_response(json.dumps(results, default=str), 400)

app.run(debug=True)