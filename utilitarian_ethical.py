import z3
import random

# set number of patients and hours
# simple 1 hour per appoitment in this model, may extend if we have time
num_patients = 20
num_hours = 9  # Available appointment slots

# store data as in grid problem
patients_data = []

# Generate synthetic patient data
random.seed(42)
for i in range(num_patients):
    pain = random.randint(0, 10)
    # Infection and pain levels are correlated
    if pain > 5:
        infection = random.randint(5, 10)
    else:
        infection = random.randint(0, 5)
    patients_data.append({'id': i, 'pain': pain, 'infection': infection, 'priority': pain + infection})

# optimiser

optimizer = z3.Optimize()

# var for each patient each hour to decide if they are scheduled or not
# use ints for mult below
appointment_slots = [
    [z3.Int(f"patient_{i}_hour_{j}") for j in range(num_hours)]
    for i in range(num_patients)
]

# constrain to 0 or 1 as in grid problem
for i in range(num_patients):
    for j in range(num_hours):
        v = appointment_slots[i][j]
        optimizer.assert_and_track(
            z3.Or(v == 0, v == 1),
            f"Add paitient {i} hour {j} to optimiser"
        )

# Each hour can be assigned to at most one patient
for j in range(num_hours):
    optimizer.assert_and_track(
        z3.Sum([appointment_slots[i][j] for i in range(num_patients)]) <= 1,
        f"One pantient per hour {j}"
    )

# Each patient can receive at most one appointment
for i in range(num_patients):
    optimizer.assert_and_track(
        z3.Sum([appointment_slots[i][j] for j in range(num_hours)]) <= 1,
        f"Only see patient {i} at most once"
    )

# score is sum product of priorities and schedule
utilitarian_score = z3.Sum([
    appointment_slots[i][j] * patients_data[i]['priority']
    for i in range(num_patients)
    for j in range(num_hours)
])

# maximise score
optimizer.maximize(utilitarian_score)

result = optimizer.check()

if result == z3.sat:
    model = optimizer.model()

    scheduled = []
    unscheduled = []

    for i in range(num_patients):
        is_scheduled = any(model[appointment_slots[i][j]] == 1 for j in range(num_hours))
        if is_scheduled:
            scheduled.append(patients_data[i])
        else:
            unscheduled.append(patients_data[i])

    print("\n===Results===")
    print(f"Patients Scheduled: {len(scheduled)}/{num_patients}")
    print(f"Patients Deferred:  {len(unscheduled)}/{num_patients}")

    scheduled_welfare = sum(p['priority'] for p in scheduled)
    deferred_welfare  = sum(p['priority'] for p in unscheduled)

    print(f"\nTotal Welfare Score (Scheduled): {scheduled_welfare}")
    print(f"Total Welfare Score (Deferred):  {deferred_welfare}")

    print("\n===schedule per hour===")
    for j in range(num_hours):
        for i in range(num_patients):
            if model[appointment_slots[i][j]] == 1:
                print(f"Hour {j}: Patient {i}")
                print(f"\tPain: {patients_data[i]['pain']}, Infection: {patients_data[i]['infection']}, Priority: {patients_data[i]['priority']}")
                

        

    print("\n---unscheduled patients---")
    for p in sorted(unscheduled, key=lambda x: -x['priority']):
        print(f"  Patient {p['id']:2d}: pain={p['pain']}, infection={p['infection']}, priority={p['priority']}")

else:
    print("UNSAT")
    print("Core:", optimizer.unsat_core())
