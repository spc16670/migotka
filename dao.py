
from migotki.models.patient import load as patient_load
from migotki.models.carer import load as carer_load
from migotki.models.ot import load as ot_load


PATIENTS = patient_load()
CARERS = carer_load()
OTS = ot_load()


def print_patients():
    for p in PATIENTS:
        print(p)


def print_carers():
    for c in CARERS:
        print(c)


def print_ots():
    for p in OTS:
        print(p)
