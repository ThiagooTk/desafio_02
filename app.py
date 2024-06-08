from flask import Flask, request, jsonify, json
from models.meal import Meal
from database import db
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xxxx'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 

db.init_app(app)

#formatacao de data
date_format = "%d/%m/%y %H:%M:%S.%f"
  #date = datetime.now()

def toJSON(self):
  return json.dumps(
      self,
      default=lambda o: o.__dict__, 
      sort_keys=True,
      indent=4)

@app.route("/meal", methods=["POST"])
def create_meal():
  data = request.json
  name = data.get("name")
  description = data.get("description")
  date = datetime.strptime(data.get("date"), date_format)
  diet = data.get("diet")

  if name and description and date and diet:
    meal = Meal(name = name, description = description, date = date, diet=diet )
    db.session.add(meal)
    db.session.commit()
    return jsonify({"message": "Meal registration successful!"})
  
  return jsonify({"message": "Meal registration failed!"}), 400

@app.route("/meal/<int:id_meal>", methods=["PUT"])
def update_meal(id_meal):
  data = request.json
  meal = Meal.query.get(id_meal)

  if meal:
    meal.name = data.get("name")
    meal.description = data.get("description")
    meal.date = datetime.strptime(data.get("date"), date_format)
    meal.diet = data.get("diet")
    db.session.commit()
    return jsonify({"message": "Meal updated successfully!"})
  
  return jsonify({"message": "Meal update failed!"}), 400

@app.route("/meal/<int:id_meal>", methods=["DELETE"])
def delete_meal(id_meal):
  meal = Meal.query.get(id_meal)

  if meal:
    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": "Meal deleted successfully!"})
  
  return jsonify({"message": "Meal delete failed!"}), 400

@app.route("/meal", methods=["GET"])
def read_meal():
  meals = Meal.query.all()
  result_meals = []

  for meal in meals:
    result_meals.append(meal.name)

  return jsonify({"Meals": result_meals})

@app.route("/meal/<int:id_meal>", methods=["GET"])
def read_meal_id(id_meal):
  meal = Meal.query.get(id_meal)
  if meal:
    return jsonify({"meal":meal.name})
  
  return jsonify({"message": "Meal not found!"}), 404


if __name__ == "__main__":
  app.run(debug=True)
 
