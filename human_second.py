# ====================
# 人とAIの対戦
# ====================

# パッケージのインポート
from game1 import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
import tkinter as tk
import tkinter.messagebox
msg = ""
msg1 = ""
msg2 = ""
msg3 = ""
msg4 = ""
FS = ("Times New Roman", 30)
FL = ("Times New Roman", 80)


# ベストプレイヤーのモデルの読み込み
model = load_model('./model/best.h5')

# ゲームUIの定義
class GameUI(tk.Frame):
    # 初期化
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.master.title('オセロ')

        # ゲーム状態の生成
        self.state = State()

        # PV MCTSで行動選択を行う関数の生成
        self.next_action = pv_mcts_action(model, 0.0)

        # キャンバスの生成
        self.c = tk.Canvas(self, width = 1400, height = 800, highlightthickness = 0)
        self.turn_of_ai()
        self.c.bind('<Button-1>', self.turn_of_human)
        self.c.pack()

        # 描画の更新
        self.on_draw()

    
    # 人間のターン
    def turn_of_human(self,event):
        global msg, msg1,msg2,msg3,msg4
        msg = "computer in DEEEEP consideration"

        # ゲーム終了時
        if self.state.is_done():
            if self.state.is_lose():
                tkinter.messagebox.showinfo("", "コンピュータの勝ち！")
            elif self.state.is_draw():
                tkinter.messagebox.showinfo("", "引き分け")
            else:
                tkinter.messagebox.showinfo("", "あなたの勝ち！")
                
            self.state = State()
            self.on_draw()

            return

        # クリック位置を行動に変換
        x = int(event.x/100)
        y = int(event.y/100)
        if x < 0 or 7 < x or y < 0 or 7 < y: # 範囲外
            return
        action = x + y * 8

        # 合法手でない時
        if not (action in self.state.legal_actions()):
            return

        # 次の状態の取得
        self.state = self.state.next(action)
        p2 = self.state.piece_count(self.state.pieces)
        p1 = self.state.piece_count(self.state.enemy_pieces)
        msg1 = p1
        msg2 = p2
        msg3 = "you:"
        msg4 = "computer:"
        self.on_draw()

        self.master.after(1, self.turn_of_ai)

    def turn_of_ai(self):
        global msg,msg1,msg2,msg3,msg4
        msg = "your turn ^^"
        # ゲーム終了時
        if self.state.is_done():
            if self.state.is_lose():
                tkinter.messagebox.showinfo("", "あなたの勝ち！")
            elif self.state.is_draw():
                tkinter.messagebox.showinfo("", "引き分け")
            else:
                tkinter.messagebox.showinfo("", "コンピュータの勝ち！")
                
            self.state = State()
            self.on_draw()

            return

        # 行動の取得
        action = self.next_action(self.state)

        # 次の状態の取得
        self.state = self.state.next(action)
        p1 = self.state.piece_count(self.state.pieces)
        p2 = self.state.piece_count(self.state.enemy_pieces)
        msg1 = p1
        msg2 = p2
        msg3 = "you:"
        msg4 = "computer:"
        self.on_draw()
        self.draw_a_dot(action,first_player=False)

        # AIのターン
        self.master.after(1, self.turn_of_human)


    # 石の描画
    def draw_piece(self, index, first_player):
        x = (index%8)*100+10
        y = int(index/8)*100+10
        if first_player:
            self.c.create_oval(x, y, x+80, y+80, width = 1.0, outline = '#000000', fill = "black")
        else:
            self.c.create_oval(x, y, x+80, y+80, width = 1.0, outline = '#000000', fill = "white")

    def draw_a_dot(self,index,first_player):
        x = (index%8)*100+10
        y = int(index/8)*100+10
        if first_player:
            self.c.create_oval(x+35, y+35, x+45, y+45, width = 1.0, outline = '#000000', fill = "red")
        else:
            self.c.create_oval(x+35, y+35, x+45, y+45, width = 1.0, outline = '#000000', fill = "red")


    # 描画の更新
    def on_draw(self):
        self.c.delete('all')
        self.c.create_rectangle(0, 0, 800, 800, width = 0.0, fill = '#00A0FF')
        self.c.create_rectangle(800, 0, 1400, 800, width = 0.0, fill = "black")
        self.c.create_text(1100, 100, text=msg, fill="silver", font=FS)
        self.c.create_text(1100, 300, text=msg1, fill="silver", font=FS)
        self.c.create_text(1100, 500, text=msg2, fill="silver", font=FS)
        self.c.create_text(1050, 300, text=msg3, fill="silver", font=FS)
        self.c.create_text(1020, 500, text=msg4, fill="silver", font=FS)

        for i in range(1, 8):
            self.c.create_line(0, i*100, 800, i*100, width = 2.0, fill = '#0077BB')
            self.c.create_line(i*100, 0, i*100, 800, width = 2.0, fill = '#0077BB')
        
        self.c.create_line(800, 0, 800, 800, width = 2.0, fill = '#0077BB')

        for i in range(64):
            if self.state.pieces[i] == 1:
                self.draw_piece(i, self.state.is_first_player())
            if self.state.enemy_pieces[i] == 1:
                self.draw_piece(i, not self.state.is_first_player())

# ゲームUIの実行
f = GameUI(model=model)
f.pack()
f.mainloop()