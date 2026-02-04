## imports
from app import db, bcrypt

## table structure
class User(db.Model):
    __tablename__ = "Users"

    ID_KEY = "id"
    EMAIL_KEY = "email"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    _password = db.Column(db.String(200), nullable=False)

    cars = db.relationship("Car", foreign_keys="Car.user_id", back_populates="user", lazy = "dynamic")

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, val):
        self._password = bcrypt.generate_password_hash(val).decode("utf-8")
    
    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.EMAIL_KEY: self.email
        }
