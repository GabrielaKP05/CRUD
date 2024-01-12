import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.id_label = tk.Label(self, text="ID:")
        self.id_label.pack()
        self.id_entry = tk.Entry(self)
        self.id_entry.pack()

        self.name_label = tk.Label(self, text="Nome:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.submit_button = tk.Button(self)
        self.submit_button["text"] = "Inserir no Banco de Dados"
        self.submit_button["command"] = self.insert_into_db
        self.submit_button.pack()

    def insert_into_db(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        email = self.email_entry.get()

        if not id.isdigit():
            messagebox.showerror("Erro", "ID deve ser um número.")
            return

        if not name.isalpha():
            messagebox.showerror("Erro", "Nome deve conter apenas letras.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Erro", "Email inválido.")
            return

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='your_database',
                                                 user='your_username',
                                                 password='your_password')

            cursor = connection.cursor()
            query = "INSERT INTO users (id, name, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (id, name, email))
            connection.commit()

            messagebox.showinfo("Sucesso", "Dados inseridos com sucesso no banco de dados!")

        except mysql.connector.Error as error:
            messagebox.showerror("Erro", f"Erro ao inserir dados no MySQL: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
