from sched import scheduler
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
import pymysql
import random
import threading
import time
from datetime import datetime
import smtplib
from email.message import EmailMessage

count = 0
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='coffee',
    charset='utf8mb4'
    )

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['TEMPLATES_AUTO_RELOAD'] = True # hot-reloading 기능
socketio = SocketIO(app)

d_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('weight_data')
def handle_weight_data(json):
    global count
    global d_time
    box = 0
    print('Received data : ' + str(json))
    weight = json['weight']


    if weight > 60 :
        box = weight / 60
        box = int(box)
    else:
        box = 0
    
    lungo = box
    americano = 4
    espresso = 2
    
    
    # 클라이언트로 데이터 전송
    socketio.emit('update_progress_lungo', {'weight_lungo': lungo})
    socketio.emit('update_progress_americano', {'weight_americano': americano})
    socketio.emit('update_progress_espresso', {'weight_espresso': espresso})
    print("box :{}".format(box))
    
    if (lungo <= 1) :
        count += 1
        print("count :", count)
    else :
        count = 0
    
    if (count % 100 == 9) :
        message = "LUNGO Box 재고 부족"
        email(message)


    with conn.cursor() as cursor:
        # SQL 쿼리 작성
        sql = "INSERT INTO box (LUNGO, AMERICANO, ESPRESSO, DATE) VALUES (%s, %s, %s, %s)"
        # 쿼리 실행
        values = (lungo, americano, espresso, d_time)
        cursor.execute(sql, values)
        # cursor.execute(d_time, val)
    # 실행한 쿼리를 데이터베이스에 반영
    conn.commit()
    


def email(alarm):
    # STMP 서버의 url과 port 번호
    # SMTP(Simple Mail Transfer Protocol)는 이메일을 전송에 사용되는 프로토콜
    SMTP_SERVER = '108.177.97.109'
    SMTP_PORT = 587
    
    # 1. SMTP 서버 연결
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    EMAIL_ADDR = 'rkdaudgus2650@gmail.com'
    EMAIL_PASSWORD = 'zptc loay lqib atkh'
    
    # 2. SMTP 서버에 로그인
    smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)
    
    # 3. MIME 형태의 이메일 메세지 작성
    message = EmailMessage()
    message.set_content(alarm)
    message["Subject"] = "재고부족알림"
    message["From"] = EMAIL_ADDR  #보내는 사람의 이메일 계정
    message["To"] = 'rkdaudgus2650@mobile.re.kr'
    
    # 4. 서버로 메일 보내기
    smtp.send_message(message)
    print("complete send email : {}".format(d_time))
    # 5. 메일을 보내면 서버와의 연결 끊기
    smtp.quit()



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=12345, debug=True)