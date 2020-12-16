import nltk
from pprint import pprint
nltk.download('punkt')
text_sample = 'The Matrix is everywhere its all around us, here even in this room. You can see it out your window or on your television. you feel it when you go to work, or go to church or pay your taxes.'

# 문장 토크나이저 sent_tokenize
sentences = nltk.sent_tokenize(text=text_sample)
print(type(sentences), len(sentences))
print(sentences)
# 단어 토크나이저 word_tokenize
sentences2 = 'The Matrix is everywhere its all around us, here even in this room.'
words = nltk.word_tokenize(sentences2)
print(type(words), len(words))
print(words)


def tokenize_text(sentences):
    return [nltk.word_tokenize(i) for i in nltk.sent_tokenize(sentences)]


pprint(tokenize_text(text_sample))
