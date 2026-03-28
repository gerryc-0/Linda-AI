# Linda-AI
Our implementation of various functional and ethical goals of Linda-AI virtual dental receptionist.

## Setup
Only project dependency is z3-solver, Python v3.10+.

pip install -r requirements.txt
python deontology/deontology_ethical.py

Note: Scripts ending in -UNSAT were built to produce unsatisfiable results. They demonstrate what happens when constraints conflict — for example, maximising revenue without respecting patient priority or dentist working hours.

## Functional Goals
- Maximise Revenue/Bookings
    - [utilitarian/utilitarian_functional-UNSAT.py](utilitarian/utilitarian_functional-UNSAT.py)
- Reduce FTA rates
    - [deontology/deontology_functional.py](deontology/deontology_functional.py)
- Capturing and on-boarding new patients
    - Medical Card vs Practice Owner (deontology)
- Patient reactivation
    - avoid spam phonecalls: how recently did we call (deontology)
    - [deontology/deontology_functional_pt_reactivation.py](deontology/deontology_functional_pt_reactivation.py)
- Enforce practice policies
    - deposit policies (deontology)
    - [deontology/deontology_functional.py](deontology/deontology_functional.py)
- Triage and prioritise appointments
    - [utilitarian](utilitarian) and [prioritarian](prioritarian)
- Free up receiptionist time for clinical matters
    - follows from all the above

## Ethical Goals
- Increase access to healthcare while keeping access fair and equitable.
    - [deontology/deontology_ethical.py](deontology/deontology_ethical.py)
- Triage patients accurately.
    - [utilitarian/utilitarian_ethical.py](utilitarian/utilitarian_ethical.py)
    - [prioritarian/prioritarian_ethical.py](prioritarian/prioritarian_ethical.py)
- Don't over-treat patients or encourage overtreatment.
    - [deontology/over_treatment.py](deontology/over_treatment.py)
- Protect vulnerable patients.
    - [deontology/deontology_ethical.py](deontology/deontology_ethical.py)
- Adhere to the relevant data protection and dental profession best practices and laws.
    - [deontology/deontology_functional_pt_reactivation.py](deontology/deontology_functional_pt_reactivation.py)

## To-do
### Functional
- [x] Failure-to-attend workflow
    - covered by [deontology/deontology_functional.py](deontology/deontology_functional.py)
    - [x] short notice cancellation: add fee to their account
- [x] No spam phone calls
### Value Conflicts
- [x] Medical Card vs Practice Owner
    - Correct implementation of booking policies
- [x] Patient vs Receptionist
    - Expedient vs Accurate triage
- [x] Patient vs Practice Owner
    - Appropriate Care, no overtreatment
- [x] Dentist vs Practice Owner
    - Appointment length and workload