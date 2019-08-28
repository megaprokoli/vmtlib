import os

from vmtlib.vmt_object import VmtObject


class VmtFile:
    def __init__(self, path):
        self._content = ""

        self.path = path
        self.shader = None

    def __str__(self):
        return self.shader.stringify()

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def directory(self):
        return os.path.dirname(os.path.abspath(self.path))

    @property
    def dict(self):
        return {self.shader.name: self.shader.dict}

    def read(self):
        with open(self.path, "r") as file:
            self._content = file.read()

            shader_obj = VmtObject.detect_objects(self._content)
            self.shader = VmtObject(shader_obj["name"], shader_obj["span"], self._content)

    def write(self, target):
        if not os.path.exists(os.path.dirname(os.path.abspath(target))):
            raise FileNotFoundError

        with open(target, "w") as file:
            file.write(str(self))

