import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import graph_maker 
import numpy as np

class App:
	def __init__(self, window, video_source=0):
		self.window = window
		self.window.geometry("1280x680")
		self.window.title=("Raspberry_Pi Spectrometer")
		self.video_source=video_source
        
        # 카메라 화면 
		self.vid= MyVideoCapture(self.video_source)
		self.canvas_1=tkinter.Canvas(self.window, width=640, height = 400)
		self.canvas_1.grid(row=0, column=0)

		# 그래프 화면
		self.canvas_2=tkinter.Canvas(self.window,width=640, height = 400)
		self.canvas_2.grid(row=0, column=1)

        # 이미지에서 Y 위치 변경
		y_Label = tkinter.Label(self.window, text=' Set Y location ', bg=self.from_rgb((225, 240, 200)), font=("Arial", 18))
		y_Label.place(x=0, y=400,height=40,width=640)

		self.y_scale = tkinter.Scale(self.window , from_=0, to=399, orient="horizontal")
		self.y_scale.place(x=0, y=440,height=40,width=640)

        # 이미지에서 밝기 변경
		bright_Label = tkinter.Label(self.window, text=' Set bright ', bg=self.from_rgb((225, 240, 200)), font=("Arial", 18))
		bright_Label.place(x=640, y=400,height=40,width=640)

		self.bright_scale = tkinter.Scale(self.window , resolution = 0.1, from_=0, to=3.0, orient="horizontal")
		self.bright_scale.place(x=640, y=440,height=40,width=640)

        # 이미지에서 X1 위치 변경
		x1_Label = tkinter.Label(self.window, text=' Set X_1 location ', bg=self.from_rgb((225, 240, 200)), font=("Arial", 18))
		x1_Label.place(x=0, y=480,height=40,width=640)

		self.x1_scale = tkinter.Scale(self.window , from_=0, to=640,  orient="horizontal")
		self.x1_scale.place(x=0, y=520,height=40,width=640)

        # 이미지에서 X2 위치 변경
		x2_Label = tkinter.Label(self.window, text=' Set X_2 location ', bg=self.from_rgb((225, 240, 200)), font=("Arial", 18))
		x2_Label.place(x=0, y=560,height=40,width=640)

		self.x2_scale = tkinter.Scale(self.window, from_=0, to=640,  orient="horizontal")
		self.x2_scale.place(x=0, y=600,height=40,width=640)
		
		# x_wave number 설정
		## x1 wave number 설정
		WN_x1_Label = tkinter.Label(self.window, text=' Wave number x1 ', bg=self.from_rgb((225, 240, 200)), font=("Arial", 18))
		WN_x1_Label.place(x=640, y=480,height=40,width=320)

		self.WN_x1_entry = tkinter.Entry(self.window, font=("Arial", 18))
		self.WN_x1_entry.place(x=640, y=520,height=40,width=320)

		## x2 wave number 설정
		WN_x2_Label = tkinter.Label(self.window, text=' Wave number x1 ', bg=self.from_rgb((225, 240, 200)), font=("Arial", 18))
		WN_x2_Label.place(x=960, y=480,height=40,width=320)

		self.WN_x2_entry = tkinter.Entry(self.window, font=("Arial", 18))
		self.WN_x2_entry.place(x=960, y=520,height=40,width=320)

		self.WN_btn = tkinter.Button(self.window, text="wavenumber set", width=15, height=40, font=("Arial", 18), command=self.Change_WN)
		self.WN_btn.place(x=640, y=560,height=40,width=640)

		self.WN_x1 = 350
		self.WN_x2 = 750

		## save 버튼
		self.save_entry = tkinter.Entry(self.window, font=("Arial", 18))
		self.save_entry.place(x=640, y=600,height=40,width=780)

		self.btn_save=tkinter.Button(self.window, text="save",width=15, height=40, font=("Arial", 18), command=self.save_graph)
		self.btn_save.place(x=1140, y=600,height=40,width=140)

		# 좌측 하단 버튼 프레임
		btn_frame = tkinter.Frame(self.window) 
		btn_frame.place(x=0, y=640, height=40, width=640)

		## image/camera 전환 버튼
		self.Change_btn=tkinter.Button(btn_frame, text="Camera",width=23, height=40, font=("Arial", 18), command=self.Change)
		self.Change_btn.pack(side="left")

		## capture 버튼
		self.capture_btn=tkinter.Button(btn_frame, text="capture",width=23, height=40, font=("Arial", 18), command=self.snapshot)
		self.capture_btn.pack(side="left")

		self.delay=50

		self.update()
		self.window.mainloop()

	# 이미지 분석 모드/ 카메라 모드 전환
	def Change(self):
		if self.Change_btn['text'] == "Camera":
			self.Change_btn['text'] = "Image"
			self.capture_btn['text'] = "image select"
			self.fileName ="sample.png"
			self.capture_btn['command'] = self.ask

		else:
			self.Change_btn['text'] = "Camera"
			self.capture_btn['text'] = "capture"
			self.capture_btn['command'] = self.snapshot

	# 그래프 저장 
	def save_graph(self):
		cv2.imwrite("graph_image/"+str(self.save_entry.get()) + ".jpg", cv2.cvtColor(self.graph, cv2.COLOR_RGB2BGR) )


	# 카메라 촬영
	def snapshot(self):
		ret, frame=self.vid.get_frame()

		if ret:
			cv2.imwrite("camera_image/"+time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) )
	
	def ask(self):
		self.window.file=tkinter.filedialog.askopenfile(initialdir='path', title='select file')
		self.fileName = self.window.file.name


	# 파장값 변환
	def Change_WN(self):
		if self.WN_x1_entry.get() or self.WN_x2_entry.get() != "":
			interval = (int(self.WN_x2_entry.get())- int(self.WN_x1_entry.get()))/(self.x2_scale.get() - self.x1_scale.get())
			self.WN_x1 = int(self.WN_x1_entry.get()) - self.x1_scale.get()*interval
			self.WN_x2 = self.WN_x1 + 640 * interval
		else:
			self.WN_x1 = 350
			self.WN_x2 = 750

	def update(self):

		if self.Change_btn['text'] == "Camera":
			ret, frame = self.vid.get_frame()
			frame = cv2.resize(frame, (640,400) ,interpolation=cv2.INTER_AREA)
		else:
			frame = cv2.cvtColor(cv2.imread(self.fileName),cv2.COLOR_BGR2RGB) 
			frame = cv2.resize(frame, (640,400) ,interpolation=cv2.INTER_AREA)

		frame = np.clip((1+self.bright_scale.get()) * frame - 128 * self.bright_scale.get(), 0, 255).astype(np.uint8)

		# 그래프 업데이트 
		gray_image= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		flux = gray_image[int(self.y_scale.get()),:]
		gragh_maker = graph_maker.make_graph()
		self.graph = gragh_maker.make_image(self.WN_x1, self.WN_x2, flux)
		self.graph = cv2.resize(self.graph, (640,400) ,interpolation=cv2.INTER_AREA)
		self.graph_img = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.graph))
		self.canvas_2.create_image(0,0, image=self.graph_img, anchor=tkinter.NW)
		
		# 카메라 이미지 편집 
		white = (255,255,255)
		cv2.line(frame,(0,self.y_scale.get()),(640,self.y_scale.get()),white,1)
		cv2.line(frame,(self.x1_scale.get(),0),(self.x1_scale.get(),400), white,1 )
		cv2.line(frame,(self.x2_scale.get(),0),(self.x2_scale.get(),400), white,1 )

		# 카메라 이미지 업데이트 
		self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
		self.canvas_1.create_image(0,0, image=self.photo, anchor=tkinter.NW)

		self.window.after(self.delay, self.update)

	def from_rgb(self,rgb):
		return "#%02x%02x%02x" % rgb


class  MyVideoCapture:
	def __init__(self, video_source=0):
		self.vid = cv2.VideoCapture(video_source)
		if not self.vid.isOpened():
			raise ValueError("unable open video source", video_source)

	def get_frame(self):
		if self.vid.isOpened():
			ret, frame = self.vid.read()
			if ret:
				frame = cv2.resize(frame, (640,400) ,interpolation=cv2.INTER_AREA)
				return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
			else:
				return (ret, None)
		else:
			return (ret,None)		
	def __del__(self):
		if self.vid.isOpened():
			self.vid.release()

App(tkinter.Tk())