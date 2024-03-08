from email.message import EmailMessage
import smtplib
import datetime

def email(alarm):
    # SMTP 서버의 IP 주소와 SSL 포트 번호
    SMTP_SERVER = '108.177.97.109' # 이 IP 주소는 예시일 뿐, 실제 사용 시 smtp.gmail.com을 사용해야 함
    SMTP_PORT = 465
    
    # 1. SMTP 서버에 SSL로 연결
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    EMAIL_ADDR = 'rkdaudgus2650@gmail.com'
    EMAIL_PASSWORD = 'zptc loay lqib atkh' # 구글 앱 비밀번호를 사용해야 함
    
    # 2. SMTP 서버에 로그인
    smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)
    
    # 3. MIME 형태의 이메일 메세지 작성
    message = EmailMessage()
    message.set_content(alarm)
    message["Subject"] = "재고부족알림"
    message["From"] = EMAIL_ADDR
    message["To"] = 'rkdaudgus2650@mobile.re.kr'
    
    # 4. 서버로 메일 보내기
    smtp.send_message(message)
    print("complete send email : {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    # 5. 서버와의 연결 끊기
    smtp.quit()

email("hi")