from re import RegexFlag
from flask_bcrypt import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String,required=True,unique=True)
    password = db.Column(db.Text,required=True)
    name = db.Column(db.String)
    role = db.Column(db.String)
    department = db.Column(db.String)
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def generate_pw_hash(self):
        self.password = generate_password_hash(
            password=self.password).decode('utf-8')
    generate_pw_hash.__doc__ = generate_password_hash.__doc__
    
    def check_pw_hash(self, password: str):
        return check_password_hash(pw_hash=self.password, password=password)
    # Use documentation from BCrypt for password hashing
    check_pw_hash.__doc__ = check_password_hash.__doc__

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        if self._created:
            self.generate_pw_hash()
        super(Users, self).save(*args, **kwargs)