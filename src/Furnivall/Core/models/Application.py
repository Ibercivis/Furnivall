class Application(PersistentObject):
    def toDBFormat(self):
        return {
            name: self.name,
            description: self.description,
            icon: self.icon
            }

