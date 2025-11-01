import socket
from customtkinter import *
import threading

class MainWindow(CTk):

    def __init__(self):
        super().__init__()

        self.username = ""

        self.top_frame = CTkFrame(self)
        self.top_frame.pack(fill = "both", expand=True)

        self.content_frame = CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True)

        self.input_frame = CTkFrame(self.content_frame)
        self.input_frame.pack(fill="x", expand=True, side="bottom")

        self.text_box = CTkTextbox(self.content_frame)
        self.text_box.pack(padx = 20, pady=20, fill="both", expand=True)
        self.text_box.configure(state="disable")

        self.is_menu_open = False
        self.menu_width = 0
        self.menu_frame = CTkFrame(self, width=0, height=400)
        self.menu_frame.place(x = 0, y = 50)
        self.menu_frame.pack_propagate(False)


        self.name_input = CTkEntry(self.menu_frame, placeholder_text="Введить ваше ім'я...")
        self.name_input.pack(pady=20)

        self.connect_button = CTkButton(self.menu_frame, text="Підключитись", command=self.connect_server)
        self.connect_button.pack(pady=10)

        self.menu_btn = CTkButton(self.top_frame, text="Меню", command=self.toggle_menu)
        self.menu_btn.pack(side="left", padx=20)

        self.input_box = CTkEntry(self.input_frame)
        self.input_box.pack(fill="x", padx= 20, pady=20, side = "left", expand=True)

        self.btn = CTkButton(self.input_frame, text="Надіслати", command=self.send_message)
        self.btn.pack(side="right")

        self.title("LogiTalk")
        self.geometry("650x400")

        self.sock = None
        self.is_connected = False



    def toggle_menu(self):
        if self.is_menu_open:
            self.close_menu()
        else:
            self.open_menu()


    def open_menu(self):
        if self.menu_width < 200:
            self.menu_width += 20
            self.menu_frame.configure(width=self.menu_width)
            self.content_frame.pack_configure(padx=(self.menu_width + 20, 0))
            self.after(10, self.open_menu)

        else:
            self.is_menu_open = True


    def close_menu(self):
        if self.menu_width > 0:
            self.menu_width -= 20
            self.menu_frame.configure(width=self.menu_width)
            self.content_frame.pack_configure(padx=(self.menu_width, 0))
            self.after(10, self.close_menu)

        else:
            self.is_menu_open = False


    def connect_server(self):
        username = self.name_input.get()
        self.username = username

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect(('127.0.0.1', 8080))
        self.is_connected = True

        self.add_message(f"Ви приєднались як {self.username}")

        threading.Thread(target=self.receive_message, daemon=True).start()


    def send_message(self):

        if not self.is_connected:
            self.add_message("Ви не підключені")
            return

        msg = self.input_box.get()

        self.sock.sendall(f"{self.username}@{msg}\n".encode())

        self.add_message(f"Ви: {msg}")

        self.input_box.delete(0, END)



    def receive_message(self):
        buffer = ""

        while self.is_connected:
            data = self.sock.recv(1024)

            if not data:
                break
            buffer += data.decode()

            parts = buffer.split("@", 2)
            author, msg = parts
            if author != self.username:
                self.add_message(f"{author}: {msg}")


    def add_message(self, text):
        self.text_box.configure(state="normal")
        self.text_box.insert(END, f"{text}\n")
        self.text_box.configure(state="disable")



main_window = MainWindow()
main_window.mainloop()