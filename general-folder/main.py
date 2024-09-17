import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from os.path import join
from pathlib import Path
from tkinter import messagebox

import qrcode
from PIL import Image, ImageTk

Base_Dir = Path(__file__).parent


class DB:
    def read(self):
        with open(join(Base_Dir, f'{self.__class__.__name__.lower()}s.txt'), mode='r') as f:
            data = f.readlines()
            objects = []
            for i in data:
                tmp = i.strip('\n').split(',')
                objects.append(self.__class__(*tmp))
            return objects

    def write(self, data):
        data = '\n'.join([','.join(map(str, i.__dict__.values())) for i in data])
        with open(join(Base_Dir, f'{self.__class__.__name__.lower()}s.txt'), mode='w') as f:
            f.write(data)


class CRUD(DB):
    def create_user(self, new_user):
        users: list[User] = User().read()
        users.append(new_user)
        User().write(users)

    def create_todo(self, new_todo, user):
        todos: list[Todo] = Todo().read()
        todos.append(new_todo)
        Todo().write(todos)

    def update(self, todo: object, field, value):
        todos: list[Todo] = Todo().read()
        for i in todos:
            if i.id == todo.id:
                if field == 'title':
                    i.title = value
                if field == 'description':
                    i.description = value
                if field == 'time':
                    i.time = value
        Todo().write(todos)

    def delete(self, todo: object):
        todos: list[Todo] = Todo().read()
        for i in todos:
            if i.id == todo.id:
                todos.remove(i)
                Todo().write(todos)
                return

    def delete_user(self, user):
        users: list[User] = User().read()
        for i in users:
            if i.id == user.id:
                users.remove(i)
                User().write(users)

    def search(self, user: object, value):
        todos: list[Todo] = Todo().read()
        search_result = []
        for i in todos:
            if i.user_id == user.id and (
                    i.title.lower().startswith(value.lower()) or i.description.lower().startswith(value.lower())):
                search_result.append(i)
        return search_result

    def get_todos(self, user):
        todos: list[Todo] = Todo().read()
        result = []
        for i in todos:
            if i.user_id == user.id:
                result.append(i)
        return result

    def get_todo(self, id):
        todos: list[Todo] = Todo().read()
        for i in todos:
            if i.id == id:
                return i
        return 'Not Found'


@dataclass
class User(DB):
    id: str = None
    username: str = None
    password: str = None
    fullname: str = None


@dataclass
class Todo(DB):
    id: str = None
    user_id: str = None
    title: str = None
    description: str = None
    time: str = None
    execute_at: str = None


