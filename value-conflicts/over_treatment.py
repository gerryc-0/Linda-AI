from z3 import *

# adhere to booking policies and do not book medical card holders

Person, (Alice, Bob, Carol) = EnumSort('Person', ['Alice', 'Bob', 'Carol'])

# toy example of value conflict
# not necessarily medically accurate but overtreatment is a real concern in dentistry
Crown = Function('Crown', Person, BoolSort())
Veneer = Function('Veneer', Person, BoolSort())
Root_Canal = Function('Root_Canal', Person, BoolSort())

s = Solver()

p = Const('p', Person)
# must have root canal if you get crown or veneer- in this toy example
s.add(ForAll([p], Implies(Crown(p),Root_Canal(p)))) 
s.add(ForAll([p], Implies(Veneer(p),Root_Canal(p))))

s.assert_and_track(Root_Canal(Bob) == True, 'Bob has a root canal')
s.assert_and_track(Crown(Bob) == True, 'Bob is getting a crown')
s.assert_and_track(Root_Canal(Alice), 'Alice is getting a root canal')
s.assert_and_track(Veneer(Carol) == True, 'Carol is getting veneers')
s.assert_and_track(Root_Canal(Carol) == False, 'Carol does not have a root canal')

result = s.check()
if result == sat:
    m = s.model()
    print("Result: SAT — a valid assignment was found.")
    for person, name in [(Alice, "Alice"), (Bob, "Bob"), (Carol, "Carol")]:
        print(f"Crown({name}) = {m.evaluate(Crown(person))}")
        print(f"Veneer({name}) = {m.evaluate(Veneer(person))}")
        print(f"Root_Canal({name}) = {m.evaluate(Root_Canal(person))}")
        print('=========')
else:
    print(f"Result: {result} — no solution exists.")
    print('UNSAT core:', s.unsat_core())