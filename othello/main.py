from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk

import vsAI
import vsHuman
import vs66AI
import vs66Human

class select(ttk.Frame):    #メインウィンドウ表示
    def __init__(self, master):
        super().__init__(master, width=600, height=600 ,style='TFrame')
        self.mode=StringVar()
        self.power = StringVar()
        self.firstColor = StringVar()
        self.secondColor = StringVar()
        self.largeGrid = StringVar()
        self.create_widgets()
        self.pack()

    def create_widgets(self): #メインウィンドウの装飾部分

        #モード選択
        Static1 = ttk.Label(text=u"相手:",font=("MSゴシック","12", "bold"),background="#FFD285")
        Static1.place(x=35, y=30)

        valuelist=["人間","AI"]
        self.comboMode = ttk.Combobox(self,values=valuelist,textvariable=self.mode,justify='center' )
        self.comboMode.current(0) 
        self.comboMode.place(x = 110 , y =30 , width = 400 ,height = 30 )
        self.comboMode.bind(
            '<<ComboboxSelected>>', 
            self.powerDis
        )

        #強さ選択
        Static2 = ttk.Label(text=u"AIの強さ:",font=("MSゴシック","12", "bold"),background="#FFD285")
        Static2.place(x=25, y=100)

        powerlist=["強い","普通","弱い"]
        self.comboSelectpower = ttk.Combobox(self,values=powerlist,textvariable = self.power,justify='center', state = "disable")
        self.comboSelectpower.current(0) 
        self.comboSelectpower.place(x = 110 , y =100 , width = 400 ,height = 30 )

        #盤面選択
        Static5 = ttk.Label(text=u"盤面の大きさ:",font=("MSゴシック","12", "bold"),background="#FFD285")
        Static5.place(x=25, y=170)

        gridlist=["8×8","6×6"]
        self.comboGrid = ttk.Combobox(self,values=gridlist,textvariable = self.largeGrid,justify='center')
        self.comboGrid.current(0) 
        self.comboGrid.place(x = 140 , y =170 , width = 370 ,height = 30 )

        #自コマの色選択
        Static3 = ttk.Label(text=u"自コマの色:",font=("MSゴシック","12", "bold"),background="#FFD285")
        Static3.place(x=25, y=240)

        powerlist=["黒","白","赤","青","ピンク","紫","水色"]
        self.comboSelectFirstColor = ttk.Combobox(self,values=powerlist,textvariable = self.firstColor, justify='center',)
        self.comboSelectFirstColor.current(0) 
        self.comboSelectFirstColor.bind(
            '<<ComboboxSelected>>', 
            self.startDis
        )
        self.comboSelectFirstColor.place(x = 140 , y =240 , width = 175 ,height = 30 )

        #敵コマの色選択
        Static4 = ttk.Label(text=u"敵コマの色:",font=("MSゴシック","12", "bold"),background="#FFD285")
        Static4.place(x=25, y=310)

        powerlist=["黒","白","赤","青","ピンク","紫","水色"]
        self.comboSelectSecondColor= ttk.Combobox(self,values=powerlist,textvariable = self.secondColor,justify='center')
        self.comboSelectSecondColor.current(1) 
        self.comboSelectSecondColor.bind(
            '<<ComboboxSelected>>', 
            self.startDis
        )
        self.comboSelectSecondColor.place(x = 140 , y =310 , width = 175 ,height = 30 )
        
        #スタートボタン
        self.button = ttk.Button(self,text="スタート",command= self.printValue, style = "TButton")
        self.button.place(x = 200 , y =500 , width = 240 ,height = 50 )

    def printValue(self): #スタートボタンが押された時の処理
        
        self.colorA = self.changeColor(self.firstColor.get())
        self.colorB = self.changeColor(self.secondColor.get())

        if self.largeGrid.get() == "8×8":
            self.file_name = "ai.py"
        else :
            self.file_name = "66ai.py"

        if self.mode.get() == "AI":
            print("AI")

            if self.power.get() == "弱い":
                n = "1"
            elif self.power.get() == "普通":
                n = "2"
            else :
                n = "4"        

            print(n)
            self.change(n,self.file_name)
            if self.largeGrid.get() == "8×8":
                self.root = tk.Toplevel(master)
                self.app = vsAI.reversi(self.root , self.colorA , self.colorB)
            else :
                self.root = tk.Toplevel(master)
                self.app = vs66AI.reversi(self.root , self.colorA , self.colorB)
                        
        else :
            if self.largeGrid.get() == "8×8":
                self.root = tk.Toplevel(master)
                self.app = vsHuman.reversi(self.root , self.colorA , self.colorB)
            else :
                self.root = tk.Toplevel(master)
                self.app = vs66Human.reversi(self.root , self.colorA , self.colorB)
                

    def powerDis(self,event):
        if self.mode.get() == "人間":
            self.comboSelectpower["state"] = "disabled"
        elif self.mode.get() == "AI":
            self.comboSelectpower["state"] = "readnoly"
    
    def startDis(self,event):
        if self.firstColor.get() == self.secondColor.get():
            self.button["state"] = "disabled"
            self.print_text("red")
        else : 
            self.button["state"] = "normal"
            self.print_text("#FFD285")
            

    def print_text(self,color):
        self.attention = ttk.Label(text=u"※両プレイヤーを同じ色にはできません．",foreground = color,font=("MSゴシック","9", "bold"),background = "#FFD285")
        self.attention.place(x=125, y=270)
        
    def changeColor(self,color):
        if color == "黒":
                return "#000000"
        elif color == "白":
                return "white"
        elif color == "赤":
                return "red"
        elif color == "青":
                return "blue"
        elif color == "ピンク":
                return "#FF69B4"
        elif color == "紫":
                return "#9400D3"
        else : return "#00FFFF" 

    def change(self,n,file_name):

        print("change")      

        with open(file_name, encoding="utf-8") as f:
            data_lines = f.read()

        # 文字列置換
        data_lines = data_lines.replace("None", n )
        print("change")
        # 同じファイル名で保存
        with open(file_name, mode="w", encoding="utf-8") as f:
            f.write(data_lines)

def click_close():
    reset()
    master.destroy()

def reset():
    print("reset")
    file_name = "ai.py"

    with open(file_name, encoding="utf-8") as f:
        data_lines = f.read()

    # 文字列置換
        data_lines = data_lines.replace("max_depth = 1", "max_depth = None" )
        data_lines = data_lines.replace("max_depth = 2", "max_depth = None" )
        data_lines = data_lines.replace("max_depth = 3", "max_depth = None" )
        data_lines = data_lines.replace("max_depth = 4", "max_depth = None" )

    # 同じファイル名で保存
    with open(file_name, mode="w", encoding="utf-8") as f:
        f.write(data_lines)


master = Tk()

#スタイル設定
style = ttk.Style()

style.theme_use("classic")
style.configure("TFrame", background  = "#FFD285")
style.configure("TButton", background = "skyblue")


master.title("設定画面")
master.protocol("WM_DELETE_WINDOW", click_close)
select(master)
master.mainloop()