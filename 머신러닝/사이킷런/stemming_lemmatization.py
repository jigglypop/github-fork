from nltk.stem import LancasterStemmer, WordNetLemmatizer
# import nltk
# nltk.download('wordnet')
stemmer = LancasterStemmer()
lemma = WordNetLemmatizer()
print(stemmer.stem('working'), stemmer.stem('works'), stemmer.stem('worked'))
print(lemma.lemmatize('amusing', 'v'))
print(lemma.lemmatize('happier', 'a'))
