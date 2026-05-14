from users import User
import db_session

db_session.global_init("db.sqlite")
session = db_session.create_session()

user = User()
user.email = "test@example.com"
user.name = "Test User"
user.set_password("password")
session.add(user)
session.commit()