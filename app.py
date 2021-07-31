#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify, request
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

import flask
app = Flask(__name__)

def fuel_type(x):
    if x=='Diesel':
        op=[1,0]
    if x=='Petrol':
        op=[0,1]
    else:
        op=[0,0]
    return op

def Seller_type(x):
    if x=='Individual':
        op=1
    else:
        op=0
    return op

def Transmission(x):
    if x=='Manual':
        op=1
    else:
        op=0
    return op

def years_used(x):
    op = 2020-x
    return op

def veh_type(x):
    if x=="4wheeler":
        op=1
    else:
        op=0
    return op

@app.route('/')
def hello_world():
    return "Hello Buddy"

@app.route('/web')
def index():
    return flask.render_template('web.html')


@app.route('/predict', methods=['POST'])
def predict():
    to_predict_list = request.form.to_dict()
    year=int(to_predict_list['year'])
    pp=float(to_predict_list['pp'])
    km=int(to_predict_list['km'])
    owner=int(to_predict_list['owner'])
    fuel=to_predict_list['fuel']
    st=to_predict_list['st']
    trnsmn=to_predict_list['trnsmn']
    vt=to_predict_list['vt']
    x=[]
    x.extend([years_used(year),pp,km,owner])
    x.extend(fuel_type(fuel))
    x.extend([Seller_type(st),Transmission(trnsmn),veh_type(vt)])
    clf = joblib.load('model.pkl')
    prediction='Rs '+str(int((clf.predict([x])[0])*100000))
    return jsonify({'The Selling Price of your Vehicle must be approximately': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

