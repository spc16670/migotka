
from migotki.models.patient import load as patient_load
from migotki.models.carer import load as carer_load
from migotki.models.ot import load as ot_load


PATIENTS = patient_load()
CARERS = carer_load()
OTS = ot_load()


def print_patients():
    for p in PATIENTS:
        print(p)


def print_patients_with_fes_sm_1s():
    print("Patients with < 1s times for activation:")
    for p in PATIENTS:
        fes = p.data['FES_times']
        for s in fes:
            tfa = s['times_for_activation']
            for t in tfa:
                if t < 1:
                    print(p.name, s['session'], t)


def print_carers():
    for c in CARERS:
        print(c)


def print_ots():
    for p in OTS:
        print(p)
