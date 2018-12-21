# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
from urllib import parse

app = Flask(__name__)

slack_token = ""
slack_client_id = ""
slack_client_secret = ""
slack_verification = ""
sc = SlackClient(slack_token)

#http://welfoodstory.azurewebsites.net/?category=%EB%A9%94%EB%94%94%EC%8A%A8%ED%8C%90%EA%B5%90

# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    list_up_url="http://welfoodstory.azurewebsites.net/"
    list_up_soup= BeautifulSoup(urllib.request.urlopen(list_up_url).read(), "html.parser")

    el_suwon_list=[]
    el_kiheung_list=[]
    el_pyeongtaek_list=["전자평택"]
    el_onyang_list=[]
    el_seocho_list=["전자서초"]
    el_woomyeon_list=[]
    el_gumi_list=[]
    ds_ahsan_list=[]
    ds_cheonahn_list=[]
    sdi_cheonahn_list=[]
    sds_jamsil_list=["SDS잠실"]
    medison_list=["메디슨판교"]


    list_up_num=0

    for place in list_up_soup.find_all("li", class_="pushy-submenu"):
        for hall in place.find_all("li", class_="pushy-link"):
            
            
            if list_up_num==0:
                sp=hall.get_text().split()
                if len(sp) == 1:
                    hall_text=sp[0]
                else:
                    hall_text=sp[1]
                el_suwon_list.append(hall_text)
                
            elif list_up_num==1:
                sp=hall.get_text().split()
                if len(sp) == 1:
                    hall_text=sp[0]
                else:
                    hall_text=sp[1]
                el_kiheung_list.append(hall_text)
                

            elif list_up_num==2:
                sp=hall.get_text().split()
                if len(sp) == 1:
                    hall_text=sp[0]
                else:
                    hall_text=sp[1]
                el_onyang_list.append(hall_text)
                

            elif list_up_num==3:
                sp=hall.get_text().split()
                if len(sp) == 1:
                    hall_text=sp[0]
                else:
                    hall_text=sp[1]
                el_woomyeon_list.append(hall_text)
                
            elif list_up_num==4:
                sp=hall.get_text().split()
                if len(sp) == 1:
                    hall_text=sp[0]
                else:
                    hall_text=sp[1]
                el_gumi_list.append(hall_text)
                
            elif list_up_num==5:
                sp=hall.get_text().split()
                if len(sp) == 1:
                    hall_text=sp[0]
                else:
                    hall_text=sp[1]
                ds_ahsan_list.append(hall_text)
                
            elif list_up_num==6:
                sp=hall.get_text().split()
                if len(sp) == 1:
                    hall_text=sp[0]
                else:
                    hall_text=sp[1]
                ds_cheonahn_list.append(hall_text)
                
            elif list_up_num==7:
                sp=hall.get_text().split()
                if len(sp) == 1:
                    hall_text=sp[0]
                else:
                    hall_text=sp[1]
                sdi_cheonahn_list.append(hall_text)
                
            elif list_up_num==8:
                pass


            
        list_up_num+=1
    #계열사별 홀 정리완료

    print_list =[]

    search_ok=0
    

    all_list = el_suwon_list + el_kiheung_list + el_pyeongtaek_list + el_onyang_list + el_seocho_list + el_woomyeon_list + el_gumi_list + ds_ahsan_list + ds_cheonahn_list + sdi_cheonahn_list + sds_jamsil_list +medison_list

    for search in all_list: #홀이름이 명령어에 있을때와 없을때
        if search in text: #있을때 -> 메뉴 출력해주는 친절한 코드
            search_ok=1
            search_url=search
            print(search_url)

    
    if(search_ok==1):
        pass
    else:
        if "전자수원" in text:
            return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+el_suwon_list)
        elif "전자기흥화성" in text:
            return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+el_kiheung_list)
        #elif "전자평택" in text:
        #    return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+el_pyeongtaek_list)
        elif "전자온양" in text:
            return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+el_onyang_list)
        #elif "전자서초" in text:
        #    return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+el_seocho_list)
        elif "전자우면동" in text:
            return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+el_woomyeon_list)
        elif "전자구미" in text:
            return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+el_gumi_list)
        elif "디플아산" in text:
            return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+ds_ahsan_list)
        elif "디플천안" in text:
            return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+ds_cheonahn_list)
        elif "SDI천안" in text:
            return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+sdi_cheonahn_list)
        #elif "sds잠실" in text:
        #    return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+sds_jamsil_list)
        elif "삼성메디슨" in text:
            return u'\n'.join(["식당도 함께 입력해주세요☞\n"]+medison_list)       
        else:
            return u'\n'.join(["어느 장소를 원하시나요?☞\n\n전자수원\n전자기흥화성\n전자평택\n전자온양\n전자서초\n전자우면동\n전자구미\n디플아산\n디플천안\nSDI천안\nSDS잠실\n삼성메디슨\n"])
   
    url = "http://welfoodstory.azurewebsites.net/?category="+parse.quote(search_url)
    print(url)
    # URL 주소에 있는 HTML 코드를 soup에 저장합니다.
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    morning = []
    lunch = []
    dinner = []

    if "스마트홀" in text:
        morning_num=11
        lunch_num=10
        dinner_num=11
    elif "레인보우홀" in text:
        morning_num=13
        lunch_num=11
        dinner_num=12
    elif "밀키웨이홀" in text:
        morning_num=0
        lunch_num=10
        dinner_num=0
    elif "오아시스홀" in text:
        morning_num=0
        lunch_num=6
        dinner_num=0
    elif "패밀리홀" in text:
        morning_num=11
        lunch_num=10
        dinner_num=11
    elif "하우젠홀" in text:
        morning_num=0
        lunch_num=0
        dinner_num=0
    elif "폴라리스홀" in text:
        morning_num=10
        lunch_num=9
        dinner_num=10
    elif "모바일" in text:
        morning_num=0
        lunch_num=15
        dinner_num=14
    elif "하모니홀" in text:
        morning_num=12
        lunch_num=11
        dinner_num=13
    elif "투게더홀" in text:
        morning_num=11
        lunch_num=11
        dinner_num=11
    elif "소재연구단지" in text:
        morning_num=12
        lunch_num=19
        dinner_num=12
    elif "6라인" in text:
        morning_num=5
        lunch_num=6
        dinner_num=6
    elif "SR1" in text:
        morning_num=6
        lunch_num=8
        dinner_num=6
    elif "SR3" in text:
        morning_num=6
        lunch_num=10
        dinner_num=6
    elif "SR5" in text:
        morning_num=11
        lunch_num=10
        dinner_num=11
    elif "SR6" in text:
        morning_num=7
        lunch_num=8
        dinner_num=6
    elif "남자기숙사" in text:
        morning_num=4
        lunch_num=3
        dinner_num=6
    elif "여자기숙사" in text:
        morning_num=5
        lunch_num=5
        dinner_num=6
    elif "MR1" in text:
        morning_num=7
        lunch_num=12
        dinner_num=7
    elif "MR2" in text:
        morning_num=3
        lunch_num=4
        dinner_num=3
    elif "15라인" in text:
        morning_num=4
        lunch_num=5
        dinner_num=4
    elif "16라인" in text:
        morning_num=7
        lunch_num=8
        dinner_num=7
    elif "17라인" in text:
        morning_num=6
        lunch_num=10
        dinner_num=6
    elif "DSR" in text:
        morning_num=6
        lunch_num=15
        dinner_num=7
    elif "전자평택" in text :
        morning_num = 6
        lunch_num = 12
        dinner_num = 6
    elif "로즈홀" in text :
        morning_num = 8
        lunch_num = 8
        dinner_num = 6
    elif "챌린지홀" in text :
        morning_num = 8
        lunch_num = 8
        dinner_num = 6
    elif "전자서초" in text :
        morning_num = 0
        lunch_num = 0
        dinner_num = 0
    elif "1단지" in text :
        morning_num = 0
        lunch_num = 10
        dinner_num = 0
    elif "2단지" in text :
        morning_num = 11
        lunch_num = 12
        dinner_num = 7
    elif "1캠퍼스" in text :
        morning_num = 15
        lunch_num = 13
        dinner_num = 10
    elif "2캠퍼스-1" in text :
        morning_num = 16
        lunch_num = 15
        dinner_num = 11
    elif "2캠퍼스-2" in text :
        morning_num = 15
        lunch_num = 0
        dinner_num = 0
    elif "2캠퍼스-3" in text :
        morning_num = 14
        lunch_num = 12
        dinner_num = 11
    elif "비전홀" in text :
        morning_num = 9
        lunch_num = 9
        dinner_num = 8
    elif "조이홀" in text :
        morning_num = 7
        lunch_num = 6
        dinner_num = 4
    elif "블루그린홀" in text :
        morning_num = 9
        lunch_num = 13
        dinner_num = 8
    elif "올렉스홀" in text :
        morning_num = 9
        lunch_num = 11
        dinner_num = 8
    elif "크리스탈홀" in text :
        morning_num = 9
        lunch_num = 9
        dinner_num = 7
    elif "SDI천안" in text :
        morning_num = 12
        lunch_num = 10
        dinner_num = 7
    elif "SDI천안기숙사" in text :
        morning_num = 4
        lunch_num = 2
        dinner_num = 3
    elif "SDS잠실" in text :
        morning_num = 3
        lunch_num = 24
        dinner_num = 4
    elif "메디슨판교" in text :
        morning_num = 4
        lunch_num = 7
        dinner_num = 3

    i=0
    morning_cal_list=[]
    lunch_cal_list=[]
    dinner_cal_list=[]

    for menu in soup.find_all("div", class_="menu-item"): #페이지 내 모든 메뉴파트 찾기
        
        if i >=0 and i < morning_num: #아침
        
            for rest in menu.find_all("div", class_="menu-item-title"): #list[i] 0~
                morning.append(rest.get_text())
                
            for menulist in menu.find_all("div",class_="menu-item-contents"): #list[i+1]
                morning.append(menulist.get_text())
                #print (menulist.get_text())
                
            for cal in menu.find_all("div", class_="menu-item-kcal"): #list[i+2] 반복문은 3씩 더해서 돌려야
                morning.append(cal.get_text())
                print(morning)
                print(cal.get_text())
                print(cal.get_text().strip("kcal"))
                morning_cal_list.append(int(cal.get_text().strip("kcal")))
    
        elif i > morning_num and i < lunch_num+morning_num+1: #점심
            
            for rest in menu.find_all("div", class_="menu-item-title"):
                lunch.append(rest.get_text())
                
            for menulist in menu.find_all("div",class_="menu-item-contents"):
                lunch.append(menulist.get_text())
                #print (menulist.get_text())
                
            for cal in menu.find_all("div", class_="menu-item-kcal"):
                lunch.append(cal.get_text())
                print(cal.get_text())
                print(cal.get_text().strip("kcal"))
                lunch_cal_list.append(int(cal.get_text().strip("kcal")))
                
        elif i >= lunch_num+morning_num+1 and i < lunch_num+morning_num+dinner_num+1: #저녁
            
            for rest in menu.find_all("div", class_="menu-item-title"):
                dinner.append(rest.get_text())
                
            for menulist in menu.find_all("div",class_="menu-item-contents"):
                dinner.append(menulist.get_text())
                #print (menulist.get_text())
                
            for cal in menu.find_all("div", class_="menu-item-kcal"):
                dinner.append(cal.get_text())
                print(cal.get_text())
                print(cal.get_text().strip("kcal"))
                dinner_cal_list.append(int(cal.get_text().strip("kcal")))
                
     
        i += 1


    
    min_cal_menu=[]

    if "아침" in text and morning_num ==0:
        print_list.append("★☆오늘의 메뉴가 없습니다ㅠㅠ☆★\n")
    elif "점심" in text and lunch_num ==0:
        print_list.append("★☆오늘의 메뉴가 없습니다ㅠㅠ☆★\n")
    elif "저녁" in text and dinner_num == 0:
        print_list.append("★☆오늘의 메뉴가 없습니다ㅠㅠ☆★\n")
        
    else:
        print_list.append("★☆오늘의 메뉴☆★\n")
        
    if "아침" in text:
        if "최저칼로리" in text:
            min_cal=str(min(morning_cal_list)) # 최저 칼로리 계산
            for hey in morning:
                if min_cal in hey:
                    min_cal_menu.append("▼최저칼로리 메뉴입니다!▼\n")
                    min_cal_menu.append("<"+morning[morning.index(hey)] +">")
                    min_cal_menu.append("///"+morning[morning.index(hey)-2]+ "///")
                    min_cal_menu.append(morning[morning.index(hey)-1])
                    return u'\n'.join(min_cal_menu)
                    
        for j in range(0,len(morning)//3):
            print_list.append("///"+morning[j*3] + "///\n " + morning[j*3+1] + "\n<" + morning[j*3+2] + ">\n")

    elif "점심" in text:
        if "최저칼로리" in text:
            min_cal=str(min(lunch_cal_list)) # 최저 칼로리 계산
            for hey in lunch:
                if min_cal in hey:
                    min_cal_menu.append("▼최저칼로리 메뉴입니다!▼\n")
                    min_cal_menu.append("<"+lunch[lunch.index(hey)]+">")
                    min_cal_menu.append("///"+lunch[lunch.index(hey)-2]+ "///")
                    min_cal_menu.append(lunch[lunch.index(hey)-1])
                    return u'\n'.join(min_cal_menu)

        for j in range(0,len(lunch)//3):
            print_list.append("///"+lunch[j*3] + "///\n" + lunch[j*3+1] + "\n<" + lunch[j*3+2]+ ">\n")


    elif "저녁" in text:
        if "최저칼로리" in text:
            min_cal=str(min(dinner_cal_list)) # 최저 칼로리 계산
            for hey in dinner:
                if min_cal in hey:
                    min_cal_menu.append("▼최저칼로리 메뉴입니다!▼\n")
                    min_cal_menu.append("<"+dinner[dinner.index(hey)] +">")
                    min_cal_menu.append("///"+dinner[dinner.index(hey)-2]+ "///")
                    min_cal_menu.append(dinner[dinner.index(hey)-1])
                    return u'\n'.join(min_cal_menu)

        for j in range(0,len(dinner)//3):
            print_list.append("///"+dinner[j*3] + "///\n" + dinner[j*3+1] + "\n<" + dinner[j*3+2]+ ">\n")

    if "아침" in text and morning_num ==0:
        pass
    elif "점심" in text and lunch_num ==0:
        pass
    elif "저녁" in text and dinner_num == 0:
        pass
        
    else:
        print_list.append("★☆맛있는 식사 되세요!☆★\n")    

   

    return u'\n'.join(print_list)

# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200,)

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})

@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                            })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})
    
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
