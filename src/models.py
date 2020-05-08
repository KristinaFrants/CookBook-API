from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cooking(db.Model):
    __tablename__ = "cooking"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    servings = db.Column(db.String(120))
    ingridients = db.Column(db.String(4500))
    cooktime = db.Column(db.String(16))
    description = db.Column(db.String(4500))
    author = db.Column(db.String(120), nullable=False)
    cooktips = db.Column(db.String(4500))
    image = db.Column(db.String(150), nullable=True)
    # video = db.Column(db.String(150), nullable=True)
    

    def __repr__(self):
        return '<Cooking %r>' % self.recipe

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "servings": self.servings,
            "cooktime": self.cooktime,
            "ingridients": self.ingridients,
            "description": self.description,
            "author": self.author,
            "image" : self.image,
            "cooktips" : self.cooktips,
            # "alerts": list(map(lambda bubu : bubu.serialize(), self.alerts)),
            # "pets": list(map(lambda x : x.serialize(), self.pets))
        }