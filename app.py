# importing librearies to use when making the db connection and building the API
from flask import Flask, request, make_response
from dbhelpers import run_statement
from apihelpers import check_endpoint_info
import json

# calling the Flask function which will return a value that I will be used for my API
app = Flask(__name__)

# making a get request with the /api/philosopher endpoint
@app.get('/api/philosopher')
# function that will call the procedure responsible to send back all philosophers
def get_all_philosophers():
    # calling the procedure
    results = run_statement('CALL get_all_philosophers()')

    # checking to see if the response is a list and if yes, turn this response into a JSON and the status code response, if not, sent back a message with the status code response
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 400)

# making a post request with the /api/philosopher endpoint
@app.post('/api/philosopher')
# function that will call the procedure responsible to add a new philosopher to the db
def add_philosopher():
    # calling the function that will verify the return value
    invalid = check_endpoint_info(request.json, ['name', 'bio', 'date_of_birth', 'date_of_death', 'image_url'])
    # if the invalid value is anything but None return with the make_response showing what was the error
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400) 

    # calling the procedure
    results = run_statement('CALL insert_philosopher(?,?,?,?,?)',
    [request.json.get('name'), request.json.get('bio'), request.json.get('date_of_birth'), request.json.get('date_of_death'), request.json.get('image_url')])

    # checking to see if the response is a list and if yes, turn this response into a JSON and the status code response, if not, sent back a message with the status code response
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    elif(results.startswith('Duplicate entry')):
        return "This username already exists. Please, pick other."
    else:
        return make_response(json.dumps(results, default=str), 400)

# making a get request with the /api/quote endpoint
@app.get('/api/quote')
# function that will call the procedure responsible to get the philosopher based on its id
def get_quotes_by_philosopher_id():
    # calling the function that will verify the return value
    invalid = check_endpoint_info(request.json, ['philosopher_id'])
    # if the invalid value is anything but None return with the make_response showing what was the error
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400) 
    # calling the procedure
    results = run_statement('CALL get_quotes_by_phylosopher_id(?)', [request.json.get('philosopher_id')])

    # checking to see if the response is a list and if yes, turn this response into a JSON and the status code response, if not, sent back a message with the status code response
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    elif(results.startswith('Duplicate entry')):
        return "This username already exists. Please, pick other."
    else:
        return make_response(json.dumps(results, default=str), 400)

# making a post request with the /api/quote endpoint
@app.post('/api/quote')
# function that will call the procedure responsible to add the quote content based on the philosopher id
def add_quote():
    # calling the function that will verify the return value
    invalid = check_endpoint_info(request.json, ['philosopher_id', 'content'])
    # if the invalid value is anything but None return with the make_response showing what was the error
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400) 

    # calling the procedure
    results = run_statement('CALL insert_quote(?,?)', [request.json.get('philosopher_id'), request.json.get('content')])

    # checking to see if the response is a list and if yes, turn this response into a JSON and the status code response, if not, sent back a message with the status code response
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    elif(results.startswith('Cannot add or update a child row')):
        return "This philosopher id doesn't exists. Please, insert an existing one."
    elif(results.startswith('Incorrect integer value')):
        return "Please, choose a valid philosopher id."
    else:
        return make_response(json.dumps(results, default=str), 400)

# making a delete request with the /api/delete endpoint
@app.delete('/api/delete')
# function that will call the procedure responsible to delete all quotes related to a philosoper and will delete the philosopher too
def delete_quote_and_philosopher():
    # calling the function that will verify the return value
    invalid = check_endpoint_info(request.json, ['philosopher_id'])
    # if the invalid value is anything but None return with the make_response showing what was the error
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400) 

    # calling the procedure
    results = run_statement('CALL delete_quote_and_philosopher(?)',
    [request.json.get('philosopher_id')])

    # checking to see if the response is a list and if yes, turn this response into a JSON and the status code response, if not, sent back a message with the status code response
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    elif(results.startswith('Duplicate entry')):
        return "This username already exists. Please, pick other."
    else:
        return make_response(json.dumps(results, default=str), 400)

# starting our application flask server with debug mode turned on
app.run(debug=True)