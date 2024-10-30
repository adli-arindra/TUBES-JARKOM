import customtkinter as ctk
import past_client

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JUARA JARKOM")
        self.geometry("800x600")

        login = self.LoginPage(self)
        login.pack(expand=True)

    # def switchPage(self, s) -> None:
    #     self.frame.pack_forget()
    #     self.frame.destroy()

    #     self.page = s

    #     if (self.page == "home"):
    #         self.frame = Homepage(self, WIDTH, HEIGHT)
    #     elif (self.page == "customerProfile"): 
    #         self.frame = CustomerProfile(self)
        
    #     self.frame.pack(expand=True, fill="both")

    class LoginPage(ctk.CTkFrame):
        p:int = 10

        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.username = self.TextBox(self)
            self.password = self.TextBox(self)
            self.usernameLabel = ctk.CTkLabel(self, text="Username")
            self.passwordLabel = ctk.CTkLabel(self, text="Password")
            self.button = ctk.CTkButton(self, text="Log in", command=self.login)
            
            self.usernameLabel.grid(row=0, column=0, padx=self.p, pady=self.p)
            self.username.grid(row=0, column=1, padx=self.p, pady=self.p)
            self.passwordLabel.grid(row=1, column=0, padx=self.p, pady=self.p)
            self.password.grid(row=1, column=1, padx=self.p, pady=self.p)
            self.button.grid(row=2, column=0, columnspan=2, padx=self.p, pady=self.p)
        
        def login(self):
            self.client, self.index = past_client.connect()
            if (not self.client): 
                self.warning("Failed connecting to server")
                return
            else: 
                self.validatePassword()
        
        def validatePassword(self):
            pw = self.password.get("1.0", ctk.END).strip('\n')
            valid = past_client.validatePassword(self.client, self.index, pw)
            if not valid:
                self.warning("Password is not valid")
                return
            else:
                self.validateUsername()

        def validateUsername(self):
            uname = self.username.get("1.0", ctk.END).strip('\n')
            valid = past_client.validateUsername(self.client, self.index, uname)
            if not valid:
                self.warning("Username is already taken")
                return
            else:
                self.warning("BERHASIL COY")


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





if __name__ == "__main__":
    app = App()
    app.mainloop()