import Furnivall.Core.Views.Sample as sample
import Furnivall.Core.Views.Genealogy as Genealogy

__all__=['sample', 'Genealogy']
ViewClasses = {}

ViewClasses['sample'] = sample.classes_to_append
ViewClasses['Genealogy'] = Genealogy.classes_to_append

