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
