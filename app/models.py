from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# Association Table for Many-to-Many relationship between Levels and Modules
level_module_association = db.Table('level_module',
    db.Column('level_id', db.Integer, db.ForeignKey('levels.id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('modules.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Level(db.Model):
    __tablename__ = 'levels'
    id = db.Column(db.Integer, primary_key=True)
    level_number = db.Column(db.Integer, unique=True, nullable=False) # 3, 4, 5, 6
    modules = db.relationship('Module', secondary=level_module_association, backref='levels', lazy='dynamic')

class Module(db.Model):
    __tablename__ = 'modules'
    id = db.Column(db.Integer, primary_key=True)
    module_number = db.Column(db.Integer, unique=True, nullable=False) # 1 through 8
    units = db.relationship('Unit', backref='module', lazy='dynamic', cascade="all, delete-orphan")

class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    materials = db.relationship('Material', backref='unit', lazy='dynamic', cascade="all, delete-orphan")
    flashcards = db.relationship('Flashcard', backref='unit', lazy='dynamic', cascade="all, delete-orphan")

class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    material_type = db.Column(db.String(32), nullable=False)
    content = db.Column(db.Text, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)

class Flashcard(db.Model):
    __tablename__ = 'flashcards'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)