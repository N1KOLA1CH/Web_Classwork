from data.db_session import global_init, create_session
from data.users import User

db_name = input().strip()

global_init(db_name)
db_sess = create_session()

colonists = db_sess.query(User).filter(User.age < 18).all()
for user in colonists:
    print(f"<Colonist> {user.id} {user.surname} {user.name} {user.age} years")



