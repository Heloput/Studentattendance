from tkinter import *
from SATable import  *
from SAFileDialog import *
import csv


window = Tk()
window.title("Учёт посещаемости студентов")
window["bg"] = "gray22"
window.geometry('1280x720+200+200')

# window.bind('<Button-1>', lambda e: window.destroy())


closeButton=Button(window)
closeButton["bg"] = "#383838"
# ft = tkFont.Font(family='Times',size=10)
# closeButton["font"] = ft
closeButton["fg"] = "#999999"
closeButton["justify"] = "center"
closeButton["text"] = "Х"
closeButton["command"] = window.destroy
closeButton.place(x=1260, y=0, width=20, height=20)

minimizeButton = Button(window)
minimizeButton["bg"] = "#383838"
# ft = tkFont.Font(family='Times',size=10)
# closeButton["font"] = ft
minimizeButton["fg"] = "#999999"
minimizeButton["justify"] = "center"
minimizeButton["text"] = "_"
minimizeButton.place(x=1240, y=0, width=20, height=20)
#window.bind("<Map>", frame_mapped(window))

file = open("data.csv", encoding='utf-8')
reader_object = csv.reader(file, delimiter = ",")

buttonExample = tk.Button(window,
              text="Create new window",
              command=createNewWindow)
buttonExample.pack()

table = Table(window, headings=('Фамилия', 'Имя', 'Отчество'), rows = ((2,5),(10, 12)))
table.pack(expand=tk.YES, fill=tk.BOTH)


greeting = Label(text='Привет!')

window.update()
window.mainloop()
