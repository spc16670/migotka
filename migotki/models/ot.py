import traceback
from scipy.io import loadmat

from .base import MatModel


def load():
    ots = []
    for n in range(1, 5):
        name = "ot" + str(n)
        try:
            o = Ot(name)
            o.from_mat()
            ots.append(o)
        except Exception as e:
            print("\nCould not process {}\n".format(name))
            traceback.print_exc()
            raise e
    return ots


class Ot(MatModel):

    def __init__(self, name):
        self.name = name
        self.data = {
            'age': None,
            'gender': None,
            'years_as_ot': None,
            'years_with_fes': None,
            'NASA_TLX': None,
            'donning': None
        }

    def from_mat(self, path=None):
        if not path:
            path = "data/ot/{}.mat".format(self.name)
        m = loadmat(path, struct_as_record=True)
        p = m[self.name]
        data = {}
        for f in self.data.keys():
            o = p[0, 0]
            v = o[f]
            data[f] = v
        data = self._simplify(data)
        for k, v in data.items():
            self.data[k] = v

    def _simplify(self, data: dict) -> dict:

        def process_nested(a, keys: list):
            l = []
            session_count = a[keys[0]].size
            for s in range(session_count):
                nd = dict()
                for k in keys:
                    nd[k] = a[k][s][0]
                l.append(nd)
            return l

        for k, v in data.items():
            if k == 'age':
                data[k] = v[0, 0]
            elif k == 'gender':
                data[k] = v[0]
            elif k == 'years_as_ot':
                data[k] = v[0, 0]
            elif k == 'years_with_fes':
                data[k] = v[0, 0]
            elif k == 'NASA_TLX':
                data[k] = process_nested(v[0, 0], [
                    'session', 'mental_demand', 'physical_demand', 'temporal_demand', 'performance', 'effort',
                    'frustration', 'total'])
            elif k == 'donning':
                data[k] = process_nested(v[0, 0], ['session', 'minutes'])
            else:
                raise Exception("Unexpected field: {}!".format(k))
        return data
