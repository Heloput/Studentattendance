import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import csv
from datetime import datetime

import sys

sys.setrecursionlimit(10000)

reader = 0
isAdmin = False

admin_login = "admin"
admin_password = "1234"
user_login = "guest"
user_password = "111"
PID = 1
IID = 1


def StringToDate(string):
    date_time_obj = datetime.strptime(string, '%d.%m.%Y')
    return date_time_obj


def DateToString(date):
    return date.strftime("%d.%m.%Y")


def delete_duplicate(my_list):
    my_list = list(set(my_list))
    return my_list


def array_column_of_CSV(index):
    results = []
    file = open("data.csv", encoding="UTF-8")
    read = csv.reader(file, delimiter=";")
    for row in read:
        if row[index] != '':
            results.append(row[index])
    return results


def array_columns_of_CSV(start=0, end=None):
    results = []
    file = open("data.csv", encoding="UTF-8")
    read = csv.reader(file, delimiter=";")
    for row in read:
        if row[start:end] != '':
            buffer = row[start:end]
            name = buffer[0] + " " + buffer[1][0] + "." + buffer[2][0] + "."
            results.append(name)
    return results


def edit_cell(tree, event):
    if tree.focus() == '':
        return False
    cur_item = int(tree.focus())
    col = tree.identify_column(event.x)

    def set_data(self):
        tree.set(cur_item, int(col[1]) - 1, main_entry.get())
        self.destroy()

    window = tk.Tk()
    window.title("Изменение значения")
    window["bg"] = "gray22"
    window.geometry('200x50+700+400')
    window.attributes('-toolwindow', True)
    main_label = tk.Label(window, text='Значение:', fg="#eee", bg="gray22")
    main_label.grid(row=0, column=0)
    main_entry = tk.Entry(window, bg='gray', fg='#000')
    main_entry.grid(row=0, column=1)
    send_btn = tk.Button(window, text='Ввод', command=lambda: set_data(window))
    send_btn.grid(row=1, column=1)

    window.update()
    window.mainloop()


def journal(data):
    full_name = array_columns_of_CSV(0, 3)
    dates = array_column_of_CSV(3)
    dates = delete_duplicate(dates)
    full_name = delete_duplicate(full_name)
    for date in range(len(dates)):
        dates[date] = StringToDate(dates[date])
    dates.sort()
    for date in range(len(dates)):
        dates[date] = DateToString(dates[date])
    full_name.sort()
    array = [[" " for x in range(len(dates))] for y in range(len(full_name))]
    for i in range(len(full_name)):
        array[i][0] = full_name[i]

    df = pd.DataFrame(full_name, columns=['ФИО/Дата'])

    table = []
    for row_id in df:
        row_str = row_id
        table.append(row_str)

    index = 1
    window = tk.Tk()
    window.title("Журнал")
    window["bg"] = "gray22"
    window.geometry('700x450+300+050')
    window.resizable(0, 0)
    frame_list = tk.Frame(window, bg='gray')

    frame_list.pack(fill="both", side="top", expand=True)
    table = ttk.Treeview(frame_list, )

    table['columns'] = [i for i in range(0, len(dates) + 1)]

    table.heading('#0', text='№')
    table.heading("#1", text="ФИО")
    table.column("#0", width=40, anchor='e')
    table.column("#1", width=110)

    for d in range(len(dates)):
        number = d + 2
        table.heading('#' + str(number), text=dates[d])
        table.column("#" + str(number), width=70, anchor='center')

    scroll_pane = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=table.yview)
    scroll_x = ttk.Scrollbar(frame_list, orient=tk.HORIZONTAL, command=table.xview)
    table.configure(yscroll=scroll_pane.set)
    table.configure(xscroll=scroll_x.set)
    scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    table.pack(expand=tk.YES, fill=tk.BOTH)

    out = list(df.itertuples(index=False, name=None))

    for row_str in out:
        table.insert('', tk.END, iid=index, text=str(index), values=row_str)
        index += 1

    children = table.get_children()
    for data_child in data.get_children():
        row = data.item(data_child)['values']
        person = row[0] + " " + row[1][0] + "." + row[2][0] + "."
        for child in children:
            if person in table.item(child)['values']:
                table.set(child, dates.index(row[3]) + 1, row[4])
    if isAdmin:
        window.bind('<Double-1>', lambda event, tree=table: edit_cell(tree, event))

    def journal_save():
        file = open("data.csv", "w", encoding="UTF-8", newline='')
        writer = csv.writer(file, delimiter=";")
        print("Journal is saved!")
        for row_journal in table.get_children():
            row_values = table.item(row_journal)['values']
            str_name = row_values[0]
            child_row = ''
            dictionary = table.set(row_journal)
            del dictionary['0']
            index_misses = 0

            for child_data in data.get_children():
                child_row = data.item(child_data)['values']
                child_name = child_row[0] + " " + child_row[1][0] + "." + child_row[2][0] + "."
                if str_name == child_name:
                    break

            for key in dictionary:
                add_list = []
                if dictionary[key] != '':
                    add_list.append(child_row[0])
                    add_list.append(child_row[1])
                    add_list.append(child_row[2])
                    add_list.append(dates[int(key) - 1])
                    add_list.append(dictionary[key])
                    writer.writerow(add_list)

                else:
                    index_misses += 1
                if len(dictionary) == index_misses:
                    add_list.append(child_row[0])
                    add_list.append(child_row[1])
                    add_list.append(child_row[2])
                    add_list.append(dates[int(key) - 1])
                    add_list.append('')
                    writer.writerow(add_list)

    def on_closing():
        if messagebox.askokcancel("Выход", "Вы хотите выйти и сохранить?"):
            if isAdmin:
                journal_save()
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.update()
    window.mainloop()


