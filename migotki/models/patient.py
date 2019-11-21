import traceback

from .base import MatModel


def load():
    patients = []
    for n in range(2, 10):
        name = "p" + str(n)
        try:
            p = Patient(name)
            p.from_mat()
            patients.append(p)
        except Exception as e:
            print("\nCould not process {}\n".format(name))
            traceback.print_exc()
            raise e
    return patients


class Patient(MatModel):

    def __init__(self, name):
        self.name = name
        self.data = {
            'Age': None,
            'Gender': None,
            'Education': None,
            'Injury_level': None,
            'ASIA_score': None,
            'Time_after_injury': None,
            'Training_sessions': None,
            'Donning': None,
            'NASA_TLX': None,
            'SAndS': None,
            'BCIFES_Trials': None,
            'MMT_initial': None,
            'MMT_final': None,
            'PIADS': None,
            'ROM_initial': None,
            'ROM_final': None,
            'Threshold': None,
            'FES_parameters': None,
            'FES_times': None,
            'Perceived_usefulness': None
        }

    def __repr__(self):
        msg = "Person " + self.name + "{\n"
        for k, v in self.data.items():
            msg += "\t" + k + ": "
            if isinstance(v, list):
                for e in v:
                    msg += "\n\t\t" + str(e)
                msg += "\n"
            else:
                msg += str(v) + "\n"
        msg += "}\n"
        return msg

    def from_mat(self, path=None):
        if not path:
            path = "data/patients/{}.mat".format(self.name)
        super().from_mat(path)

    def _simplify(self, data: dict) -> dict:

        def process_nested(a, keys: list):
            l = []
            if not a.flatten()[0]:
                return l
            for i in a:
                nd = dict()
                for k in keys:
                    nd[k] = i[k][0][0, 0]
                l.append(nd)
            return l

        def process_muscle_data(data):
            l = []
            if not data.flatten()[0]:
                return l
            for e in data:
                muscle, L, R = e[0]
                muscle = muscle[0, 0][0]
                L = L.flatten()[0]
                L = L[0] if L.dtype else L
                R = R.flatten()[0]
                R = R[0] if R.dtype else L
                d = {'muscle': muscle, 'L': L, 'R': R}
                l.append(d)
            return l

        def process_roms(data):
            l = []
            if data[0, 0] is None:
                return l
            for d in data:
                trial, type, flex, ext = d[0]
                t = {'trial': trial.flatten()[0],
                     'type': type.flatten()[0],
                     'flexion': flex.flatten()[0],
                     'extension': ext.flatten()[0]}
                l.append(t)
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
            elif k == 'Injury_level':
                data[k] = v[0, 0][0, 0][0][0, 0][0]
            elif k == 'ASIA_score':
                data[k] = v[0, 0][0, 0][0][0, 0][0]
            elif k == 'Time_after_injury':
                data[k] = v[0, 0][0, 0][0][0, 0][0]
            elif k == 'Training_sessions':
                data[k] = int(v[0, 0][0, 0][0][0, 0][0])
            elif k == 'Donning':
                data[k] = process_nested(v[0, 0], ['session', 'all_green', 'final_thresh', 'final_FES', 'total'])
            elif k == 'NASA_TLX':
                data[k] = process_nested(v[0, 0], [
                    'session', 'mental_demand', 'physical_demand','temporal_demand', 'performance', 'effort',
                    'frustration', 'total'])
            elif k == 'SAndS':
                data[k] = process_nested(v[0, 0], ['session', 'stress', 'satisfaction'])
            elif k == 'BCIFES_Trials':
                data[k] = process_nested(v[0, 0], ['session', 'TP', 'FP', 'TN'])
            elif k == 'MMT_initial':
                data[k] = process_muscle_data(v[0, 0])
            elif k == 'MMT_final':
                data[k] = process_muscle_data(v[0, 0])
            elif k == 'PIADS':
                data[k] = process_nested(v[0, 0], [
                    'confident', 'secure', 'fit_with_routine', 'fit_in_environments', 'comfortable'])
            elif k == 'ROM_initial':
                data[k] = process_roms(v[0, 0])
            elif k == 'ROM_final':
                data[k] = process_roms(v[0, 0])
            elif k == 'Threshold':
                thresholds = process_nested(v[0, 0], ['session', 'threshold'])
                for d in thresholds:
                    for key in d.keys():
                        if key == 'session':
                            d[key] = d[key][0, 0]
                        else:
                            d[key] = d[key][0].tolist()
                data[k] = thresholds
            elif k == 'FES_parameters':
                feses = process_nested(v[0, 0], ['session', 'current', 'pulse_width', 'start_time', 'duration'])
                for d in feses:
                    for key in d.keys():
                        if key == 'session':
                            d[key] = d[key][0, 0]
                        else:
                            d[key] = d[key][0].tolist()
                data[k] = feses
            elif k == 'FES_times':
                feses = process_nested(v[0, 0], ['session', 'times_for_activation'])
                for d in feses:
                    for key in d.keys():
                        if key == 'session':
                            if d[key].size == 0:
                                d[key] = None
                            else:
                                d[key] = d[key][0, 0]
                        else:
                            if d[key].size == 0:
                                d[key] = []
                            else:
                                d[key] = d[key].flatten().tolist()
                data[k] = feses
            elif k == 'Perceived_usefulness':
                data[k] = v[0, 0][0, 0]
            else:
                raise Exception("Unexpected field: {}!".format(k))

        return data
