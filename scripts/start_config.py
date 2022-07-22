class CreateConfig:
    def __init__(self):
        pass

    @staticmethod
    def create(path):
        from scripts.config import Write
        t = Write()
        t.add_item("key", "SECRET_KEY", "MT@D^NO7fdANf&lW")
        t.add_item("key", "SSL_REDIRECT", "F")

        t.add_item("sql", "SQLALCHEMY_TRACK_MODIFICATIONS", "F")
        t.add_item("sql", "FLASKY_SLOW_DB_QUERY_TIME", "0.5")
        t.add_item("sql", "SQLALCHEMY_TRACK_MODIFICATIONS", "F")
        t.add_item("sql", "SQLALCHEMY_RECORD_QUERIES", "T")

        t.add_item("page", "FLASKY_POSTS_PER_PAGE", "20")
        t.add_item("page", "FLASKY_FOLLOWERS_PER_PAGE", "50")
        t.add_item("page", "FLASKY_COMMENTS_PER_PAGE", "30")

        t.add_item("sql_dev", "SQLALCHEMY_DATABASE_URI",
                   "mysql+pymysql://root:root@127.0.0.1:3306/assistant?charset=utf8")

        t.add_item("emile", "MAIL_SERVER", "SMTP_server_ip")
        t.add_item("emile", "MAIL_PORT", "465")
        t.add_item("emile", "MAIL_USERNAME", "your_email@***.***")
        t.add_item("emile", "MAIL_PASSWORD", "your_SMTP_password")
        t.add_item("emile", "MAIL_DEFAULT_SENDER", "your_email@***.***")
        t.add_item("emile", "MAIL_DEBUG", "F")
        t.add_item("emile", "MAIL_USE_TLS", "F")
        t.add_item("emile", "MAIL_USE_SSL", "T")
        t.add_item("emile", "FLASKY_MAIL_SUBJECT_PREFIX", "[Flasky]")
        t.add_item("emile", "FLASKY_MAIL_SENDER", "'Flasky Admin your_email@***.***'")

        t.add_item("img", "AVATAR_PATH", "D:\\user_avatar (a valid path to hold all the user profile)")
        t.add_item("img", "AVATAR_WIDTH", "256")
        t.add_item("img", "AVATAR_HEIGHT", "256")
        t.add_item("img", "AVATAR_MIN_WIDTH", "40")
        t.add_item("img", "AVATAR_MIN_HEIGHT", "40")
        t.write(path)


if __name__ == "__main__":
    n = input("do you want to create config file? [y/n]")
    if n == "y":
        CreateConfig.create("../config.data")
