import numpy as np
import pandas as pd

import re

from pymystem3 import Mystem

import nltk
from nltk.corpus import stopwords

from tensorflow.keras.preprocessing.sequence import pad_sequences

def remove_special_characters(text):
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text

def predict(model, tokenizer, text, max_news_len):
    _df = pd.DataFrame({'post_text': [text]})
    
    _df['post_text'] = _df['post_text'].apply(lambda x: x.lower())
    _df['post_text'] = _df['post_text'].apply(remove_special_characters)
    _df['tokens'] = _df['post_text'].apply(nltk.word_tokenize)
    
    _stop_words = set(stopwords.words('russian'))
    
    _df['tokens'] = _df['tokens'].apply(lambda x: [word for word in x if word not in _stop_words])

    _m = Mystem()
    _df['tokens'] = _df['tokens'].apply(lambda x: [_m.lemmatize(word)[0] for word in x])
    _df['processed_text'] = _df['tokens'].apply(lambda x: ' '.join(x))
    _df.replace("", pd.NA, inplace=True)
    _df.dropna(inplace=True)
    
    _sequences = tokenizer.texts_to_sequences(_df['processed_text'])
    
    x_predict = pad_sequences(_sequences, maxlen=max_news_len)
    
    return model.predict(x_predict)
        
def predict_class(model, tokenizer, text, y_train, max_news_len):
    try:
        class_labels = y_train.keys()
        predictions = predict(model, tokenizer, text, max_news_len)
        
        predicted_class_index = np.argmax(predictions)
        predicted_class = class_labels[predicted_class_index]
    except:
        predicted_class = 'Не удалось создать прогноз!'
    
    return predicted_class
    