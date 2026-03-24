from z3 import *

# adhere to booking policies and do not book medical card holders

Person, (Alice, Bob, Carol) = EnumSort('Person', ['Alice', 'Bob', 'Carol'])

Medical_Card = Function('Medical_Card', Person, BoolSort())
Booked = Function('Booked', Person, BoolSort())

s = Solver()

s.assert_and_track(Medical_Card(Bob) == True, 'Bob has a medical card') 

for p in [Alice, Bob, Carol]:
    s.assert_and_track(Booked(p),f'{p} is booked')
# s.add(And(Booked(Alice),Booked(Bob),Booked(Carol))) # system doesn't check for medical card and books everybody
# Deontological rule: do not book medical card
p = Const('p', Person)
s.add(ForAll([p], Not(And(Medical_Card(p), Booked(p)))))

result = s.check()
if result == sat:
    m = s.model()
    print("Result: SAT — a valid assignment was found.")
    for person, name in [(Alice, "Alice"), (Bob, "Bob"), (Carol, "Carol")]:
        print(f"Booked({name}) = {m.evaluate(Booked(person))}")
else:
    print(f"Result: {result} — no solution exists.")
    print('UNSAT core:', s.unsat_core())