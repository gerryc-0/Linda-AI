from z3 import *
import random

# take deposit off someone at the weekend
people = [f"person_{i}" for i in range(10)]
Person, patients = EnumSort('Person', people)

# Take depoists on weekends 
Deposit = Function('Deposit', Person, BoolSort())
Booked = Function('Booked', Person, BoolSort())
Weekend = Function('Weekend', Person, BoolSort())
HighDemandDentist = Function('HighDemandDentist', Person, BoolSort())
SameDayBooking = Function('SameDayBooking', Person, BoolSort())
LongAppointment = Function('LongAppointment', Person, BoolSort())
BankHoliday = Function('BankHolidays', Person, BoolSort())
BadHistory =  Function('BadHistory', Person, BoolSort()) # has high no-show rate (apt type/)
s = Solver()

random.seed(42)
for i, p in enumerate(patients):
    w = random.choice([True, False])
    hd = random.choice([True, False])
    sd = random.choice([True, False])
    la = random.choice([True, False])
    h = random.choice([True, False])
    d = random.choice([True, False])
    if w:
        bh = False
    else:
        bh = random.choice([True, False])
    s.assert_and_track(Weekend(p) == w, f"patient_{i}, Weekend: {w}")
    s.assert_and_track(HighDemandDentist(p) == hd, f"patient_{i}, HighDemandDentist: {hd}")
    s.assert_and_track(SameDayBooking(p) == sd, f"patient_{i}, SameDayBooking: {sd}")
    s.assert_and_track(LongAppointment(p) == la, f"patient_{i}, LongAppointment: {la}")
    s.assert_and_track(BadHistory(p) == h, f"patient_{i}, BadHistory: {h}")
    s.assert_and_track(BankHoliday(p) == bh, f"patient_{i}, BankHoliday: {bh}")
    s.assert_and_track(Deposit(p)==d, f"patient_{i}, Deposit: {d}")
    print(f"{p}: Weekend={w}, HighDemand={hd}, SameDay={sd}, "
          f"LongAppt={la}, HighNoShow={h}, BankHoliday={bh}")
    print(f"Deposit paid: {d}")



# Deontological rule: do not keep deposit if they are not booked
p = Const('p', Person)
s.add(ForAll([p], Implies(Deposit(p), Booked(p))))
# rule 2, take deposit if they are booked on the weekend
s.add(ForAll([p], Implies(Weekend(p), Deposit(p))))
# rule 3, if they're booked on the weekend they must be booked
s.add(ForAll([p], Implies(Weekend(p), Booked(p))))

# additional rules - must have deposit for each predicate
s.add(ForAll([p], Implies(HighDemandDentist(p), Deposit(p))))
s.add(ForAll([p], Implies(SameDayBooking(p), Deposit(p))))
s.add(ForAll([p], Implies(LongAppointment(p), Deposit(p))))
s.add(ForAll([p], Implies(BadHistory(p), Deposit(p))))

# --- Goal: find a satisfying MODEL (not a refutation) ---
result = s.check()
if result == sat:
    m = s.model()
    print("Result: SAT — a valid assignment was found.")
    for p in patients:
        print(f"  Deposit({p}) = {m.evaluate(Deposit(p))}")
else:
    print(f"Result: {result} — no solution exists.")
    print(f"UNSAT Core: {s.unsat_core()}")