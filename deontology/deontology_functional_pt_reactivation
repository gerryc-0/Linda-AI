from z3 import *
import random

# Deontology functional goal: Patient Reactivation
# Linda AI must not spam call patients when carrying out patient reactivations

# When a patient books with the practice, they consent to being
# contacted by Linda AI. This consent remains valid until:
# (a) the patient explicitly retracts their consent or
# (b) GDPR patient data retention requirements expire (e.g. 7 years after last contact)

# deontology rules:
# 1. Do not contact a patient if they were contacted in the last 6 months
# 2. Do not cold call a patient unless they have valid consent (not retracted, not expired)
# 3. Must reactivate at least one patient (functional requirement)

people = [f"person_{i}" for i in range(10)]
Person, patients = EnumSort('Person', people)

# predicates
ContactedRecently = Function('ContactedRecently', Person, BoolSort()) # contacted in last 6 months
ConsentRetracted = Function('ConsentRetracted', Person, BoolSort()) # patient has retracted consent
GDPRinvalid = Function('GDPRinvalid', Person, BoolSort()) # data retention period exceeded
Reactivate = Function('Reactivate', Person, BoolSort()) # decision variable

s = Solver()

random.seed(42)
for i, p in enumerate(patients):
    recently = random.choice([True, False])
    retracted = random.choice([True, False])
    expired = random.choice([True, False])
    s.assert_and_track(ContactedRecently(p) == recently, f"patient_{i}, ContactedRecently: {recently}")
    s.assert_and_track(ConsentRetracted(p) == retracted, f"patient_{i}, ConsentRetracted: {retracted}")
    s.assert_and_track(GDPRinvalid(p) == expired, f"patient_{i}, GDPRinvalid: {expired}")
    print(f"{p}: ContactedRecently={recently}, ConsentRetracted={retracted}, "
          f"GDPRinvalid={expired}")

# deontology rule 1: do not reactivate if contacted in the last 6 months
p = Const('p', Person)
s.assert_and_track(
    ForAll([p], Implies(ContactedRecently(p), Not(Reactivate(p)))),
    "Rule: do not reactivate if contacted in the last 6 months"
)

# deontology rule 2: do not reactivate if patient has retracted consent
s.assert_and_track(
    ForAll([p], Implies(ConsentRetracted(p), Not(Reactivate(p)))),
    "Rule: do not reactivate if patient has retracted consent"
)

# deontology rule 3: do not reactivate if GDPR data retention has expired
s.assert_and_track(
    ForAll([p], Implies(GDPRinvalid(p), Not(Reactivate(p)))),
    "Rule: do not reactivate if GDPR data retention has expired"
)

# functional goal: reactivate at least one patient
s.assert_and_track(
    Or([Reactivate(p) for p in patients]),
    "Rule: must reactivate at least one patient"
)

# --- Goal: find a satisfying MODEL ---
result = s.check()
if result == sat:
    m = s.model()
    print("\nResult: SAT — a valid assignment was found.")
    for person in patients:
        print(f"  Reactivate({person}) = {m.evaluate(Reactivate(person))}, "
              f"ContactedRecently={m.evaluate(ContactedRecently(person))}, "
              f"ConsentRetracted={m.evaluate(ConsentRetracted(person))}, "
              f"GDPRinvalid={m.evaluate(GDPRinvalid(person))}")
else:
    print(f"\nResult: {result} — no patient can be reactivated under these rules.")
    print(f"UNSAT Core: {s.unsat_core()}")