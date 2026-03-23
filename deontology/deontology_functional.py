from z3 import *

# take deposit off someone at the weekend
Person, (Alice, Bob, Carol) = EnumSort('Person', ['Alice', 'Bob', 'Carol'])

# Predicate: Pregnant maps a Person to True/False
Deposit = Function('Deposit', Person, BoolSort())
Booked = Function('Booked', Person, BoolSort())
Weekend = Function('Weekend', Person, BoolSort())
s = Solver()

s.add(Weekend(Alice) == True)  # Alice is booked on the weekend
s.add(Weekend(Bob) == False)  
s.add(Weekend(Carol) == False)

s.add(Deposit(Alice) == True)  
s.add(Deposit(Bob) == True)    
s.add(Deposit(Carol) == False)

s.add(Or(Booked(Alice),Booked(Bob),Booked(Carol))) # must book somebody

# Deontological rule: do not keep deposit if they are not booked
p = Const('p', Person)
s.add(ForAll([p], Implies(Deposit(p), Booked(p))))
# rule 2, take deposit if they are booked on the weekend
s.add(ForAll([p], Implies(Weekend(p), Deposit(p))))
# rule 3, if they're booked on the weekend they must be booked
s.add(ForAll([p], Implies(Weekend(p), Booked(p))))



# --- Goal: find a satisfying MODEL (not a refutation) ---
result = s.check()
if result == sat:
    m = s.model()
    print("Result: SAT — a valid assignment was found.")
    for person, name in [(Alice, "Alice"), (Bob, "Bob"), (Carol, "Carol")]:
        print(f"  Booked({name}) = {m.evaluate(Booked(person))}")
else:
    print(f"Result: {result} — no solution exists.")