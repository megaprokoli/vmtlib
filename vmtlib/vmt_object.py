import re


class VmtObject:
    def __init__(self, name, span=None, string=None, dict=None, layer=0):
        self._layer = layer  # for output formatting

        self.name = name
        self.attributes = {}
        self.childs = {}

        if string is not None and span is not None:  # if from dict and not string
            self.string = string[span[0]:span[1]]
            self.work_str = ""
            self.span = span

            self.__add_childs()
            self.__fetchlines()
        elif dict is not None:
            self.__from_dict(dict)

    @property
    def layer_char(self):
        return "\t" * self._layer

    @property
    def dict(self):
        d = {}

        for k in self.attributes.keys():
            d.update({k: self.attributes[k]})

        for k in self.childs.keys():
            d.update({k: self.childs[k].dict})

        return d

    @classmethod
    def __cleanup_name(cls, name):
        name = "".join(list(filter(lambda c: ord(c) >= 32, name)))  # remove control chars
        name = name.replace("\"", "")  # remove "
        name = name.replace("{", "")
        name = name.split("//")[0]  # remove comments
        name = name.replace(" ", "")  # remove spaces
        return name

    @classmethod
    def detect_objects(cls, content):
        name_match = re.search("(^^|\n*|\t*).*(\n*|\t*|\n\t*)\{", content)  # (^^|\n*|\t*).*(\n*|\t*|\n\t*)\{

        if name_match is not None:
            name = content[name_match.span()[0]:name_match.span()[1]]
            op_matches = re.finditer("\{", content)
            cl_matches = re.finditer("\}", content)

            obj = {"name": cls.__cleanup_name(name),
                   "span": [list(op_matches)[0].span()[1], list(cl_matches)[-1].span()[0]]}
            return obj
        return None

    def get(self, attr):
        val = self.attributes.get(attr)

        if val is None:
            val = self.childs.get(attr)
        return val

    def set(self, attr, val):
        if isinstance(val, VmtObject):
            self.childs[attr] = val
        else:
            self.attributes[attr] = val

    def stringify(self):
        print(self.name + " - " + str(self._layer))
        string = ""

        string += self.layer_char + self.name + "\n" + self.layer_char + "{\n"

        for k in self.attributes.keys():
            string += "{}{} {}\n".format(self.layer_char, k, self.attributes[k])

        for v in self.childs.values():
            string += v.stringify()

        string += self.layer_char + "}\n"
        return string

    def __from_dict(self, d):
        keys = d.keys()

        for k in list(keys):
            v = d[k]

            if isinstance(v, dict):
                self.childs.update({k: VmtObject(name=k, dict=v, layer=self._layer + 1)})
            else:
                self.attributes.update({k: v})

    def __add_childs(self):
        work_str = self.string

        obj_pos = self.detect_objects(work_str)

        while obj_pos is not None:

            self.childs.update({obj_pos["name"]: VmtObject(name=obj_pos["name"],
                                                           span=obj_pos["span"],
                                                           string=self.string,
                                                           layer=self._layer + 1)})
            span = obj_pos["span"]
            work_str = work_str.replace("".join(work_str[span[0]-1:span[1]+1]), "")     # extracted child + { and }

            obj_pos = self.detect_objects(work_str)

        self.work_str = work_str

    def __parse_attributes(self, string):
        key = None
        val = None

        arg_match = re.search(r"([^\t]\w+)(\t+| +)(.+)", string)
        if arg_match is not None:
            g = arg_match.groups()
            key = g[0]
            val = g[2]

        return key, val

    def __fetchlines(self):
        tmp = ""

        for char in self.work_str:

            if char == "\n":
                if tmp != "":
                    k, v = self.__parse_attributes(tmp)

                    if k is not None:
                        self.attributes.update({k: v})
                    tmp = ""
            else:
                tmp += char


