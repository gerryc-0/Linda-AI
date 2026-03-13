from z3 import *
import random

# book people today if they are urgent, else tomorrow
people = [f"person_{i}" for i in range(5)]
slots = 3 # 3 free slots opened up
Person, persons = EnumSort('Person', people)

# Predicate: Pregnant maps a Person to True/False
Urgent = Function('Urgent', Person, BoolSort())
Today = Function('Today', Person, BoolSort()) # booked today
Tomorrow = Function('Tomorrow', Person, BoolSort()) # book tomorrow
s = Solver()

urgency = {}
random.seed(42)
for i, p in enumerate(persons):
    urge = random.choice([True, False])
    urgency[i]=urge
    s.add(Urgent(p) == urge)

#can't be booked today and tomorrow
p = Const('p', Person)
s.add(ForAll([p],Not(And(Today(p),Tomorrow(p)))))

# must be booked today if uregent
for i, q in enumerate(persons):
    s.assert_and_track(Implies(Urgent(q),Today(q)),\
                       f"Patient {q} is urgent and must be booked today")

# only 3 slots left today
s.add(Sum([If(Today(p), 1, 0) for p in persons]) <= slots)

# --- Goal: find a satisfying MODEL (not a refutation) ---
result = s.check()

if result == sat:
    m = s.model()
    print("Result: SAT — a valid assignment was found.")
    for i, p in enumerate(persons):
        print(f"Patient: {p} = Urgent: {m.evaluate(Urgent(p))}, Today: {m.evaluate(Today(p))}, Tomorrow: {m.evaluate(Tomorrow(p))}")
else:
    print(f"Result: {result} — no solution exists.")
    print("Unsat core:", s.unsat_core())