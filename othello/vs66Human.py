import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pygame



hw = 6
dy = [0, 1, 0, -1, 1, 1, -1, -1]
dx = [1, 0, -1, 0, 1, -1, 1, -1]

CANVAS_SIZE = 400

NUM_SQUARE = 6
BOARD_COLOR = 'green' # 盤面の背景色

def empty(grid, y, x):
        return grid[y][x] == -1 or grid[y][x] == 2

def inside(y, x):
        return 0 <= y < hw and 0 <= x < hw
    
def check(grid, player,  y, x):
    res_grid = [[False for _  in range(hw)] for _ in range(hw)]
    res = 0
    for dr in range(hw):
        ny = y + dy[dr]
        nx = x + dx[dr] 
        if not inside(ny, nx):
            continue
        if empty(grid, ny, nx):
            continue
        if grid[ny][nx] == player:
            continue
        plus = 0
        flag = False
        for d in range(hw):
            nny = ny + d * dy[dr]
            nnx = nx + d * dx[dr]
            if not inside(nny, nnx):
                break
            if  empty(grid, nny, nnx):
                break
            if grid[nny][nnx] == player:
                flag = True
                break
            plus += 1
        if flag:
            res += plus
            for d in range(plus):
                nny = ny + d * dy[dr]
                nnx = nx + d * dx[dr]
                res_grid[nny][nnx] = True
    return res, res_grid

