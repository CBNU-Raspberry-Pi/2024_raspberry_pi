import tkinter as tk
import random

class GridGame:
    def __init__(self):
        self.running = False  # 반복문 상태를 추적하는 변수 추가
        self.last_filled = []
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

        self.start_point_button = tk.Button(self.window, text="StartPointGrid", command=self.start_point_game)
        self.start_point_button.place(relx=0.3, rely=0.9, anchor='center')

        self.start_random_button = tk.Button(self.window, text="StartRandomGrid", command=self.start_random_game, state=tk.DISABLED)
        self.start_random_button.place(relx=0.7, rely=0.9, anchor='center')

        # 새로운 'GridGameStop' 버튼 추가
        self.stop_button = tk.Button(self.window, text="GridGameStop", command=self.stop, state=tk.DISABLED)
        self.stop_button.place(relx=0.5, rely=0.9, anchor='center')


    def start_point_game(self):
        # 모든 버튼을 초기화
        for i in range(8):
            for j in range(8):
                self.buttons[i][j].config(text="", bg="SystemButtonFace")

        # 무작위 위치 선택 (하단 4행만 선택)
        start_i, start_j = random.randint(4, 7), random.randint(0, 7)

        # 하단 격자 채우기
        self.buttons[start_i][start_j].config(text="P", bg="blue")

        # 상단 격자는 하단 격자와 점대칭으로 채우기
        symmetric_i = 7 - start_i
        symmetric_j = 7 - start_j
        self.buttons[symmetric_i][symmetric_j].config(text="P", bg="blue")

        # Enable the StartRandomGrid button
        self.start_random_button.config(state=tk.NORMAL)

    def start_random_game(self):
        self.running = True  # 반복문 시작
        self.stop_button.config(state=tk.NORMAL)  # 'GridGameStop' 버튼 활성화
        self.start_random_game_iteratively()

    def stop(self):
        self.running = False  # 반복문 중지
        self.stop_button.config(state=tk.DISABLED)  # 'GridGameStop' 버튼

    def start_random_game_iteratively(self):
        # RandomGrid에서 채워진 버튼을 초기화, 단, self.last_filled에 있는 버튼은 초기화하지 않음
        for i in range(8):
            for j in range(8):
                if self.buttons[i][j]["text"] == "R" and (i, j) not in self.last_filled:
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
        if starts_and_directions and self.running:  # 'running' 변수 확인
            start_i, start_j, direction = random.choice(starts_and_directions)

            # 선택한 시작점에서 지정된 방향으로 3칸을 채운다.
            self.last_filled = []  # 최근에 채워진 격자 위치 초기화
            for k in range(3):
                self.buttons[start_i][start_j].config(text="R", bg="red")
                self.last_filled.append((start_i, start_j))  # 채워진 격자의 위치를 self.last_filled에 추가
                start_i += direction[0]
                start_j += direction[1]
                
            # 화면을 갱신하고, 0.01초 후에 함수를 다시 호출한다.
            self.window.update_idletasks()
            self.window.after(10, self.start_random_game_iteratively)  # 500ms = 0.5 seconds
        else:
            print("No more available spots or the game was stopped. Stopping the loop.")

    def run(self):
        self.window.mainloop()

# Create and run the grid game
game = GridGame()
game.run()
