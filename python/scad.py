class ScadFragment(object):
    def __init__(self, *args, **kw):
        self.args = args
        self.kw = kw

    def scad(self):
        args = [self.args]
        if self.kw:
            kw = str.join(", ", ["%s=%s" % (key, val) for (key, val) in self.kw.items()])
            args.append(kw)
        args = str.join(", ", args)
        scad = "%s(%s);\n" % (self.__class__.__name__, args)
        return scad

class module(ScadFragment): 
    def scad(self):
        args = ''
        if len(self.args) == 2:
            args = ''
            body = self.args[1]
        if len(self.args) == 3:
            args = self.args[1]
            body = self.args[2]
        else:
            assert "wat?"
        scad = "module %s(%s) { %s }\n" % (self.__class__.name, args, body)


class polyhedron(ScadFragment):
    pass

class translate(ScadFragment):
    pass

class rotate(ScadFragment):
    pass

class union(ScadFragment):
    pass

class difference(ScadFragment):
    pass

class liner_extrude(ScadFragment):
    pass

class circle(ScadFragment):
    pass

class cube(ScadFragment):
    pass