class reversi:
    def __init__(self,master,firstColor,secondColor):
        self.master = master # サブウィジェット

        self.firstColor = firstColor
        self.secondColor = secondColor
        
        self.grid = [[ -1 for _ in range(hw)] for _ in range(hw)]
        self.grid[2][2] = 1
        self.grid[2][3] = 0
        self.grid[3][2] = 0
        self.grid[3][3] = 1
        self.player = 0 # 0: 黒 1: 白
        self.nums = [2, 2]    
        # ウィジェットの作成
        self.createWidgets()

        # イベントの設定
        self.setEvents()

         # オセロゲームの初期化
        self.initOthello()
        print("OK")

    def createWidgets(self):
        '''ウィジェットを作成・配置する'''

        # キャンバスの作成
        self.canvas = tk.Canvas(
            self.master,
            bg=BOARD_COLOR,
            width=CANVAS_SIZE+1, # +1は枠線描画のため
            height=CANVAS_SIZE+1, # +1は枠線描画のため
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

    def setEvents(self):
        '''イベントを設定する'''

        # キャンバス上のマウスクリックを受け付ける
        self.canvas.bind('<ButtonPress>', self.click)

    def initOthello(self):
        '''ゲームの初期化を行う'''    
        # １マスのサイズ（px）を計算
        self.square_size = CANVAS_SIZE // NUM_SQUARE

        # マスを描画
        for y in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):
                # 長方形の開始・終了座標を計算
                xs = x * self.square_size
                ys = y * self.square_size
                xe = (x + 1) * self.square_size
                ye = (y + 1) * self.square_size
                
                # 長方形を描画
                tag_name = 'square_' + str(x) + '_' + str(y)
                self.canvas.create_rectangle(
                    xs, ys,
                    xe, ye,
                    tag=tag_name
                )
        self.check_pass()
        self.output()

    def reset_grid(self):
        self.grid = [[ -1 for _ in range(hw)] for _ in range(hw)]
        self.grid[3][3] = 1
        self.grid[3][4] = 0
        self.grid[4][3] = 0
        self.grid[4][4] = 1
        self.player = 0 # 0: 黒 1: 白
        self.nums = [2, 2]


    def click(self, event):
        '''盤面がクリックされた時の処理'''


        if self.end():
            self.reset_grid()
            self.resetOutput(3,2)
            self.resetOutput(2,3)
            self.resetOutput(4,5)
            self.resetOutput(5,4)

        # クリックされた位置がどのマスであるかを計算
        x = event.x // self.square_size
        y = event.y // self.square_size
        
        if self.check_xy(y,x) == False :
            return

        self.move(y,x)
        self.check_pass()
        self.output()
        if self.end():
            self.check_pass()
            self.output()
            self.end_game()
        
        if self.check_pass() and self.check_pass():
            self.end()


    def check_xy(self,y,x):
        if self.grid[y][x] == 2:
            return True
        else : return False

    def resetOutput(self,x,y):
        print(self.grid)
        #x1 ~ 7の表示
        print('   ', end ='')
        for i in range(hw):
            print(i, end=' ')
        #盤面表示
        print(' ')
        for y in range(hw):
            print(str(y) + '0' , end = ' ')
            for x in range(hw):
                print('〇' if self.grid[y][x] == 0 else '● ' if self.grid[y][x] == 1 else '* ' if self.grid[y][x] == 2 else '. ' , end='')
            print(' ')

                        
        #GUI表示         
        center_x = (x + 0.5) * self.square_size
        center_y = (y + 0.5) * self.square_size

        xs = center_x - (self.square_size * 0.8) // 2
        ys = center_y - (self.square_size * 0.8) // 2
        xe = center_x + (self.square_size * 0.8) // 2
        ye = center_y + (self.square_size * 0.8) // 2    

                
        tag_name = 'square_' + str(x) + '_' + str(y)
        xs = x * self.square_size
        ys = y * self.square_size
        xe = (x + 1) * self.square_size
        ye = (y + 1) * self.square_size
        self.canvas.create_rectangle(
            xs, ys,
            xe, ye,
            fill="green",
            tag=tag_name
        )

    def move(self, y, x):
        plus, plus_grid = check(self.grid, self.player, y, x)
        if (not empty(self.grid, y, x)) or (not inside(y, x)) or not plus:
            return
        self.grid[y][x] = self.player
        for ny in range(hw):
            for nx in range(hw):
                if plus_grid[ny][nx]:
                    self.grid[ny][nx] = self.player
        self.nums[self.player] += 1 + plus
        self.nums[1 - self.player] -= plus
        self.player = 1 - self.player
        self.check_pass()
        
    def move(self, y, x):
        plus, plus_grid = check(self.grid, self.player, y, x)
        if (not empty(self.grid, y, x)) or (not inside(y, x)) or not plus:
            return
        self.grid[y][x] = self.player
        for ny in range(hw):
            for nx in range(hw):
                if plus_grid[ny][nx]:
                    self.grid[ny][nx] = self.player
        self.nums[self.player] += 1 + plus
        self.nums[1 - self.player] -= plus
        self.player = 1 - self.player
        self.check_pass()
        
    def check_pass(self):
        for y in range(hw):
            for x in range(hw):
                if self.grid[y][x] == 2:
                    self.grid[y][x] = -1
        res = True
        for y in range(hw):
            for x in range(hw):
                if not empty(self.grid, y, x):
                    continue
                plus, _ = check(self.grid, self.player, y, x)
                if plus:
                    res = False
                    self.grid[y][x] = 2
        if res:
            self.player = 1 - self.player
        return res
        
    def output(self):
        
        pygame.mixer.init()
        pygame.mixer.music.load('reversi1.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

        for y in range(hw):
            for x in range(hw):
                if self.grid[y][x] == 0:
                    color = self.firstColor
                elif self.grid[y][x] == 1:
                    color = self.secondColor
                elif self.grid[y][x] == 2:
                    color = "yellow"
                else :
                    color = "green"
                         
                center_x = (x + 0.5) * self.square_size
                center_y = (y + 0.5) * self.square_size

                xs = x * self.square_size
                ys = y * self.square_size
                xe = (x + 1) * self.square_size
                ye = (y + 1) * self.square_size

                if self.grid[y][x] == 1 or self.grid[y][x] == 0 :
                    tag_name = 'square_' + str(x) + '_' + str(y)
                    xs = x * self.square_size
                    ys = y * self.square_size
                    xe = (x + 1) * self.square_size
                    ye = (y + 1) * self.square_size
                    self.canvas.create_rectangle(
                        xs, ys,
                        xe, ye,
                        fill="green",
                        tag=tag_name
                    )

                    xs = center_x - (self.square_size * 0.8) // 2
                    ys = center_y - (self.square_size * 0.8) // 2
                    xe = center_x + (self.square_size * 0.8) // 2
                    ye = center_y + (self.square_size * 0.8) // 2    

                    tag_name = 'disk_' + str(x) + '_' + str(y)
                    self.canvas.create_oval(
                        xs, ys,
                        xe, ye,
                        fill=color,
                        tag=tag_name
                    )
                
                elif self.grid[y][x] == 2 :
                    tag_name = 'square_' + str(x) + '_' + str(y)
                    xs = x * self.square_size
                    ys = y * self.square_size
                    xe = (x + 1) * self.square_size
                    ye = (y + 1) * self.square_size
                    self.canvas.create_rectangle(
                        xs, ys,
                        xe, ye,
                        fill=color,
                        tag=tag_name
                    )


                else :
                    tag_name = 'square_' + str(x) + '_' + str(y)
                    xs = x * self.square_size
                    ys = y * self.square_size
                    xe = (x + 1) * self.square_size
                    ye = (y + 1) * self.square_size
                    self.canvas.create_rectangle(
                        xs, ys,
                        xe, ye,
                        fill=color,
                        tag=tag_name
                    )

    
    def getgrid(self):
        return self.grid

    def setgrid(self,y,x,n):
        self.grid[y][x] = n
        return self.grid


    def end(self):
        if min(self.nums) == 0:
            return True
        res = True
        for y in range(hw):
            for x in range(hw):
                if self.grid[y][x] == -1 or self.grid[y][x] == 2:
                    res = False
        return res

    def end_game(self):
        if self.nums[0] > self.nums[1] :
            ResultColor = self.changeColor(self.firstColor)
            n = messagebox.showinfo("ゲーム終了", ResultColor + "の勝ち！")  
        elif self.nums[1] > self.nums[0]:
            ResultColor = self.changeColor(self.secondColor)  
            n = messagebox.showinfo("ゲーム終了", ResultColor + "の勝ち！")
        else:
            n = messagebox.showinfo("ゲーム終了", "引き分け！")
           

        

        if n == "ok":
            self.destroyer()
    
    def execute(self):
        self.master.attributes("-topmost", True)

    def changeColor(self,color):
        if color == "#000000":
                return "黒"
        elif color == "white":
                return "白"
        elif color == "red":
                return "赤"
        elif color == "blue":
                return "青"
        elif color == "#FF69B4":
                return "ピンク"
        elif color == "#9400D":
                return "紫"
        else : return "水色" 

    def destroyer(self):
        self.master.destroy()
