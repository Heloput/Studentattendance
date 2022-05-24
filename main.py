from tkinter import *
import csv


window = Tk()
window.title("Учёт посещаемости студентов")
window["bg"] = "gray22"
window.geometry('1280x720+200+200')


file = open("data.csv", encoding='utf-8')
reader_object = csv.reader(file, delimiter = ",")

greeting = Label(text='Привет!')

window.update()
window.mainloop()