def count_misses(tree):
    table = []
    for row_id in tree.get_children():
        row = tree.item(row_id)['values']
        table.append(row)

    df = pd.DataFrame(table, columns=['Фамилия', 'Имя', "Отчество", 'Пара', "Статус"])
    df = df[["Фамилия", 'Имя', 'Отчество', "Статус"]]
    db = df[(df["Статус"] == 'н') | (df["Статус"] == 'б')]
    db = db.groupby(by=["Фамилия", "Имя", "Отчество"])['Статус'].count().reset_index(name='count')

    index = 1
    window = tk.Tk()
    window.title("Список пропусков")
    window["bg"] = "gray22"
    window.geometry('490x250+300+050')
    window.resizable(0, 0)
    frame_list = tk.Frame(window, width=450, height=650, bg='gray')
    frame_list.grid(column=0, row=0, sticky='we')
    table = ttk.Treeview(frame_list, selectmode="extended")

    table['columns'] = [0, 1, 2, 3]

    table.heading('#0', text='№')
    table.heading("#1", text="Фамилия")
    table.heading("#2", text="Имя")
    table.heading("#3", text="Отчество")
    table.heading("#4", text="Пропуски")
    table.column("#0", width=30, anchor='e')
    table.column("#1", width=120)
    table.column("#2", width=120)
    table.column("#3", width=120)
    table.column("#4", width=80, anchor='c')

    scroll_pane = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscroll=scroll_pane.set)
    scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
    table.pack(expand=tk.YES, fill=tk.BOTH)

    out = list(db.itertuples(index=False, name=None))

    for row in out:
        table.insert('', tk.END, text=str(index), values=row)
        index += 1

    def save_group(added_list):
        file = open("Список пропусков.csv", "w", encoding="1251", newline='')
        writer = csv.writer(file, delimiter=";")
        for row_ide in added_list.get_children():
            rows = added_list.item(row_ide)['values']
            writer.writerow(rows)

    save_button = tk.Button(window, text="Сохранить список", width=70, command=lambda: save_group(table))
    save_button.place(relx=0, rely=.9)

    window.update()
    window.mainloop()


