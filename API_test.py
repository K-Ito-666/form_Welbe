import pickle
import sys
sys.path.append('../')
import os
#print(os.getcwd())
from flask import Flask, request
import hashlib
import json
import string
import datetime
#from diary_update import update_file

app = Flask(__name__, template_folder='')
path = os.getcwd()

#@app.route('/login', method=[''])

#日付ごとをkeysにした辞書にする

@app.route('/post', methods=['POST'])
def html():
    data = request.json
    day=data['contents']['day']
    filename = str(day) + '.json'
    
    if os.path.exists(filename) == True:
        with open(filename,'r') as f:
            json_r = json.load(f)
            json_r[data['user']]=data['contents']
        with open(day + '.json','w') as f:
            json.dump(json_r,f)
    else:
        data_dic = {data['user']:data['contents']}
        with open(day + '.json','a') as f:
            json.dump(data_dic,f)

    return {'response': "sucess"}


@app.route('/get_diary', methods=['GET'])
def get_diary():
    user = request.args.get('user')
    today = datetime.date.today()
    diary_dic={}
    for i in range(7):
        day = today - datetime.timedelta(days=i)
        filename = str(day) + '.json'
        if os.path.exists(filename) == True:
            with open(filename,'r',encoding='cp932') as f:
                j_r = json.load(f)
                if user in j_r.keys():
                    diary_dic[str(day)]=j_r[user]['diary']

    return(diary_dic)


@app.route('/get_fb', methods=['GET'])
def get_fb():
    user = request.args.get('user')
    today = datetime.date.today()
    diary_dic={}
    diary_dic['date']=[]
    diary_dic['my_happy']=[]
    diary_dic['user']=[]
    for i in range(7):
        day = today - datetime.timedelta(days=i)
        filename = str(day) + '.json'
        if os.path.exists(filename) == True:
            with open(filename,'r',encoding='cp932') as f:
                j_r = json.load(f)
                for users in j_r.keys():
                    diary_dic['date'].append(j_r[users]['day'])
                    diary_dic['my_happy'].append(j_r[users]['my_happy'])
                    diary_dic['user'].append(users)

    return(diary_dic)



if __name__ == "__main__":
    app.run(debug=True)
