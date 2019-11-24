from scipy.io import loadmat


class MatModel:

    def __init__(self, name):
        self.name = name
        self.data = {}

    def __repr__(self):
        msg = self.name + " {\n"
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

    def get_training_sessions(self, prop):
        no_of_sessions = self.data['Training_sessions']
        sessions = self.data[prop]
        training_sessions = sessions[:no_of_sessions]
        return training_sessions

    def get_extensor(self, session):
        c1, c2 = tuple(c for c in session['current'])
        return c1 if c1 > c2 else c2

    def get_flexor(self, session):
        c1, c2 = tuple(c for c in session['current'])
        return c1 if c1 < c2 else c2

    def get_tpr(self, trial):
        tp = trial['TP']
        fp = trial['FP']
        tn = trial['TN']
        return tp/(tp+fp+tn)

    def get_fdr(self, trial):
        tp = trial['TP']
        fp = trial['FP']
        return fp/(fp+tp)

    def from_mat(self, path=None):
        if not path:
            path = "data/{}.mat".format(self.name)
        m = loadmat(path, struct_as_record=True)
        p = m[self.name]
        data = {}
        for f in self.data.keys():
            o = p[0, 0]
            v = o[0][f]
            data[f] = v
        data = self._simplify(data)
        for k, v in data.items():
            self.data[k] = v

    def _simplify(self, data) -> dict:
        pass