def fragmentation(df):
    length = len(df)
    n = 0
    m = 0
    print(length)
    if length < 20:
        return False
    if length % 2 == 0:
        n = int(length / 2)
        m = n
    else:
        n = int(length / 2) + 1
        m = int(length / 2)
    print(n, m)

    df1 = df.iloc[:m]
    df2 = df.iloc[m:m + n]

    first = list(df1.itertuples(index=False, name=None))
    second = list(df2.itertuples(index=False, name=None))

    print(first)
    print(second)

    file = open("Первая подгруппа.csv", "w", encoding="1251", newline='')
    writer = csv.writer(file, delimiter=";")
    for row in first:
        writer.writerow(row)
    file = open("Вторая подгруппа.csv", "w", encoding="1251", newline='')
    writer = csv.writer(file, delimiter=";")
    for row in second:
        writer.writerow(row)
    messagebox.showinfo('Разбиение', 'Группа разделилась пополам!\nФайлы сохранены и находятся в директории программы!')

    return True


def grouping(tree):
    table = []
    for row_id in tree.get_children():
        row = tree.item(row_id)['values']
        table.append(row)

    group = pd.DataFrame(table, columns=['Фамилия', 'Имя', "Отчество", 'Дата', "Статус"])
    group_ready = group[["Фамилия", 'Имя', 'Отчество']]
    group_ready = group_ready.drop_duplicates()
    return group_ready


def list_group(group):
    index = 1
    window = tk.Tk()
    window.title("Список студентов")
    window["bg"] = "gray22"
    window.geometry('500x250+300+050')
    window.resizable(0, 0)
    frame_list = tk.Frame(window, width=450, height=650, bg='gray')
    frame_list.grid(column=0, row=0, sticky='we')
    table = ttk.Treeview(frame_list, selectmode="extended")

    table['columns'] = [0, 1, 2, 3, 4, 5, 6]

    table.heading('#0', text='№')
    table.heading("#1", text="Фамилия")
    table.heading("#2", text="Имя")
    table.heading("#3", text="Отчество")
    table.column("#0", width=50, anchor='e')
    table.column("#1", width=150)
    table.column("#2", width=150)
    table.column("#3", width=150)

    scroll_pane = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscroll=scroll_pane.set)
    scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
    table.pack(expand=tk.YES, fill=tk.BOTH)

    out = list(group.itertuples(index=False, name=None))

    for row in out:
        table.insert('', tk.END, text=str(index), values=row)
        index += 1

    def save_group(added_list):
        file = open("Список студентов.csv", "w", encoding="1251", newline='')
        writer = csv.writer(file, delimiter=";")
        for row_id in added_list.get_children():
            rows = added_list.item(row_id)['values']
            writer.writerow(rows)

    save_button = tk.Button(window, text="Сохранить список", width=70, command=lambda: save_group(table))
    save_button.place(relx=0, rely=.9)

    window.update()
    window.mainloop()


def delete_row(tree):
    if tree.focus() == '':
        return False
    else:
        row_id = int(tree.focus())
        tree.delete(row_id)
        return True


def edit_row(tree):
    if tree.focus() == '':
        return False

    cur_item = int(tree.focus())

    selected_item = tree.selection()
    values = tree.item(selected_item, option="values")

    add_window = tk.Tk()
    add_window.title("Ввод значений")
    add_window["bg"] = "gray22"
    add_window.geometry('250x180+900+300')
    add_window.attributes('-toolwindow', True)
    family_label = tk.Label(add_window, text='Фамилия', fg="#eee", bg="gray22")
    family_label.grid(row=0, column=0)

    family_entry = tk.Entry(add_window, bg='gray', fg='#000')
    family_entry.insert(0, values[0])
    family_entry.grid(row=0, column=1)

    user_label = tk.Label(add_window, text='Имя', justify="center", fg="#eee", bg="gray22")
    user_label.grid(row=1, column=0)

    user_entry = tk.Entry(add_window, bg='gray', fg='#000')
    user_entry.insert(0, values[1])
    user_entry.grid(row=1, column=1)

    last_label = tk.Label(add_window, text='Отчество', justify="center", fg="#eee", bg="gray22")
    last_label.grid(row=2, column=0)

    last_entry = tk.Entry(add_window, bg='gray', fg='#000')
    last_entry.insert(0, values[2])
    last_entry.grid(row=2, column=1)

    date_label = tk.Label(add_window, text='Дата', justify="center", fg="#eee", bg="gray22", width=20)
    date_label.grid(row=3, column=0)

    date_entry = tk.Entry(add_window, bg='gray', fg='#000')
    date_entry.insert(0, values[3])
    date_entry.grid(row=3, column=1)

    status_label = tk.Label(add_window, text='Статус', justify="center", fg="#eee", bg="gray22", width=20)
    status_label.grid(row=4, column=0)

    status_entry = tk.Entry(add_window, bg='gray', fg='#000')
    status_entry.insert(0, values[4])
    status_entry.grid(row=4, column=1)

    def set_data(self):
        tree.set(cur_item, 0, family_entry.get())
        tree.set(cur_item, 1, user_entry.get())
        tree.set(cur_item, 2, last_entry.get())
        tree.set(cur_item, 3, date_entry.get())
        tree.set(cur_item, 4, status_entry.get())
        self.destroy()

    edit_btn = tk.Button(add_window, text="Изменить", command=lambda: set_data(add_window))
    edit_btn.grid(row=7, column=0, columnspan=2)


