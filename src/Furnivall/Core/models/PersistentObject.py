class PersistentObject(Object):
    
    def toDBFormat(self):
        raise Exception("The method toDBFormat should be implemented on all persistent objects.")
