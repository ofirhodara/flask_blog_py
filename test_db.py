from db_classes import *
from blog import *

if __name__ == '__main__':
    db.create_all()
    user1 = User(username='ofi3r1', password='ofir2474', email='ofir@2gm3ail.com')
    db.session.add(user1)
    db.session.commit()
    print(User.query.all())
    