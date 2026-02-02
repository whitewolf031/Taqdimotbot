from dotenv import load_dotenv
import os

class BotConfig:
    def __init__(self):
        load_dotenv()
        self.getBotEnv()
        self.getAdminEnv()
        self.payment_token()

    def getBotEnv(self):
        self.token = os.getenv("TOKEN", "deafulttoken")

    def getAdminEnv(self):
        self.group_id = os.getenv("GROUP_ID", "deafultid")
        self.admin_id = os.getenv("ADMIN_ID", "admin_id")

    def payment_token(self):
        self.payme_token = os.getenv("PAYME_PROVIDER_TOKEN")