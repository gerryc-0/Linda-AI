from z3 import *

# don't book pregnant women
# --- EnumSort: a finite set of exactly three named values ---
Person, (Alice, Bob, Carol) = EnumSort('Person', ['Alice', 'Bob', 'Carol'])

# Predicate: Pregnant maps a Person to True/False
Pregnant = Function('Pregnant', Person, BoolSort())
Booked = Function('Booked', Person, BoolSort())
s = Solver()

s.add(Pregnant(Alice) == True)  # Alice is pregnant
s.add(Pregnant(Bob) == False)   # Bob is not pregnant
s.add(Pregnant(Carol) == False) # Carol is not pregnant

s.add(Or(Booked(Alice),Booked(Bob),Booked(Carol))) # must book somebody

# Deontological rule: do not book pregnant women
p = Const('p', Person)
s.add(ForAll([p], Implies(Pregnant(p), Not(Booked(p)))))

# --- Goal: find a satisfying MODEL (not a refutation) ---
result = s.check()
if result == sat:
    m = s.model()
    print("Result: SAT — a valid assignment was found.")
    for person, name in [(Alice, "Alice"), (Bob, "Bob"), (Carol, "Carol")]:
        print(f"  Booked({name}) = {m.evaluate(Booked(person))}")
else:
    print(f"Result: {result} — no solution exists.")