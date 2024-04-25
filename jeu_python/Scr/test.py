spell_properties = {
            "fireball": {"icon": "ressources/sort/spell_bar/feu.PNG", "max_range": 300,
                         "cd": 80, "use": False},
            "iceball": {"icon":"ressources/sort/spell_bar/glace.JPG", "max_range": 500,
                        "cd": 80, "use": False},
            "lave": {"icon": "ressources/sort/spell_bar/lave.JPG", "max_range": 1500,
                     "cd": 0, "use": False}
        }

for spell, properties in spell_properties.items():
    if properties["use"]:
        print("utilisé")
    else:
        print("non")
    properties["cd"] += 1
    print(properties["cd"])
