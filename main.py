import tkinter as tk
from tkinter import ttk
import csv

window = tk.Tk()
window.title("Учёт посещаемости студентов")
window["bg"] = "gray22"
window.geometry('1280x720+200+200')
frame_list = tk.Frame(window, bg='gray')
frame_list.grid(column=0, row=2, sticky='we')

file = open("data.csv", encoding="UTF-8")
reader = csv.reader(file, delimiter=";")

table = ttk.Treeview(frame_list)
table['columns'] = [0, 1, 2, 3, 4]
table['show'] = 'headings'
table.heading("#1", text="Фамилия")
table.heading("#2", text="Имя")
table.heading("#3", text="Отчество")
table.heading("#4", text="Дата")
table.heading("#5", text="Статус")
table.column("#1", width=100)
table.column("#2", width=100)
table.column("#3", width=100)
table.column("#4", width=50)
table.column("#5", width=50, anchor="center")
for row in reader:
    table.insert('', tk.END, values=row)


scroll_pane = ttk.Scrollbar(frame_list, command=table.yview())
table.configure(yscrollcommand=scroll_pane.set)
scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
table.pack(expand=tk.YES, fill=tk.BOTH)

window.update()
window.mainloop()
