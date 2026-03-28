# Linda-AI
Our implemtation of various functional and ethical goals of Linda-AI virtual dental receptionist.

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
- Triage patients accurately.
- Don't over-treat patients or encourage overtreatment.
- Protect vulnerable patients.
- Adhere to the relevant data protection and dental profession best practices and laws.

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