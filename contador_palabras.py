

from nltk.corpus import stopwords
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
import string
from collections import Counter
from collections import OrderedDict




def keywords(miarchivo):
    #miarchivo = open('./prueba/archivoTXT.txt',"r")
    texto = miarchivo.read()

    stop_words = set(stopwords.words('spanish'))
    prepositions =['a','ante','bajo','cabe','con','contra','de','desde','en','entre','hacia','hasta','para','por','según','sin','so','sobre','tras']
    prep_alike = ['durante','mediante','excepto','salvo','incluso','más','menos']
    adverbs = ['no','si','sí']
    articles = ['el','la','los','las','un','una','unos','unas','este','esta','estos','estas','aquel','aquella','aquellos','aquellas']
    aux_verbs = ['he','has','ha','hemos','habéis','han','había','habías','habíamos','habíais','habían']
    comillas =['?','--','-','1','2''3','4','5','6','7','8','9','0']
    stop_words_2=prepositions+prep_alike+adverbs+articles+aux_verbs+comillas

    word_tokens = word_tokenize(texto)

    word_tokens = list(filter(lambda token: token not in string.punctuation,word_tokens))

    word_tokens = list(filter(lambda token: token.lower() ,word_tokens))


    filtro = []
    num = []
    for palabra in word_tokens:
        if palabra not in stop_words:
            if palabra not in stop_words_2:
                try:
                    num.append(float(palabra))
                except ValueError:
                    filtro.append(palabra)



    c = Counter(filtro)


    y = OrderedDict(c.most_common(50))
    #with open('')
    return (y)
