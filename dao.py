
from ania.models.patient import load as patient_load
from ania.models.carer import load as carer_load


PATIENTS = patient_load()
CARERS = carer_load()


def print_patients():
    for p in PATIENTS:
        print(p)


def print_carers():
    for c in CARERS:
        print(c)
