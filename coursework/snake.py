# %%
from tkinter import Tk, Canvas, messagebox
import random
import tkinter


class SnakeGame:
    def __init__(self, root, snakeSize=15, snake=[], width=550, height=550, gameOver=False, pause_bt=False):
        self.snakeSize = snakeSize
        self.snake = snake
        self.width = width
        self.height = height
        self.gameOver = gameOver
        self.root = root
        self.pause_bt = pause_bt
        self.init()

    def init(self):
        self.window = self.setWindowDimensions(self.root, self.width + 100, self.height + 250)
        self.window.title("SNAKE GAME")
        self.window.geometry("600x600")
        self.title = tkinter.Label(self.window, text="SNAKE\nGAME", font=("Arial", 50), width=25, height=4).place(
            x=-300, y=5)
        self.button_start = tkinter.Button(self.window, text="START", command=self.start, font=("Arial", 10), width=15,
                                           height=4, activeforeground="white", activebackground="#6b7c85").place(x=235,
                                                                                                                 y=275)
        self.photo = tkinter.PhotoImage(file="snake.png")
        self.imgLabel = tkinter.Label(self.window, image=self.photo).place(x=350, y=50)
        l1 = tkinter.Label(self.window, text="Your Name").place(x=250, y=400)
        self.e1 = tkinter.Entry(self.window, bd=5)
        self.e1.place(x=350, y=400)
        self.button_get = tkinter.Button(self.window, text="enter", command=self.get_user, font=("Arial", 10), width=10,
                                         height=2, activeforeground="white", activebackground="#6b7c85").place(x=150,
                                                                                                               y=400)
        self.button_lb = tkinter.Button(self.window, text="leaderboard", command=self.get_leader_board,
                                        font=("Arial", 10), width=10, height=2, activeforeground="white",
                                        activebackground="#6b7c85").place(x=50, y=400)

    def get_leader_board(self):
        with open("score.txt", "r") as f:
            text_lines = f.readlines()
        lb = []
        for text in text_lines:
            v, k = text.split('\t')
            lb.append((k.replace('\n', ''), v))
        lb.sort(key=lambda k: int(k[1]), reverse=True)
        if len(lb) < 10:
            op = lb
        else:
            op = lb[:10]
        string = "\n".join("name : %s,  score: %s" % tup for tup in op)
        messagebox.showinfo(title='top 10 leader borad', message=string)

    def get_user(self):
        self.user = self.e1.get()
        self.e1.destroy()
        l2 = tkinter.Label(self.window, text=f'user:{self.user}').place(x=350, y=400)
        return self.user

    def reset(self):
        self.canvas.destroy()
        del self.snake[:]
        self.gameOver = False
        self.start()

    def start(self):
        self.canvas = Canvas(self.window, bg="#acc2d9", width=self.width, height=self.height)
        self.canvas.pack()
        self.snake.append(
            self.canvas.create_rectangle(self.snakeSize, self.snakeSize, self.snakeSize * 2, self.snakeSize * 2,
                                         fill="white"))
        self.score = 0
        txt = "Score: " + str(self.score)
        self.scoreText = self.canvas.create_text(self.width / 2, 10, fill="black", font="Times 10 italic bold",
                                                 text=txt)
        self.canvas.bind("<Left>", self.leftKey)
        self.canvas.bind("<Right>", self.rightKey)
        self.canvas.bind("<Up>", self.upKey)
        self.canvas.bind("<Down>", self.downKey)
        self.canvas.focus_set()
        self.direction = "right"
        self.placeFood()
        self.moveSnake()
        self.button_restart = tkinter.Button(self.window, text="RESTART", command=self.reset, font=("Arial", 5),
                                             width=5, height=2, activeforeground="white",
                                             activebackground="#6b7c85").place(x=5, y=550)
        self.button_pause = tkinter.Button(self.window, text="Pause", command=self.pause, font=("Arial", 5), width=5,
                                           height=2, activeforeground="white", activebackground="#6b7c85")
        self.button_pause.place(x=50, y=550)
        self.button_boss_key = tkinter.Button(self.window, text="boss", command=self.boss_key, font=("Arial", 5),
                                              width=5, height=2, activeforeground="white",
                                              activebackground="#6b7c85").place(x=100, y=550)
        self.cheat_code = tkinter.Entry(self.window, bd=5)
        self.cheat_code.place(x=250, y=550)
        self.button_cc = tkinter.Button(self.window, text="cc enter", command=self.cheat, font=("Arial", 5), width=5,
                                        height=2, activeforeground="white", activebackground="#6b7c85")
        self.button_cc.place(x=150, y=550)

    def cheat(self):
        self.code = self.cheat_code.get()
        if self.code == 'yqsxsg' and len(self.snake) > 1:
            self.canvas.delete(self.snake[-1])
            del self.snake[-1]

    def boss_key(self):
        self.canvas.destroy()
        self.window.geometry("400x400")
        self.bk_photo = tkinter.PhotoImage(file="bk.gif")
        self.bk_img = tkinter.Label(self.window, image=self.bk_photo).place(x=0, y=00)

    def pause(self):
        if self.pause_bt == True:
            self.pause_bt = not self.pause_bt
            self.button_pause.configure(text="Start")
            self.moveSnake()
        else:
            self.pause_bt = not self.pause_bt
            self.button_pause.configure(text="Pause")

    def placeFood(self):
        global food, foodX, foodY
        food = self.canvas.create_rectangle(0, 0, self.snakeSize, self.snakeSize, fill="steel blue")
        foodX = random.randint(0, self.width - self.snakeSize)
        foodY = random.randint(0, self.height - self.snakeSize)
        self.canvas.move(food, foodX, foodY)

    def leftKey(self, event):
        self.direction = "left"

    def rightKey(self, event):
        self.direction = "right"

    def upKey(self, event):
        self.direction = "up"

    def downKey(self, event):
        self.direction = "down"

    def setWindowDimensions(self, root, w, h):
        window = root
        window.title("SNAKE GAME")
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        return window

    def moveFood(self):
        global food, foodX, foodY
        self.canvas.move(food, (foodX * (-1)), (foodY * (-1)))
        foodX = random.randint(0, self.width - self.snakeSize)
        foodY = random.randint(0, self.height - self.snakeSize)
        self.canvas.move(food, foodX, foodY)

    def overlapping(self, a, b):
        if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
            return True
        return False

    def growSnake(self):
        lastElement = len(self.snake) - 1
        lastElementPos = self.canvas.coords(self.snake[lastElement])
        self.snake.append(self.canvas.create_rectangle(0, 0, self.snakeSize, self.snakeSize, fill="#FDF3F3"))
        if (self.direction == "left"):
            self.canvas.coords(self.snake[lastElement + 1], lastElementPos[0] + self.snakeSize, lastElementPos[1],
                               lastElementPos[2] + self.snakeSize, lastElementPos[3])
        elif (self.direction == "right"):
            self.canvas.coords(self.snake[lastElement + 1], lastElementPos[0] - self.snakeSize, lastElementPos[1],
                               lastElementPos[2] - self.snakeSize, lastElementPos[3])
        elif (self.direction == "up"):
            self.canvas.coords(self.snake[lastElement + 1], lastElementPos[0], lastElementPos[1] + self.snakeSize,
                               lastElementPos[2],
                               lastElementPos[3] + self.snakeSize)
        else:
            self.canvas.coords(self.snake[lastElement + 1], lastElementPos[0], lastElementPos[1] - self.snakeSize,
                               lastElementPos[2],
                               lastElementPos[3] - self.snakeSize)
        self.score += 10
        txt = "score:" + str(self.score)
        self.canvas.itemconfigure(self.scoreText, text=txt)

    def moveSnake(self):
        self.canvas.pack()
        positions = []
        positions.append(self.canvas.coords(self.snake[0]))
        if positions[0][0] < 0:
            self.canvas.coords(self.snake[0], self.width, positions[0][1], self.width - self.snakeSize, positions[0][3])
        elif positions[0][2] > self.width:
            self.canvas.coords(self.snake[0], 0 - self.snakeSize, positions[0][1], 0, positions[0][3])
        elif positions[0][3] > self.width:
            self.canvas.coords(self.snake[0], positions[0][0], 0 - self.snakeSize, positions[0][2], 0)
        elif positions[0][1] < 0:
            self.canvas.coords(self.snake[0], positions[0][0], self.height, positions[0][2],
                               self.height - self.snakeSize)
        positions.clear()
        positions.append(self.canvas.coords(self.snake[0]))
        if self.direction == "left":
            self.canvas.move(self.snake[0], -self.snakeSize, 0)
        elif self.direction == "right":
            self.canvas.move(self.snake[0], self.snakeSize, 0)
        elif self.direction == "up":
            self.canvas.move(self.snake[0], 0, -self.snakeSize)
        elif self.direction == "down":
            self.canvas.move(self.snake[0], 0, self.snakeSize)
        sHeadPos = self.canvas.coords(self.snake[0])
        foodPos = self.canvas.coords(food)
        if self.overlapping(sHeadPos, foodPos):
            self.moveFood()
            self.growSnake()
        for i in range(1, len(self.snake)):
            if self.overlapping(sHeadPos, self.canvas.coords(self.snake[i])):
                self.gameOver = True
                self.canvas.create_text(self.width / 2, self.height / 2, fill="white", font="Times 20 italic bold",
                                        text="Game Over!")
                with open("score.txt", "a") as f:
                    f.write(f'{self.score}\t{self.user}\n')
                self.get_leader_board()
        for i in range(1, len(self.snake)):
            positions.append(self.canvas.coords(self.snake[i]))
        for i in range(len(self.snake) - 1):
            self.canvas.coords(self.snake[i + 1], positions[i][0], positions[i][1], positions[i][2], positions[i][3])
        if not self.gameOver and self.pause_bt == False:
            self.window.after(100, self.moveSnake)


# %%

root = Tk()
SnakeGame(root)
root.mainloop()

# %%

