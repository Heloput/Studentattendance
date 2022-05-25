import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import string
import csv

reader = 0
isAdmin = -1

admin_login = "admin"
admin_password = "1234"
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
    global isAdmin

    def clicked(self):
        global isAdmin
        user_get = username_entry.get()
        password_get = password_entry.get()
        if (user_get == user_login) and (password_get == user_password):
            messagebox.showinfo('Гостевой режим', 'Гость, добро пожаловать!'.format(username=user_login))
            isAdmin = 1
            self.destroy()
        elif (user_get == admin_login) and (password_get == admin_password):
            messagebox.showinfo('Администратор', 'Администратор, добро пожаловать!'.format(username=user_login))
            isAdmin = 2
            self.destroy()
        else:
            messagebox.showwarning("Ошибка!", "Неверные данные!\n Проверьте ввод!")
            isAdmin = 0
        print(isAdmin)

    window = tk.Tk()
    window.title("Авторизация")
    window["bg"] = "gray22"
    window.geometry('200x150+700+400')
    window.attributes('-toolwindow', True)
    main_label = tk.Label(window, text='Авторизация', justify="center",  fg="#eee", bg="gray22")
    main_label.pack()
    user_label = tk.Label(window, text='Имя пользователя', justify="center",  fg="#eee", bg="gray22")
    user_label.pack()
    username_entry = tk.Entry(window, bg='gray', fg='#000')
    username_entry.pack()
    password_label = tk.Label(window, text='Пароль', justify="center",  fg="#eee", bg="gray22")
    password_label.pack()
    password_entry = tk.Entry(window, bg='gray', fg='#000', show="*")
    password_entry.pack()
    send_btn = tk.Button(window, text='Войти', command=lambda: clicked(window))
    send_btn.place(relx=.4, rely=.75)

    window.mainloop()


def main_window():
    window = tk.Tk()
    window.title
    window.title("Учёт посещаемости студентов")
    window["bg"] = "gray22"
    window.geometry('800x450+200+200')
    window.resizable(0, 0)  # делает неактивной кнопку Развернуть
    frame_list = tk.Frame(window, bg='gray')
    frame_list.grid(column=0, row=0, sticky='nsew')

    table = ttk.Treeview(frame_list)
    table['columns'] = [0, 1, 2, 3, 4, 5, 6, 7]
    table.heading('#0', text='№')
    table.heading("#1", text="Фамилия")
    table.heading("#2", text="Имя")
    table.heading("#3", text="Отчество")
    table.heading("#4", text="Дата")
    table.heading("#5", text="Статус")
    table.heading("#6", text="Предмет")
    table.heading("#7", text="Пара")
    table.heading("#8", text="Преподаватель")
    table.column("#0", width=30, anchor='e')
    table.column("#1", width=100)
    table.column("#2", width=100)
    table.column("#3", width=100)
    table.column("#4", width=50)
    table.column("#5", width=50, anchor="center")
    table.column("#6", width=100, anchor="center")
    table.column("#7", width=50, anchor="center")
    table.column("#8", width=100, anchor="center")

    id = 0
    iid = 0

    for row in reader:
        table.insert('', tk.END, text=str(id), values=row)
        iid += 1
        id += 1

    scroll_pane = ttk.Scrollbar(frame_list, command=table.yview())
    table.configure(yscrollcommand=scroll_pane.set)
    scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
    table.pack(expand=tk.YES, fill=tk.BOTH)

    def insert_data():
        table.insert('', tk.END, iid=iid)

    insert_button = tk.Button(window, text="Добавить", command=insert_data)
    insert_button.grid(row=2, column=5)

    window.update()
    window.mainloop()






if download_window():
    #authorization_window()
    #if isAdmin == 1 or isAdmin == 2:
    main_window()
