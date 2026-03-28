from z3 import *
import random

# financial policies of dental practice - deposits and cancellations

people = [f"person_{i}" for i in range(10)]
Person, patients = EnumSort('Person', people)

# flexible deposit policies - predicates
# deposit must be paid
Deposit = Function('Deposit', Person, BoolSort())
Booked = Function('Booked', Person, BoolSort())
Weekend = Function('Weekend', Person, BoolSort())
HighDemandDentist = Function('HighDemandDentist', Person, BoolSort())
SameDayBooking = Function('SameDayBooking', Person, BoolSort())
LongAppointment = Function('LongAppointment', Person, BoolSort())
BankHoliday = Function('BankHolidays', Person, BoolSort())
BadHistory =  Function('BadHistory', Person, BoolSort()) # has high no-show rate (apt type or patient history)

# cancellation fee policies - predicates
# fee waived if emergency or first offence
ShortNoticeCancellation = Function('ShortNoticeCancellation', Person, BoolSort())  # cancelled within 24hrs
MedicalEmergency = Function('MedicalEmergency', Person, BoolSort()) # medical emergency
FirstOffence = Function('FirstOffence', Person, BoolSort()) # first time cancellation at short notice
CancellationFee = Function('CancellationFee', Person, BoolSort()) # fee added to account


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
          f"LongAppt={la}, HighNoShow={h}, BankHoliday={bh}, Deposit={d}")

    # cancellation policy
    snc = random.choice([True, False])
    me = random.choice([True, False])
    fo = random.choice([True, False])
    cf = random.choice([True, False])
    s.assert_and_track(ShortNoticeCancellation(p) == snc, f"patient_{i}, ShortNoticeCancellation: {snc}")
    s.assert_and_track(MedicalEmergency(p) == me, f"patient_{i}, MedicalEmergency: {me}")
    s.assert_and_track(FirstOffence(p) == fo, f"patient_{i}, FirstOffence: {fo}")
    s.assert_and_track(CancellationFee(p) == cf, f"patient_{i}, CancellationFee: {cf}")
 
    print(f"{p}: Weekend={w}, HighDemand={hd}, SameDay={sd}, "
          f"LongAppt={la}, BadHistory={h}, BankHoliday={bh}, Deposit={d}")
    print(f"        ShortNoticeCancellation={snc}, MedicalEmergency={me}, "
          f"FirstOffence={fo}, CancellationFee={cf}")


# deontological rule: do not keep deposit if they are not booked
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

# short notice cancellation rules

# if short notice cancellation and NOT medical emergency and NOT first offence, charge fee
s.assert_and_track(ForAll([p], Implies(And(ShortNoticeCancellation(p), Not(MedicalEmergency(p)), Not(FirstOffence(p))), CancellationFee(p))),
    "Cancellation rule: charge fee for short notice cancellation"
)
 
# do not charge fee if medical emergency
s.assert_and_track(ForAll([p], Implies(MedicalEmergency(p), Not(CancellationFee(p)))),
    "Cancellation rule: waive fee for medical emergency"
)
 
# do not charge fee if first offence (warning only)
s.assert_and_track(ForAll([p], Implies(FirstOffence(p), Not(CancellationFee(p)))),
    "Cancellation rule: waive fee for first offence (warning issued)"
)
 
# do not charge fee if they did not cancel at short notice
s.assert_and_track(
    ForAll([p], Implies(Not(ShortNoticeCancellation(p)), Not(CancellationFee(p)))),
    "Cancellation rule: no fee if cancellation was not short notice"
)

# --- Goal: find a satisfying MODEL ---
result = s.check()
if result == sat:
    m = s.model()
    print("Result: SAT — a valid assignment was found.")
    print("\n--- Deposit Policy Results ---")
    for p in patients:
        print(f"  Deposit({p}) = {m.evaluate(Deposit(p))}")
    print("\n--- Cancellation Fee Results ---")
    for p in patients:
        print(f"  {p}: ShortNoticeCancellation={m.evaluate(ShortNoticeCancellation(p))}, "
              f"MedicalEmergency={m.evaluate(MedicalEmergency(p))}, "
              f"FirstOffence={m.evaluate(FirstOffence(p))}, "
              f"CancellationFee={m.evaluate(CancellationFee(p))}")
else:
    print(f"Result: {result} — no solution exists.")
    print(f"UNSAT Core: {s.unsat_core()}")