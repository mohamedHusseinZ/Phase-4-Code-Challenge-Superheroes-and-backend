


import os
from flask import Flask, jsonify, request  # Add this import
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)






@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{'id': hero.id, 'name': hero.name} for hero in heroes]
    return jsonify(heroes_data)    



@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero_by_id(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        return jsonify({'id': hero.id, 'name': hero.name})
    else:
        return jsonify({'message': 'Hero not found'}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(powers_data)

@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power_by_id(power_id):
    power = Power.query.get(power_id)
    if power:
        return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
    else:
        return jsonify({'message': 'Power not found'}), 404

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return jsonify({'message': 'Power not found'}), 404

    data = request.get_json()
    if 'description' in data:
        power.description = data['description']
        db.session.commit()
        return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
    else:
        return jsonify({'message': 'Invalid request'}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if not all([hero_id, power_id, strength]):
        return jsonify({'message': 'Invalid request. Missing required data'}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return jsonify({'message': 'Hero or Power not found'}), 404

    hero_power = HeroPower(hero=hero, power=power, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify({'message': 'HeroPower created successfully'}), 201

if __name__ == '__main__':
    app.run(port=5000, debug=True)
