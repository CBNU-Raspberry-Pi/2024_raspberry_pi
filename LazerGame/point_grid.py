import tkinter as tk
import random

class PointGrid:
    def __init__(self):
        # UI 생성
        self.window = tk.Tk()
        self.window.title("Grid Game")
        self.window.geometry('600x600')  # UI 창 크기 조절
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.frame = tk.Frame(self.window)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.buttons = []

        for i in range(8):
            row = []
            for j in range(8):
                btn = tk.Button(self.frame, text="", width=2, height=1)
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

        self.start_button = tk.Button(self.window, text="Start", command=self.start_game)
        self.start_button.place(relx=0.5, rely=0.9, anchor='center')

    def start_game(self):
        # 모든 버튼을 초기화
        for i in range(8):
            for j in range(8):
                self.buttons[i][j].config(text="", bg="SystemButtonFace")

        # 무작위 위치 선택 (하단 4행만 선택)
        start_i, start_j = random.randint(4, 7), random.randint(0, 7)

        # 하단 격자 채우기
        self.buttons[start_i][start_j].config(text="X", bg="blue")

        # 상단 격자는 하단 격자와 점대칭으로 채우기
        symmetric_i = 7 - start_i
        symmetric_j = 7 - start_j
        self.buttons[symmetric_i][symmetric_j].config(text="X", bg="blue")

    def run(self):
        self.window.mainloop()

# Create and run the random grid game
game = PointGrid()
game.run()
