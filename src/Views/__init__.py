import sample, Genealogy

__all__=['sample', 'Genealogy']
ViewClasses = {}

ViewClasses['sample'] = sample.classes_to_append
ViewClasses['Genealogy'] = Genealogy.classes_to_append

