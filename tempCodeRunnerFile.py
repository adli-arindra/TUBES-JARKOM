essage")

        def addChatBox(self, username, message):
            chatbox = self.ChatBox(self, username, message)
            chatbox.pack(self.mid_frame)