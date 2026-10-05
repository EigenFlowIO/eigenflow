REGISTRIES={"metric":{},"filtration":{},"analysis":{},"operator":{},"reducer":{}}
def register(kind,name):
    if kind not in REGISTRIES: raise KeyError(kind)
    def deco(obj): REGISTRIES[kind][name]=obj; return obj
    return deco
