from Core import *
import sys, Core, types
import pprint

modules=Core.__all__

for i in modules:
    print "Analizing module %s from package %s" %(i,"Core")
    module=getattr(Core, i) # Core.Assignent
    classes=sorted([ a for a in dir(module) if isinstance(getattr(module, a, None), types.ClassType)]) # Get classes... # FIXME This seems to fail...
    classes=[ (a, getattr(module,a).__base__) for a in dir(module) if type(getattr(module, a)) is types.TypeType]
    print "Classes for module %s are:" %(module)
    pprint.pprint(classes)
