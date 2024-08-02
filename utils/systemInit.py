import ast
import asyncio
from utils.databaseManager import Notice, Database
from utils.databaseSchemas import NoticeResponse
from utils.usersManager import init_user_tabel
from utils.utils import EmailManager


class SystemInit:
    def __init__(self, database_url='sqlite:///database/database.db'):
        self.database_url = database_url
        self.db = self.init_database()
        self.email_manager = self.create_email_manager()

    def init_database(self):
        """
        数据库初始化
        """
        # 判断表是否存在
        db = Database(self.database_url)
        table_names = db.table_names()
        print("数据库表名:", table_names)
        if 'order' not in table_names:
            db.create_tables()
            db.create_example_data()
        if 'user' not in table_names:
            # asyncio.run(init_user_tabel())
            asyncio.create_task(init_user_tabel())
        return db

    def create_email_manager(self):
        """
        创建邮件管理器
        """
        email_param = self.db.search_data(Notice, NoticeResponse, [Notice.name == '邮箱通知'])
        email_param = ast.literal_eval(email_param.config)
        email_manager = EmailManager(smtp_address=email_param['smtp_address'],
                                     sendmail=email_param['sendmail'],
                                     send_name=email_param['sendmail'],
                                     smtp_pwd=email_param['smtp_pwd'],
                                     smtp_port=email_param['smtp_port'])
        return email_manager
