from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/order', methods=['POST'])
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    name = request.form['name_give']
    count = request.form['count_give']
    address = request.form['address_give']
    phone = request.form['phone_give']
    print (name,count,address,phone)


    # 2. mongoDB에 데이터 넣기
    order = {
            'name': name,
            'count' : count,
            'address' : address,
            'phone': phone
        }
    db.orders.insert_one(order)

    return jsonify({'result': 'success', 'msg': '주문이 등록되었습니다!'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    result = list( db.orders.find({},{'_id' : False}) )

    # 2. orders라는 키 값으로 customer 정보 보내주기
    return jsonify({'result': 'success', 'orders' : result})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
