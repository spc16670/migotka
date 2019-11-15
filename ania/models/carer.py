import traceback

from .base import MatModel


def load():
    carers = []
    for n in range(2, 10):
        name = "c" + str(n)
        try:
            p = Carer(name)
            p.from_mat()
            carers.append(p)
        except Exception as e:
            print("\nCould not process {}\n".format(name))
            traceback.print_exc()
            raise e
    return carers


class Carer(MatModel):

    def __init__(self, name):
        self.name = name
        self.data = {
            'Age': None,
            'Gender': None,
            'Education': None,
            'Distance_travelled': None,
            'NASA_TLX': None,
            'SAndS': None,
            'PIADS': None,
            'Training_sessions': None
        }

    def from_mat(self, path=None):
        if not path:
            path = "data/carers/{}.mat".format(self.name)
        super().from_mat(path)

    def _simplify(self, data: dict) -> dict:

        def process_nested(a, keys: list):
            l = []
            if not a[0, 0]:
                return l
            for i in a:
                nd = dict()
                for k in keys:
                    nd[k] = i[k][0][0, 0]
                l.append(nd)
            return l

        for k, v in data.items():
            if k == 'Age':
                data[k] = v[0, 0][0, 0]
                if data[k]:
                    data[k] = data[k][0][0][0][0, 0]
            elif k == 'Gender':
                data[k] = v[0, 0][0, 0]
                if data[k]:
                    data[k] = data[k][0][0][0][0]
            elif k == 'Education':
                data[k] = v[0, 0][0, 0]
                if data[k]:
                    data[k] = data[k][0][0][0][0]
            elif k == 'Distance_travelled':
                data[k] = v[0, 0][0, 0]
                if data[k]:
                    data[k] = data[k][0][0][0][0, 0]
            elif k == 'Training_sessions':
                data[k] = int(v[0, 0][0, 0][0][0, 0][0])
            elif k == 'NASA_TLX':
                data[k] = process_nested(v[0, 0], [
                    'session', 'mental_demand', 'physical_demand', 'temporal_demand', 'performance', 'effort',
                    'frustration', 'total'])
            elif k == 'SAndS':
                data[k] = process_nested(v[0, 0], ['session', 'stress', 'satisfaction'])
            elif k == 'PIADS':
                data[k] = process_nested(v[0, 0], [
                    'confident', 'secure', 'fit_with_routine', 'fit_in_environments', 'comfortable'])
            elif k == 'Training_sessions':
                data[k] = v[0, 0][0, 0][0][0, 0][0]
            else:
                raise Exception("Unexpected field: {}!".format(k))
        return data
