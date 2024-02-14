import tkinter as tk
import random

class RandomGrid:
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
    # RandomGrid에서 채워진 버튼을 초기화
    for i in range(8):
        for j in range(8):
            if self.buttons[i][j]["text"] == "R":
                self.buttons[i][j].config(text="", bg="SystemButtonFace")

    # 모든 가능한 시작점과 방향을 구한다.
    starts_and_directions = []
    for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # 오른쪽, 아래, 왼쪽, 위
        for i in range(8):
            for j in range(8):
                if self.buttons[i][j]["text"] != "P":
                    can_fill = True
                    for k in range(3):
                        ni, nj = i + direction[0]*k, j + direction[1]*k
                        if not (0 <= ni < 8 and 0 <= nj < 8) or self.buttons[ni][nj]["text"] == "P":
                            can_fill = False
                            break
                    if can_fill:
                        starts_and_directions.append((i, j, direction))

    # 가능한 시작점과 방향 중에서 무작위로 하나를 선택한다.
    if starts_and_directions:
        start_i, start_j, direction = random.choice(starts_and_directions)

        # 선택한 시작점에서 지정된 방향으로 3칸을 채운다.
        for k in range(3):
            self.buttons[start_i][start_j].config(text="R", bg="red")
            start_i += direction[0]
            start_j += direction[1]

    def run(self):
        self.window.mainloop()

# Create and run the random grid game
game = RandomGrid()
game.run()
