import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import string
import csv

reader = 0
isAdmin = False
user = 0
password = 0

admin_login = "admin"
admin_password="1234"
user_login = "guest"
user_password = "111"


def download_window():
    try:
        file = open("data.csv", encoding="UTF-8")
        global reader
        reader = csv.reader(file, delimiter=";")
        return True

    except csv.Error:
        print("ERROR")
        return False
    except FileNotFoundError:
        window = tk.Tk()
        window.title("Загрузка файла")
        window["bg"] = "gray22"
        window.geometry('300x100+700+400')
        window.resizable(False, False)
        print("Файл не существует!")
        download_lbl = tk.Label(window, text="Отсутствует файл!\n Проверьте его на наличие!\nЗагрузите файл из архива.", fg="#eee", bg="gray22", justify="center")
        download_lbl.place(relx=.2, rely=.2)
        button = tk.Button(window, text="Окей", command=window.destroy)
        button.place(relx=.85, rely=.7)
        window.update()
        window.mainloop()

        return False


def authorization_window():
    global admin_login
    global admin_password
    global user_login
    global user_password

    def clicked():
        global user
        global password
        user_get = username_entry.get()
        password_get = password_entry.get()
        if (user_get == user_login) and (password_get == user_password):
            messagebox.showinfo('Заголовок', '{username}, {password}'.format(username=user, password=password))

    window = tk.Tk()
    window.title("Загрузка файла")
    window["bg"] = "gray22"
    window.geometry('300x150+700+400')
    window.resizable(False, False)
    main_label = tk.Label(window, text='Авторизация', justify="center",  fg="#eee", bg="gray22")
    main_label.pack()
    user_label = tk.Label(window, text='Имя пользователя', justify="center",  fg="#eee", bg="gray22")
    user_label.pack()
    username_entry = tk.Entry(window, bg='gray', fg='#000')
    username_entry.pack()
    password_label = tk.Label(window, text='Пароль', justify="center",  fg="#eee", bg="gray22")
    password_label.pack()
    password_entry = tk.Entry(window, bg='gray', fg='#000')
    password_entry.pack()
    send_btn = tk.Button(window, text='Войти', command=clicked)
    send_btn.pack()



    window.mainloop()

def main_window():
    window = tk.Tk()
    window.title
    window.title("Учёт посещаемости студентов")
    window["bg"] = "gray22"
    window.geometry('800x450+200+200')
    frame_list = tk.Frame(window, bg='gray')
    frame_list.grid(column=0, row=2, sticky='we')
    table = ttk.Treeview(frame_list)
    table['columns'] = [0, 1, 2, 3, 4, 5, 6, 7]
    table['show'] = 'headings'
    table.heading("#1", text="Фамилия")
    table.heading("#2", text="Имя")
    table.heading("#3", text="Отчество")
    table.heading("#4", text="Дата")
    table.heading("#5", text="Статус")
    table.heading("#6", text="Предмет")
    table.heading("#7", text="Режим занятий")
    table.heading("#8", text="Преподаватель")
    table.column("#1", width=100)
    table.column("#2", width=100)
    table.column("#3", width=100)
    table.column("#4", width=50)
    table.column("#5", width=50, anchor="center")
    table.column("#6", width=100, anchor="center")
    table.column("#7", width=50, anchor="center")
    table.column("#8", width=100, anchor="center")

    for row in reader:
        table.insert('', tk.END, values=row)

    scroll_pane = ttk.Scrollbar(frame_list, command=table.yview())
    table.configure(yscrollcommand=scroll_pane.set)
    scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
    table.pack(expand=tk.YES, fill=tk.BOTH)

    window.update()
    window.mainloop()


if download_window():
    #main_window()
    authorization_window()