def save_file(added_list):
    file = open("data.csv", "w", encoding="UTF-8", newline='')
    writer = csv.writer(file, delimiter=";")
    for row_id in added_list.get_children():
        row = added_list.item(row_id)['values']
        writer.writerow(row)
    messagebox.showinfo('Сохранение....', 'Таблица успешно сохранена!')


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
        download_lbl = tk.Label(window, text="Отсутствует файл!\n Проверьте его на наличие!\nЗагрузите файл из архива.",
                                fg="#eee", bg="gray22", justify="center")
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
            isAdmin = False
            self.destroy()
            main_window()

        elif (user_get == admin_login) and (password_get == admin_password):
            messagebox.showinfo('Администратор', 'Администратор, добро пожаловать!'.format(username=user_login))
            isAdmin = True
            self.destroy()
            main_window()

        else:
            messagebox.showwarning("Ошибка!", "Неверные данные!\n Проверьте ввод!")
            isAdmin = False
        print(isAdmin)

    window = tk.Tk()
    window.title("Авторизация")
    window["bg"] = "gray22"
    window.geometry('200x150+700+400')
    window.attributes('-toolwindow', True)
    main_label = tk.Label(window, text='Авторизация', justify="center", fg="#eee", bg="gray22")
    main_label.pack()
    user_label = tk.Label(window, text='Имя пользователя', justify="center", fg="#eee", bg="gray22")
    user_label.pack()
    username_entry = tk.Entry(window, bg='gray', fg='#000')
    username_entry.pack()
    password_label = tk.Label(window, text='Пароль', justify="center", fg="#eee", bg="gray22")
    password_label.pack()
    password_entry = tk.Entry(window, bg='gray', fg='#000', show="*")
    password_entry.pack()
    send_btn = tk.Button(window, text='Войти', command=lambda: clicked(window))
    send_btn.place(relx=.4, rely=.75)

    window.mainloop()


