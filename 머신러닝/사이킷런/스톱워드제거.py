from nltk import word_tokenize, sent_tokenize, corpus
# nltk.download('stopwords')
stopword = corpus.stopwords.words('english')
print(len(stopword))
print(*stopword)


text_sample = 'The Matrix is everywhere its all around us, here even in this room. You can see it out your window or on your television. you feel it when you go to work, or go to church or pay your taxes.'


def tokenize_text(sentences):
    return [word_tokenize(i) for i in sent_tokenize(sentences)]


all_tokens = []
word_tokens = tokenize_text(text_sample)
for sentence in word_tokens:
    temp = []
    for word in sentence:
        word = word.lower()
        if word not in stopword:
            temp.append(word)
    all_tokens.append(temp)
print(all_tokens)
