from Furnivall.Views import Genealogy as Genealogy
from Furnivall.Views import Sentiment as Sentiment

__all__=['Genealogy', 'Sentiment']
ViewClasses = {}
ViewClasses['Genealogy'] = Genealogy.classes_to_append
ViewClasses['Sentiment'] = Sentiment.classes_to_append

