import tkinter
from tkinter import *
from tkinter import messagebox
import random

window=tkinter.Tk()
####
lbl = Label(window, text="이름") 
lbl.pack()
userName =''

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
    txt.delete("1.0",END) # 텍스트 상자에 있던 내용 삭제.
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
                
#    print("%d스트라이크" % strike_count)
#    print("%d볼" % bol_count)
    if(com==user):
        messagebox.showinfo("yes", "%d 번만에 정답!!" % cnt)
        window.quit()
        window.destroy()
#        print("%d 번만에 정답!!" % cnt)
#        break
#        
        
def close():
    window.quit()
    window.destroy()        
#menu = Menu(window)
#
#menu_file = Menu(menu,tearoff=0)
#menu_file.add_command(label="run",command =RunStrike )##usernum과 computer를 비교하여 출력해주는 커맨드를 만들어서 넣을 예정
#menu_file.add_cascade(label="File",menu=menu_file)
#window.config(menu=menu)##윈도우 메뉴창에 메뉴 생성.
#        
def Init():
    user.clear()
    
menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="실행",command=RunStrike)
menu1.add_separator()
menu1.add_command(label="Exit", command=close)
menubar.add_cascade(label="File", menu=menu1)

menu2 = Menu(menubar, tearoff=0, selectcolor="red")
menu2.add_command(label="초기화", command =Init)
menubar.add_cascade(label="Edit", menu=menu2)
window.config(menu=menubar)
##################################33

#strike_count = 0 ## 스트라이크 카운트
#bol_count = 0 ## 볼 카운
user=[] ## 사용자 숫자 정보를 넣기위한 리스트
photoArr=[["1.gif", "2.gif", "3.gif", "4.gif", "5.gif",
         "6.gif", "7.gif", "8.gif", "9.gif"]]## 포문을 이용해서 이미지를 넣을 예정
## 컴퓨터 숫자 3개 입력.
com=[] 
while True: 
    rd = random.randint(1, 9)
    if(not rd in com):
        com.append(rd)
        if len(com) == 3:
            break 
print(len(com))
print(com)
cnt=0 ##게임 횟수 저장변수
#######타이틀 작성 
window.title("test")
window.geometry("640x400+100+100")
window.resizable(False, False)
########## 공지사항 출력. 
label=tkinter.Label(window, text="이름을 입력 후 save\n규칙 1에서 9사이에 겹치치 않는 숫자 3개 클릭 후 첫번째 메뉴에서 실행버튼클릭\n 실행버튼 이후 계속 도전을 하기위해 두번째 메뉴에서 초기화 버튼을 클릭 후 진행")
label.pack()

#btn = Button(window, text='종료', command=quit)    # quit는 프로그램을 종료시킨다
#btn.pack()

#### 이미지 버튼 함수.
def ClickNum1():
     if len(user)<3:
        user.append(int(1))
        messagebox.showinfo("yes", "숫자1이 입력됩니다")
   
        
def ClickNum2():
    if len(user)<3:
        user.append(int(2))
        messagebox.showinfo("yes", "숫자2가 입력됩니다")
def ClickNum3():
    if len(user)<3:
        user.append(int(3))
        messagebox.showinfo("yes", "숫자3이 입력됩니다")
def ClickNum4():
    if len(user)<3:
        user.append(int(4))
        messagebox.showinfo("yes", "숫자4가 입력됩니다")
def ClickNum5():
    if len(user)<3:
        user.append(int(5))
        messagebox.showinfo("yes", "숫자5가 입력됩니다")
def ClickNum6():
    if len(user)<3:
        user.append(int(6))
        messagebox.showinfo("yes", "숫자6이 입력됩니다")
def ClickNum7():
    if len(user)<3:
        user.append(int(7))
        messagebox.showinfo("yes", "숫자7이 입력됩니다")
def ClickNum8():
    if len(user)<3:
        user.append(int(8))
        messagebox.showinfo("yes", "숫자8이 입력됩니다")
def ClickNum9():
    if len(user)<3:
        user.append(int(9))  
        messagebox.showinfo("yes", "숫자9가 입력됩니다")
####
    
##########################이미지 버튼식으로 넣어 클릭 시 데이터 저장. ######
photo = PhotoImage(file="./1.gif",master=window)
lbl = Button(window, image=photo,command = ClickNum1)
lbl.pack(side=LEFT)

photo2 = PhotoImage(file="./2.gif",master=window)
lbl2 = Button(window, image=photo2,command = ClickNum2)
lbl2.pack(side=LEFT)


photo3 = PhotoImage(file="./3.gif",master=window)
lbl3 = Button(window, image=photo3,command = ClickNum3)
lbl3.pack(side=LEFT)


photo4 = PhotoImage(file="./4.gif",master=window)
lbl4 = Button(window, image=photo4,command = ClickNum4)
lbl4.pack(side=LEFT)


photo5 = PhotoImage(file="./5.gif",master=window)
lbl5 = Button(window, image=photo5,command = ClickNum5)
lbl5.pack(side=LEFT)


photo6 = PhotoImage(file="./6.gif",master=window)
lbl6 = Button(window, image=photo6,command = ClickNum6)
lbl6.pack(side=LEFT)


photo7 = PhotoImage(file="./7.gif",master=window)
lbl7 = Button(window, image=photo7,command = ClickNum7)
lbl7.pack(side=LEFT)


photo8 = PhotoImage(file="./8.gif",master=window)
lbl8 = Button(window, image=photo8,command = ClickNum8)
lbl8.pack(side=LEFT)


photo9 = PhotoImage(file="./9.gif",master=window)
lbl9 = Button(window, image=photo9,command = ClickNum9)
lbl9.pack(side=LEFT)
####################################




window.mainloop()

#clear
