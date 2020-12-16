import re

text = 'name=yeomdonghwan, gender=male, major=ml'
text1 = re.sub('[a-z]+=', '', text)
print(re.split(', ', text1))
