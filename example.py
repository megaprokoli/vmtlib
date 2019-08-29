from vmtlib.vmt_file import VmtFile


vmt = VmtFile()

# vmt.read()


d = {"shader": {"$basetexture": "brick", "Proxies": {"key": "val"}}}

vmt.from_dict(d)

vmt.shader.set("$basetexture", "new")

vmt.write("target.vmt")
