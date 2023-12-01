# PYTHON
from flask import Flask, render_template, request, send_file
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import pandas as pd


def search_important_info(content): #중요한 정보 검색 함수 정의
    phone_matches = re.findall(r"\d{3}-\d{4}-\d{4}", content) #정규 표현식을 사용하여 전화번호 찾기
    email_matches = re.findall(r"[a-zA-Z0-9._+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,4}+", content) #정규 표현식을 사용하여 이메일 찾기
    penum_matches = re.findall(r"\d{6}-\d{7}+", content)#주민등록 번호 찾기
    
    return bool(phone_matches),bool(email_matches), bool(penum_matches) #3가지 중요한 정보 유형을 true or false로 반환함
#[\w\.-]+@[\w\.-]+
#\d{3}-\d{4}-\d{4}
def list_files(): #파일 검색 및 정보 수집 함수 정의
    upload_path = "uploads" #uploads 폴더로 경로 지정
    files_info = []

    for file in os.listdir(upload_path): #uploads 폴더 내 파일 목록 가져옴
        file_path = os.path.join(upload_path, file) #각 파일에 대한 반복문

        # 파일 내 중요한 정보 검색
        if file_path.endswith('.xlsx'):  # Check if the file is an Excel file
            df = pd.read_excel(file_path) #엑셀 파일 읽어옴
            content = df.to_string(index=False) 
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

        phone, email, penum = search_important_info(content)

        files_info.append({ 
            'file_name': file,
            'phone': phone,
            'email': email,
            'penum': penum
        })

    return files_info

def send_email(file_path):
    load_dotenv()
    SECRET_ID = os.getenv("SECRET_ID")
    SECRET_PASS = os.getenv("SECRET_PASS")

    smtp = smtplib.SMTP('smtp.naver.com', 587)
    smtp.ehlo()
    smtp.starttls()

    smtp.login(SECRET_ID, SECRET_PASS)

    myemail = 'boanproject1234@naver.com'
    youremail = 'pricep@naver.com'

    msg = MIMEMultipart()

    msg['Subject'] = "중요 내용 첨부돼있습니다."
    msg['From'] = myemail
    msg['To'] = youremail

    with open(file_path, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(file_path))

    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    msg.attach(part)

    smtp.sendmail(myemail, youremail, msg.as_string())
    smtp.quit()



if __name__ == '__main__':
    list_of_lists = [[item[key] for key in item] for item in list_files()] #2차원 리스트 생성
    #print(list_of_lists[1])
    idx = 0
    for res in list_of_lists: #이중 for 반복문을 통해 uploads 폴더 내에 있는 파일의 경로를 전달
        for result in res: 
            #print(result)
            if result == True:
                print(res)
                send_email(os.path.join('uploads', list_of_lists[idx][0]))
                break

        
