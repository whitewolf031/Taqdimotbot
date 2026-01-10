from dotenv import load_dotenv
import os

class BotConfig:
    def __init__(self):
        load_dotenv()
        # self.db_bot()
        self.getBotEnv()
        # self.getAdminEnv()
        # self.group_user_names()

    def getBotEnv(self):
        self.token = os.getenv("TOKEN", "deafulttoken")

    # def getAdminEnv(self):
    #     self.admin_id = os.getenv("ADMIN_ID", "deafultid")
    #     self.group_id = os.getenv("GROUP_ID", "deafultid")
    
    # def group_user_names(self):
    #     return os.getenv("CHANNEL_USERNAMES", "@codecraftdevelop").split(",")