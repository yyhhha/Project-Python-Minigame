import tkinter
from tkinter import *
from tkinter import messagebox
import random
import pygame
from pygame import mixer
###GUI tkinter사용 bgm pygame.mixer사용
window=tkinter.Tk()##tkinter객체 생성
lbl = Label(window, text="이름") 
lbl.pack()
userName =''

##### 배경음악
mixer.init()##mixer초기화
mixer.music.load("Itro.mp3")#음악 파일 로드
mixer.music.play(-1)# 음악 재생 -1을 넣어주면 무한반복

base = PhotoImage(file = "base2.gif")#배경화면 이미지 지정
base_label = Label(image = base)#
base_label.place(x = 0, y = 0)#사진의 위치 지정
##글자를 입력받을 텍스트위젯
## 이름을 입력받게 하여 게임이 끝난 후 이름과 
## 횟수등을 저장할 예정
txt = Text(window,width=20,height=2 )
txt.pack()
txt.insert(END,"이름을 입력하세요")
## 세이브 버튼 
def btnsave():
    print(txt.get("1.0",END))##1:첫번째 라인 , 0 : 0번째 colum 위치 END는 끝까지
    global userName ## scope가 달라 global로 지정해주지 않으면 전역 변수가 아닌 
    #지역변수를 사용하려 하여 에러가 난다. 
    userName+=txt.get("1.0",END)
#    txt.delete("1.0",END) # 텍스트 상자에 있던 내용 삭제.
btn = Button(window,text="save",command=btnsave) 
btn.pack()  
############################
##menu탭에 실행하기 추가!!!
def RunStrike():
    global cnt
    strike_count =0
    bol_count =0
    cnt +=1
    for i in range(0,3):
        if (com[i] == user[i]): ## 같은 자리 같은 숫자면 스트라이크 증가
            strike_count=strike_count+1
        else:
            j=0
            for j in range(0,3):
                if (com[i] == user[j]):
                    bol_count = bol_count + 1
    messagebox.showinfo("yes", "%d스트라이크" % strike_count)
    messagebox.showinfo("yes", "%d볼" % bol_count) 
                
    if(com==user):
        messagebox.showinfo("yes", "%d 번만에 정답!!" % cnt)
        #정답이면 tkinter객체
        SaveScore()
        mixer.quit() 
        window.quit()
        window.destroy()
        pygame.quit()
        sys.exit()
        
#음악 종료와 tkinter,pygame,mixer
def close():
    SaveScore()
    mixer.quit() 
    window.quit()
    window.destroy()
    pygame.quit()
    sys.exit()        

#유저 넘버들을 초기화 
def Init():
    user.clear()

##메뉴바   
menubar = Menu(window)
#첫번째 메뉴들 정의
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="실행",command=RunStrike)
menu1.add_separator()
menu1.add_command(label="Exit", command=close)
menubar.add_cascade(label="File", menu=menu1)
#두번째 메뉴들 정의
menu2 = Menu(menubar, tearoff=0, selectcolor="red")
menu2.add_command(label="초기화", command =Init)
menubar.add_cascade(label="Edit", menu=menu2)
window.config(menu=menubar)
##################################33

user=[] ## 사용자 숫자 정보를 넣기위한 리스트
## 컴퓨터 숫자 3개 입력.
com=[] 
while True: 
    rd = random.randint(1, 9)
    if(not rd in com):
        com.append(rd)
        if len(com) == 3:
            break 
#print(com)
cnt=0 ##게임 횟수 저장변수
#######타이틀 작성 
window.title("Strike")
window.geometry("600x600")
window.resizable(False, False)
########## 공지사항 출력. 
label=tkinter.Label(window, text="1) 이름을 입력 후 'save'를 클릭하세요!\n2) 겹치지 않는 숫자 3개 선택 후 'File -> 실행'\n3) 계속 도전하려면 'Edit -> 초기화'")
label.pack()
def SaveScore():
    f = open('./test.txt','w',encoding='utf-8')
    data = [userName,str(cnt)]
    print(data)
    f.writelines(data)
    f.close()

#### 이미지 버튼 함수.
def ClickNum(n):
    if len(user)<3:
        user.append(int(n))
        messagebox.showinfo("yes", "숫자{}이 입력됩니다".format(n))

####################################
        #반복문을 돌면서 이미지를  매핑
for i in range(1,10):
    globals()['photo{}'.format(i)] = PhotoImage(file="./"+str(i)+".gif",master=window)
## 버튼에 이미지를 매핑과 커맨드를 매핑
lbl1 = Button(window, image=photo1,command = lambda: ClickNum(1))
lbl2 = Button(window, image=photo2,command = lambda: ClickNum(2))
lbl3 = Button(window, image=photo3,command = lambda: ClickNum(3))
lbl4 = Button(window, image=photo4,command = lambda: ClickNum(4))
lbl5 = Button(window, image=photo5,command = lambda: ClickNum(5))
lbl6 = Button(window, image=photo6,command = lambda: ClickNum(6))
lbl7 = Button(window, image=photo7,command = lambda: ClickNum(7))
lbl8 = Button(window, image=photo8,command = lambda: ClickNum(8))
lbl9 = Button(window, image=photo9,command = lambda: ClickNum(9))
## 버튼 이미지들의 위치정보를 설정한다. 
for i in range(1,10):
    globals()['lbl{}'.format(i)].pack(side=LEFT)
window.protocol('WM_DELETE_WINDOW',close)
window.mainloop()

