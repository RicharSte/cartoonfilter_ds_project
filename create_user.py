from getpass import getpass
import sys

from cartoonfilter_ds_project.webapp import create_app
from cartoonfilter_ds_project.webapp.model import db, User

app = create_app()

with app.app_context():
    username = input('Write here your username: ')
    
    if User.query.filter(User.username == username).count():
        print('You can\'t use this username')
        sys.exit(0)
        
    password1 = getpass('Write your password: ')
    password2 = getpass('Write your password again: ')
    
    if not password1 == password2:
        print('Passwords are not same')
        sys.exit(0)
        
    new_user = User(username=username, role='user')
    new_user.set_password(password1)
    
    db.session.add(new_user)
    db.session.commit()
    print('New User is created')
    
    