def main_window():
    global PID
    global IID
    window = tk.Tk()
    window.title("Учёт посещаемости студентов")
    window["bg"] = "gray22"
    window.geometry('560x350+200+200')
    window.resizable(0, 0)  # делает неактивной кнопку Развернуть
    frame_list = tk.Frame(window, bg='gray', width=444, pady=4, padx=4)
    frame_list.grid(column=0, row=0, sticky='we', columnspan=6)
    table = ttk.Treeview(frame_list, selectmode="extended")

    table['columns'] = [0, 1, 2, 3, 4]
    table.heading('#0', text='№')
    table.heading("#1", text="Фамилия")
    table.heading("#2", text="Имя")
    table.heading("#3", text="Отчество")
    table.heading("#4", text="Дата")
    table.heading("#5", text="Статус")
    table.column("#0", width=40, anchor='center')
    table.column("#1", width=120)
    table.column("#2", width=120)
    table.column("#3", width=120)
    table.column("#4", width=80, anchor="center")
    table.column("#5", width=50, anchor="center")

    for row in reader:
        table.insert('', tk.END, iid=IID, text=str(PID), values=row)
        IID += 1
        PID += 1

    scroll_pane = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscroll=scroll_pane.set)
    scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
    table.pack(expand=tk.YES, fill=tk.BOTH)

    def insert_form():
        global PID
        global IID
        add_window = tk.Tk()
        add_window.title("Ввод значений")
        add_window["bg"] = "gray22"
        add_window.geometry('280x180+900+300')
        add_window.attributes('-toolwindow', True)
        family_label = tk.Label(add_window, text='Фамилия', fg="#eee", bg="gray22")
        family_label.grid(row=0, column=0)
        family_entry = tk.Entry(add_window, bg='gray', fg='#000')
        family_entry.grid(row=0, column=1)
        user_label = tk.Label(add_window, text='Имя', justify="center", fg="#eee", bg="gray22")
        user_label.grid(row=1, column=0)
        user_entry = tk.Entry(add_window, bg='gray', fg='#000')
        user_entry.grid(row=1, column=1)
        last_label = tk.Label(add_window, text='Отчество', justify="center", fg="#eee", bg="gray22")
        last_label.grid(row=2, column=0)
        last_entry = tk.Entry(add_window, bg='gray', fg='#000')
        last_entry.grid(row=2, column=1)
        date_label = tk.Label(add_window, text='Дата', justify="center", fg="#eee", bg="gray22", width=20)
        date_label.grid(row=3, column=0)
        date_entry = tk.Entry(add_window, bg='gray', fg='#000')
        date_entry.grid(row=3, column=1)
        status_label = tk.Label(add_window, text='Статус', justify="center", fg="#eee", bg="gray22", width=20)
        status_label.grid(row=4, column=0)
        status_entry = tk.Entry(add_window, bg='gray', fg='#000')
        status_entry.grid(row=4, column=1)

        def insert_data():
            global PID
            global IID
            if len(family_entry.get()) == 0 and len(user_entry.get()) == 0 and len(last_entry.get()) == 0 and len(
                    date_entry.get()) == 0:
                messagebox.showwarning("Вводимые поля", "Пустые поля!\nВведите данные!")
            else:
                table.insert('', tk.END, iid=IID, text=str(PID), values=(
                    family_entry.get(), user_entry.get(), last_entry.get(), date_entry.get(), status_entry.get()))
                add_window.destroy()
                PID += 1
                IID += 1

        add_btn = tk.Button(add_window, text="Добавить", command=insert_data)
        add_btn.grid(row=7, column=0, columnspan=2)

        add_window.update()
        add_window.mainloop()

    if isAdmin:
        insert_button = tk.Button(window, text="Добавить", command=insert_form)
        insert_button.grid(row=2, column=0)

        edit_button = tk.Button(window, text="Изменить", command=lambda: edit_row(table))
        edit_button.grid(row=2, column=1)

        save_btn = tk.Button(window, text="Сохранить", command=lambda: save_file(table))
        save_btn.grid(row=2, column=2, )

        delete_btn = tk.Button(window, text="Удалить", command=lambda: delete_row(table))
        delete_btn.grid(row=2, column=3, )

        window.bind('<Double-1>', lambda event, tree=table: edit_cell(tree, event))

    border_label = tk.Label(window, text="Работа с отчётами", bg="gray22", fg="#eee")
    border_label.grid(row=3, column=0, columnspan=2)

    list_students = grouping(table)

    list_button = tk.Button(window, text="Список группы", command=lambda: list_group(list_students))
    list_button.grid(row=4, column=0)

    fragment_button = tk.Button(window, text="Разбить группу", command=lambda: fragmentation(list_students))
    fragment_button.grid(row=4, column=1)

    misses_button = tk.Button(window, text="Список пропусков", command=lambda: count_misses(table))
    misses_button.grid(row=4, column=2)

    journal_button = tk.Button(window, text="Журнал", command=lambda: journal(table))
    journal_button.grid(row=4, column=3)

    window.update()
    window.mainloop()


if download_window():
    authorization_window()