class Window(CRUD):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Welcome to login window')
        self.root.geometry("400x300")

        login_button = tk.Button(self.root, text='Login', command=self.login)
        login_button.pack(pady=5)

        register_button = tk.Button(self.root, text='Register', command=self.register)
        register_button.pack(pady=5)

        return_button = tk.Button(self.root, text='Exit', command=lambda: self.root.destroy())
        return_button.pack(pady=5)

        # ======================================= defition qr_code ===============================================

        data = '''https://t.me/python_and_others'''
        qr = qrcode.QRCode(version=1, box_size=3, border=5)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill='Black', back_color='White')
        file_path = join(Base_Dir, 'images')
        image_path = join(file_path, 'qr_code.png')
        img.save(image_path)

        qr_image = Image.open(image_path)
        qr_photo = ImageTk.PhotoImage(qr_image)

        qr_label = tk.Label(self.root, image=qr_photo)
        qr_label.image = qr_photo
        qr_label.pack(anchor='se', side='right', padx=10, pady=10)

        self.root.mainloop()

    def login(self):
        self.root.withdraw()
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title('Welcome to login window')
        self.login_window.geometry("400x300")
        username_label = tk.Label(self.login_window, text='Username', bg='#FF8A33', fg='#FFFFFF')
        username_label.pack(pady=5)

        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self.login_window, text='Password', bg='#FF8A33', fg='#FFFFFF')
        password_label.pack(pady=5)

        self.password_entry = tk.Entry(self.login_window, show='*')
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.login_window, text='Login', command=self.check_login)
        login_button.pack(pady=5)

        back_button = tk.Button(self.login_window, text='back ⬅️',
                                command=lambda: (self.login_window.destroy(), self.root.deiconify()))
        back_button.pack(pady=50, anchor='se', side='left', padx=5)

        self.login_window.mainloop()

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        users: list[User] = User().read()
        for user in users:
            if user.username == username and user.password == password:
                messagebox.showinfo(title='Login', message=f'Welcome {user.fullname}!')
                self.user_menu(user)
                return
        messagebox.showinfo(title='Login', message='Incorrect username or password!')

    def register(self):
        self.root.withdraw()
        self.register_window = tk.Toplevel(self.root)
        self.register_window.title('register window')
        self.register_window.geometry('400x400')

        username_label = tk.Label(self.register_window, text='Username')
        username_label.pack(pady=5)

        username_entry = tk.Entry(self.register_window)
        username_entry.pack(pady=5)

        password_label = tk.Label(self.register_window, text='Password')
        password_label.pack(pady=5)

        password_entry = tk.Entry(self.register_window)
        password_entry.pack(pady=5)

        fullname_label = tk.Label(self.register_window, text='Funlname')
        fullname_label.pack(pady=5)

        fullname_entry = tk.Entry(self.register_window)
        fullname_entry.pack(pady=5)

        users: list[User] = User().read()

        create_user_button = tk.Button(self.register_window, text='Register 📌',
                                       command=lambda: (self.create_user(User(**{
                                           'id': len(users) + 1,
                                           'username': username_entry.get(),
                                           'password': password_entry.get(),
                                           'fullname': fullname_entry.get()
                                       })), self.succes_message(), self.register_window.destroy(),
                                                        self.root.deiconify()))
        create_user_button.pack(pady=10)

    def user_menu(self, user):
        self.login_window.withdraw()
        self.user_window = tk.Toplevel(self.root)
        self.user_window.title('user_menu')
        self.user_window.geometry('400x400')

        todo_button = tk.Button(self.user_window, text='Todo 📊', command=lambda: (self.todo_menu(user)))
        todo_button.pack(pady=5)

        settings_button = tk.Button(self.user_window, text='Settings ⚙️', command=lambda: self.settings(user))
        settings_button.pack(pady=5)

        back_button = tk.Button(self.user_window, text='Back ⬅️',
                                command=lambda: (self.user_window.destroy(), self.login_window.deiconify()))
        back_button.pack(pady=50, anchor='se', side='left', padx=5)

        self.user_window.mainloop()

    def settings(self, user):
        self.user_window.withdraw()
        self.settings_window = tk.Toplevel(self.user_window)
        self.settings_window.title('settings')
        self.settings_window.geometry('400x400')

        about_button = tk.Button(self.settings_window, text='About himself 📂',
                                 command=lambda: self.about_user_message(user))
        about_button.pack(pady=5)

        edit_account_button = tk.Button(self.settings_window, text='Edit account ✏️',
                                        command=lambda: (self.edit_account_page(user)))
        edit_account_button.pack(pady=5)

        delete_account_button = tk.Button(self.settings_window, text='Delete account 🗑',
                                          command=lambda: self.delete_user_page(user))
        delete_account_button.pack(pady=5)

        back_button = tk.Button(self.settings_window, text='Back ⬅️',
                                command=lambda: (self.settings_window.destroy(), self.user_window.deiconify()))
        back_button.pack(pady=50, anchor='se', side='left', padx=5)

    def about_user_message(self, user):
        users: list[User] = User().read()
        texxt = ''
        for i in users:
            if i.id == user.id:
                texxt += 'ID: ' + i.id + '\n'
                texxt += 'Username: ' + i.username + '\n'
                texxt += 'Password: ' + i.password + '\n'
                texxt += 'Fullname: ' + i.fullname
        messagebox.showinfo(title='info', message=texxt)

    def edit_account_page(self, user):
        self.settings_window.withdraw()
        self.edit_account_window = tk.Toplevel(self.settings_window)
        self.edit_account_window.title('edit account')
        self.edit_account_window.geometry('400x400')

        fullname_button = tk.Button(self.edit_account_window, text='Fullname 🔰',
                                    command=lambda: (self.change_account_data(user, 'fullname')))
        fullname_button.pack(pady=5)

        password_button = tk.Button(self.edit_account_window, text='Password 🔑',
                                    command=lambda: (self.change_account_data(user, 'password')))
        password_button.pack(pady=5)

        back_button = tk.Button(self.edit_account_window, text='Back ⬅️',
                                command=lambda: (self.edit_account_window.destroy(), self.settings_window.deiconify()))
        back_button.pack(pady=50, anchor='se', side='left', padx=5)

    def change_account_data(self, user, field):

        self.edit_account_window.withdraw()
        change_account_window = tk.Toplevel(self.edit_account_window)
        change_account_window.title('change data')
        change_account_window.geometry('400x400')

        value_label = tk.Label(change_account_window, text='value')
        value_label.pack(pady=5)

        value_entry = tk.Entry(change_account_window)
        value_entry.pack(pady=5)

        change_button = tk.Button(change_account_window, text='confirm ☑️', command=lambda: (
        self.update_account(user, field, value_entry.get()), self.succes_message(), change_account_window.destroy(),
        self.edit_account_window.deiconify()))
        change_button.pack(pady=5)

    def update_account(self, user, field, value):

        users: list[User] = User().read()

        if field == 'fullname':
            for i in users:
                if user.id == i.id:
                    i.fullname = value
                    User().write(users)
        if field == 'password':
            for i in users:
                if user.id == i.id:
                    i.password = value
                    User().write(users)

    def delete_user_page(self, user):
        self.settings_window.withdraw()
        self.delete_user_window = tk.Toplevel(self.settings_window)
        self.delete_user_window.title('delete account')
        self.delete_user_window.geometry('400x400')

        message_label = tk.Label(self.delete_user_window, text='Delete account? 🚫')
        message_label.pack(pady=5)

        ok_button = tk.Button(self.delete_user_window, text='ok', command=lambda: (
        self.delete_user(user), self.succes_message(), self.delete_user_window.destroy(), self.root.deiconify()))
        ok_button.pack(pady=2)

        cancel_button = tk.Button(self.delete_user_window, text='cancel 🙅',
                                  command=lambda: (self.delete_user_window.destroy(), self.settings_window.deiconify()))
        cancel_button.pack(pady=50, anchor='se', side='left', padx=5)

    def todo_menu(self, user):
        self.user_window.withdraw()
        self.todo_window = tk.Toplevel(self.user_window)
        self.todo_window.geometry('400x400')

        search_button = tk.Button(self.todo_window, text='search',
                                  command=lambda: (self.open_input_search_window(user)))
        search_button.pack(pady=5)

        todo_button = tk.Button(self.todo_window, text='todo', command=lambda: (self.general_todo_menu(user)))
        todo_button.pack(pady=5)

        add_button = tk.Button(self.todo_window, text='add', command=lambda: self.add_todo(user))
        add_button.pack(pady=5)

        back_button = tk.Button(self.todo_window, text='Back',
                                command=lambda: (self.todo_window.destroy(), self.user_window.deiconify()))
        back_button.pack(pady=50, anchor='se', side='left', padx=5)

    def open_input_search_window(self, user):
        self.todo_window.withdraw()
        self.input_search_window = tk.Toplevel(self.todo_window)
        self.input_search_window.title('Search')
        self.input_search_window.geometry('400x400')

        input_search = tk.Label(self.input_search_window, text='Input Value')
        input_search.pack(pady=1)
        print(user.id, user.username)

        self.input_search_entry = tk.Entry(self.input_search_window)
        self.input_search_entry.pack(pady=1)

        input_search_button = tk.Button(self.input_search_window, text='search',
                                        command=lambda: (self.search_menu(user)))
        input_search_button.pack(pady=5)

        input_search_back_button = tk.Button(self.input_search_window, text='back ⬅️', command=lambda: (
        self.input_search_window.destroy(), self.todo_window.deiconify()))
        input_search_back_button.pack(pady=50, anchor='se', side='left', padx=5)

    def search_menu(self, user):
        self.input_search_window.withdraw()
        self.search_window = tk.Toplevel(self.input_search_window)
        self.search_window.title('Search window')
        self.search_window.geometry('400x400')

        value = self.input_search_entry.get()
        if value == '':
            messagebox.showinfo(title='error', message='Maydonga hech nima kiritilmadi 🔴')
            self.search_window.destroy()
            self.input_search_window.deiconify()
        todos = self.search(user, value)
        if len(todos) == 0:
            messagebox.showinfo(title='User', message='Hech narsa topilmadi🙁')
            self.input_search_window.destroy()
            self.todo_menu(user)
            return
        self.todos_listbox = tk.Listbox(self.search_window)
        self.todos_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = tk.Scrollbar(self.search_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.todos_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.todos_listbox.yview)
        for i in todos:
            id = f'ID: {i.id}'
            title = f'Title: {i.title}'
            description = f'Description: {i.description}'
            time = f'Time: {i.time}'
            execute_at = f'Execute At: {i.execute_at}'
            self.todos_listbox.insert(tk.END, id)
            self.todos_listbox.insert(tk.END, title)
            self.todos_listbox.insert(tk.END, description)
            self.todos_listbox.insert(tk.END, time)
            self.todos_listbox.insert(tk.END, execute_at)
            self.todos_listbox.insert(tk.END, '')

        search_id_entry = tk.Entry(self.search_window)
        search_id_entry.pack(pady=5)

        todo_id = search_id_entry.get()

        search_id_button = tk.Button(self.search_window, text='Enter ↪️',
                                     command=lambda: (self.todo_handler(user, search_id_entry.get(), todos)))
        search_id_button.pack(pady=5)

        search_menu_back = tk.Button(self.search_window, text='back ⬅️', command=lambda: (
        self.search_window.destroy(), self.input_search_window.deiconify()))
        search_menu_back.pack(pady=50, anchor='se', side='left', padx=5)

    def todo_handler(self, user: User, todo_id: str, todos):
        session_todo = None
        for i in todos:
            if i.id == todo_id:
                session_todo = i
                print(user.id)
                self.search_deeds(user, i)
                return

    def update_page(self, user: User, todo: Todo):
        self.search_deeds_window.withdraw()
        self.update_window = tk.Toplevel(self.search_deeds_window)
        title = todo.id + ' ' + todo.title
        self.update_window.title(title)
        self.update_window.geometry('400x400')

        info_label1 = tk.Label(self.update_window, text='title/description/time', fg='#F5F5BC')
        info_label1.pack(pady=5)

        field_entry = tk.Entry(self.update_window)
        field_entry.pack(pady=5)

        info_label2 = tk.Label(self.update_window, text='value', fg='#F5F5BC')
        info_label2.pack(pady=5)

        value_entry = tk.Entry(self.update_window)
        value_entry.pack(pady=5)

        update_button = tk.Button(self.update_window, text='update', command=lambda: (
        self.update(todo, field_entry.get(), value_entry.get()), self.succes_message()))
        update_button.pack(pady=5)

        back_button = tk.Button(self.update_window, text='back ⬅️',
                                command=lambda: (self.update_window.destroy(), self.search_deeds_window.deiconify()))
        back_button.pack(pady=15, anchor='se', side='left', padx=5)

    def search_deeds(self, user: User, todo: Todo):
        self.search_window.withdraw()
        self.search_deeds_window = tk.Toplevel(self.search_window)
        self.search_deeds_window.title('search deeds')
        self.search_deeds_window.geometry('400x400')

        check_todo_button = tk.Button(self.search_deeds_window, text='check 👀', command=lambda: (self.check_todo(todo)))
        check_todo_button.pack(pady=5)

        update_button = tk.Button(self.search_deeds_window, text='Update 🔄',
                                  command=lambda: (self.update_page(user, todo)))
        update_button.pack(pady=5)

        delete_button = tk.Button(self.search_deeds_window, text='Delete ⛔️',
                                  command=lambda: (self.delete(todo), self.search_menu(user), self.succes_message()))
        delete_button.pack(pady=5)

        back_button = tk.Button(self.search_deeds_window, text='back ⬅️',
                                command=lambda: (self.search_deeds_window.destroy(), self.search_window.deiconify()))
        back_button.pack(pady=20, anchor='se', side='left', padx=5)

    def succes_message(self):
        messagebox.showinfo(title='succes', message='successfully implemented ☑️')

    def check_todo(self, todo):
        id = todo.id
        get_todo_newinfo = self.send_todo(id)
        checking = f'''
        ID: {get_todo_newinfo.id}
        Title: {get_todo_newinfo.title}
        Description: {get_todo_newinfo.description}
        Time: {get_todo_newinfo.time}
        Created at: {get_todo_newinfo.execute_at}
        '''
        messagebox.showinfo(title='todo info', message=checking)

    def send_todo(self, id):
        todos: list[Todo] = Todo().read()
        for todo in todos:
            if todo.id == id:
                return todo

    def general_todo_menu(self, user: User):

        self.todo_window.withdraw()
        self.general_todo_window = tk.Toplevel(self.todo_window)
        self.general_todo_window.title('general todo')
        self.general_todo_window.geometry('400x400')

        id = user.id
        todos = self.return_todos(id)
        self.temp = self.get_todos(user)

        if len(todos) == 0:
            messagebox.showinfo(title='User', message='Hech narsa topilmadi🙁')
            self.general_todo_window.destroy()
            self.todo_menu(user)
            return
        self.todoss_listbox = tk.Listbox(self.general_todo_window)
        self.todoss_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbarr = tk.Scrollbar(self.general_todo_window)
        scrollbarr.pack(side=tk.RIGHT, fill=tk.Y)

        self.todoss_listbox.config(yscrollcommand=scrollbarr.set)
        scrollbarr.config(command=self.todoss_listbox.yview)
        for i in todos:
            id = f'ID: {i.id}'
            title = f'Title: {i.title}'
            description = f'Description: {i.description}'
            time = f'Time: {i.time}'
            execute_at = f'Execute At: {i.execute_at}'
            self.todoss_listbox.insert(tk.END, id)
            self.todoss_listbox.insert(tk.END, title)
            self.todoss_listbox.insert(tk.END, description)
            self.todoss_listbox.insert(tk.END, time)
            self.todoss_listbox.insert(tk.END, execute_at)
            self.todoss_listbox.insert(tk.END, '')

        search_entry = tk.Entry(self.general_todo_window)
        search_entry.pack(pady=5)

        enter_button = tk.Button(self.general_todo_window, text='Enter ↪️',
                                 command=lambda: (self.general_todos_deeds(user, self.get_todo(search_entry.get()))))
        enter_button.pack(pady=5)

        back_button = tk.Button(self.general_todo_window, text='back ⬅️', command=lambda: (
            self.general_todo_window.destroy(), self.todo_window.deiconify()))
        back_button.pack(pady=20, anchor='se', side='left', padx=5)

    def general_todos_deeds(self, user: User, todo: Todo):
        self.general_todo_window.withdraw()
        self.todo_deeds_window = tk.Toplevel(self.todo_window)
        self.todo_deeds_window.title('todo deeds')
        self.todo_deeds_window.geometry('400x400')

        check_button = tk.Button(self.todo_deeds_window, text='check 👀', command=lambda: self.check_todo(todo))
        check_button.pack(pady=5)

        update_button = tk.Button(self.todo_deeds_window, text='update 🔄',
                                  command=lambda: (self.todo_update_page(todo, user)))
        update_button.pack(pady=5)

        delete_button = tk.Button(self.todo_deeds_window, text='Delete ⛔️',
                                  command=lambda: self.todo_delete_page(user, todo))
        delete_button.pack(pady=5)

        back_button = tk.Button(self.todo_deeds_window, text='back ⬅️', command=lambda: (
        self.todo_deeds_window.destroy(), self.general_todo_window.deiconify()))
        back_button.pack(pady=5)

    def todo_update_page(self, todo: Todo, user: User):
        self.todo_deeds_window.withdraw()
        self.todo_update_window = tk.Toplevel(self.todo_deeds_window)
        self.todo_update_window.title('update page')
        self.todo_update_window.geometry('400x400')

        todo_id = todo.id
        current_todo = self.send_todo(todo_id)

        check_button = tk.Button(self.todo_update_window, text='Check 👀', command=lambda: self.check_todo(current_todo))
        check_button.pack(pady=5)

        title_button = tk.Button(self.todo_update_window, text='Title 📗',
                                 command=lambda: (self.todo_title_update_page(user, todo)))
        title_button.pack(pady=5)

        description_button = tk.Button(self.todo_update_window, text='Description 📜',
                                       command=lambda: (self.todo_description_update_page(user, todo)))
        description_button.pack(pady=5)

        time_button = tk.Button(self.todo_update_window, text='Time ⌛️',
                                command=lambda: (self.todo_time_update_page(user, todo)))
        time_button.pack(pady=5)

        back_button = tk.Button(self.todo_update_window, text='back ⬅️',
                                command=lambda: (self.todo_update_window.destroy(), self.todo_deeds_window.deiconify()))
        back_button.pack(pady=5)

    def todo_title_update_page(self, user, todo):
        self.todo_update_window.withdraw()
        self.title_update_window = tk.Toplevel(self.todo_update_window)
        self.title_update_window.title('title update')
        self.title_update_window.geometry('400x400')

        info_label = tk.Label(self.title_update_window, text='New value to the title', fg='#1FBFFF')
        info_label.pack(pady=5)

        value_entry = tk.Entry(self.title_update_window)
        value_entry.pack(pady=5)

        enter_button = tk.Button(self.title_update_window, text='Enter ↪️', command=lambda: (
        self.update(todo, 'title', value_entry.get()), self.succes_message(), self.title_update_window.destroy(),
        self.todo_update_window.deiconify()))
        enter_button.pack(pady=5)

    def todo_description_update_page(self, user, todo):
        self.todo_update_window.withdraw()
        self.description_update_window = tk.Toplevel(self.todo_update_window)
        self.description_update_window.title('title update')
        self.description_update_window.geometry('400x400')

        info_label = tk.Label(self.description_update_window, text='New value to the title', fg='#1FBFFF')
        info_label.pack(pady=5)

        value_entry = tk.Entry(self.description_update_window)
        value_entry.pack(pady=5)

        enter_button = tk.Button(self.description_update_window, text='Enter ↪️', command=lambda: (
        self.update(todo, 'description', value_entry.get()), self.succes_message(),
        self.description_update_window.destroy(), self.todo_update_window.deiconify()))
        enter_button.pack(pady=5)

    def todo_time_update_page(self, user, todo):
        self.todo_update_window.withdraw()
        self.time_update_window = tk.Toplevel(self.todo_update_window)
        self.time_update_window.title('title update')
        self.time_update_window.geometry('400x400')

        info_label = tk.Label(self.time_update_window, text='New value to the title', fg='#1FBFFF')
        info_label.pack(pady=5)

        value_entry = tk.Entry(self.time_update_window)
        value_entry.pack(pady=5)

        enter_button = tk.Button(self.time_update_window, text='Enter ↪️', command=lambda: (
        self.update(todo, 'time', value_entry.get()), self.succes_message(), self.time_update_window.destroy(),
        self.todo_update_window.deiconify()))
        enter_button.pack(pady=5)

    def todo_delete_page(self, user: User, todo: Todo):
        self.todo_deeds_window.withdraw()
        self.todo_delete_window = tk.Toplevel(self.todo_deeds_window)
        self.todo_delete_window.title('title update')
        self.todo_delete_window.geometry('400x400')

        question_label = tk.Label(self.todo_delete_window, text='todo delete?', fg='#1FBFFF')
        question_label.pack(pady=5)

        ok_button = tk.Button(self.todo_delete_window, text='ok', command=lambda: (
        self.delete(todo), self.todo_delete_window.destroy(), self.general_todo_menu(user), self.succes_message()))
        ok_button.pack(pady=5)

        back_button = tk.Button(self.todo_delete_window, text='back ⬅️',
                                command=lambda: (self.todo_delete_window.destroy(), self.todo_deeds_window.deiconify()))
        back_button.pack(pady=5)

    def return_todos(self, id):
        result = []
        todos: list[Todo] = Todo().read()
        for i in todos:
            if id == i.user_id:
                result.append(i)
        return result

    def add_todo(self, user):
        self.todo_window.withdraw()
        self.add_todo_window = tk.Toplevel(self.todo_window)
        self.add_todo_window.title('add todo')
        self.add_todo_window.geometry('400x400')

        title_label = tk.Label(self.add_todo_window, text='title', fg='#1FBFFF')
        title_label.pack(pady=5)

        title_entry = tk.Entry(self.add_todo_window)
        title_entry.pack(pady=5)

        description_label = tk.Label(self.add_todo_window, text='description', fg='#1FBFFF')
        description_label.pack(pady=5)

        description_entry = tk.Entry(self.add_todo_window)
        description_entry.pack(pady=5)

        time_label = tk.Label(self.add_todo_window, text='time', fg='#1FBFFF')
        time_label.pack(pady=5)

        time_entry = tk.Entry(self.add_todo_window)
        time_entry.pack(pady=5)

        todos: list[Todo] = Todo().read()

        add_todo_button = tk.Button(self.add_todo_window, text='add todo ✳️', command=lambda: (self.create_todo(Todo(**{
            'id': len(todos) + 1,
            'user_id': user.id,
            'title': title_entry.get(),
            'description': description_entry.get(),
            'time': time_entry.get(),
            'execute_at': str(datetime.now())[:-7]
        }), user), self.succes_message(), self.add_todo_window.destroy(), self.todo_window.deiconify()))
        add_todo_button.pack(pady=5)

        back_button = tk.Button(self.add_todo_window, text='back ⬅️',
                                command=lambda: (self.add_todo_window.destroy(), self.todo_window.deiconify()))
        back_button.pack(pady=5)


Window()
