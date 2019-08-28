from vmtlib.vmt_file import VmtFile


vmt = VmtFile("example.vmt")
print(vmt.filename)
vmt.read()
vmt.shader.set("$basetexture", "new")
vmt.write("target.vmt")
