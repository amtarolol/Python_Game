states = {
            "enflammé": {"start_time": 0, "duration": 5, "damage_per_second": 2},
            "empoisonné": {"start_time": 0, "duration": 5, "damage_per_second": 2}
        }
oui = ["enflammé"]
for state in oui:
    if state in states:
        print(states[state])