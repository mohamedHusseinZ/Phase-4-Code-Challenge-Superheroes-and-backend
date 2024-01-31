from app import app, db, Hero, Power, HeroPower
from random import choice

with app.app_context():
    # Seeding powers
    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]
    powers = [Power(**power_data) for power_data in powers_data]
    db.session.add_all(powers)
    db.session.commit()

    # Seeding heroes
    heroes_data = [
        {"name": "Kamala Khan"},
        {"name": "Doreen Green"},
        {"name":  "zaki hussein"},
        
    ]
    heroes = [Hero(name=hero_data['name']) for hero_data in heroes_data]
    db.session.add_all(heroes)
    db.session.commit()

    # Adding powers to heroes
    strengths = ["Strong", "Weak", "Average"] 
    for hero in Hero.query.all():
        for _ in range(choice([1, 2, 3])):
            power = choice(Power.query.all())
            hero_power = HeroPower(hero=hero, power=power, strength=choice(strengths))
            db.session.add(hero_power)

            print(f"Added HeroPower: Hero '{hero.name}' has power '{power.name}' with strength '{hero_power.strength}'")

    db.session.commit()

print("🦸‍♀️ Done seeding!")



