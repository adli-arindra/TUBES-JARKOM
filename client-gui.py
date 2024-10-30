import customtkinter as ctk
import client
from const import *

class App(ctk.CTk):
    username = "undefined"

    def __init__(self):
        super().__init__()
        self.title("JUARA JARKOM")
        self.geometry("800x600")

        self.login = self.LoginPage(self)
        self.login.pack(expand=True)
        # self.changePage()

    def changePage(self):
        self.login.pack_forget()
        self.login.destroy()

        self.chat = self.ChattingRoom(self)
        self.chat.pack(expand=True, fill="both")

    class LoginPage(ctk.CTkFrame):
        p:int = 10

        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.username = self.TextBox(self)
            self.password = self.TextBox(self)
            self.usernameLabel = ctk.CTkLabel(self, text="Username")
            self.passwordLabel = ctk.CTkLabel(self, text="Password")
            self.button = ctk.CTkButton(self, text="Log in", command=self.connect)
            
            self.usernameLabel.grid(row=0, column=0, padx=self.p, pady=self.p)
            self.username.grid(row=0, column=1, padx=self.p, pady=self.p)
            self.passwordLabel.grid(row=1, column=0, padx=self.p, pady=self.p)
            self.password.grid(row=1, column=1, padx=self.p, pady=self.p)
            self.button.grid(row=2, column=0, columnspan=2, padx=self.p, pady=self.p)

            self.client = client.Client()
        
        def connect(self) -> None:
            connected = self.client.connect()
            if (not connected): 
                self.warning("Failed connecting to server")
                return
            else: 
                self.validatePassword()
        
        def validatePassword(self):
            content = self.password.get("1.0", ctk.END).strip('\n')
            valid = self.client.validate(content)
            if not valid:
                self.warning("Password is not valid")
                return
            else:
                self.validateUsername()

        def validateUsername(self):
            content = self.username.get("1.0", ctk.END).strip('\n')
            self.master.username = content
            valid = self.client.validate(content)
            if not valid:
                self.warning("Username is already taken")
                return
            else:
                self.changePage()
                
        def changePage(self):
            self.master.changePage()

        def warning(self, msg="error"):
            try:
                self.warningLabel.destroy()
            except:
                pass
            self.warningLabel = ctk.CTkLabel(self, 
                                        text=msg,
                                        text_color="red")
            self.warningLabel.grid(row=3, column=0, columnspan=2, padx=self.p, pady=self.p)
        
        class TextBox(ctk.CTkTextbox):
            def __init__(self, master, **kwargs):
                super().__init__(master,
                                 height=10,
                                 **kwargs)
                
    class ChattingRoom(ctk.CTkFrame):
        p:int = 10
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            self.top_frame = ctk.CTkFrame(self)
            self.top_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
            usernameLabel = ctk.CTkLabel(self.top_frame, text=self.master.username, font=FONT)
            portLabel = ctk.CTkLabel(self.top_frame, text=PORT, font=FONT)
            ipLabel = ctk.CTkLabel(self.top_frame, text=SERVER_IP, font=FONT)
            usernameLabel.grid(row=0, column=1, padx = self.p)
            portLabel.grid(row=0, column=2, padx = self.p)
            ipLabel.grid(row=0, column=3, padx = self.p)

            self.mid_frame = ctk.CTkScrollableFrame(self)

            self.bottom_frame = ctk.CTkFrame(self)
            textbox = ctk.CTkTextbox(self.bottom_frame, height=80, font=FONT)
            button = ctk.CTkButton(self.bottom_frame, text="Send", font=FONT, comand=self.sendMessage)

            textbox.pack(expand=True, fill="x", side="left")
            button.pack(side="right", fill="y")

            self.top_frame.pack(fill="both")
            self.mid_frame.pack(expand=True, fill="both")
            self.bottom_frame.pack(fill="both")

        def sendMessage(self):
            content = self.username.get("1.0", ctk.END).strip('\n')


        def addChatBox(self, username, message):
            chatbox = self.ChatBox(self.mid_frame, username, message)
            chatbox.pack(expand=True, fill="x")

        class ChatBox(ctk.CTkFrame):
            def __init__(self, master, username, msg, **kwargs):
                super().__init__(master, **kwargs)
                username = ctk.CTkLabel(self, text=username, font=FONT, padx = 10)
                message = ctk.CTkLabel(self, text=msg, font=FONT, anchor="w", padx = 10)

                username.pack(side="left")
                message.pack(expand=True, fill="both", side="left")

            






if __name__ == "__main__":
    app = App()
    app.mainloop()