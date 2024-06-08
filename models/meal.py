from database import db
import json

class Meal(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  description = db.Column(db.String(80), nullable=False) 
  date = db.Column(db.DateTime, nullable=False)
  diet = db.Column(db.Boolean, nullable=False)
