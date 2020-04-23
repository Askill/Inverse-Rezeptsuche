from application import app
import nltk
from search import defaultArr, stem


nltk.download('stopwords')
nltk.download('punkt')
delattr = stem(defaultArr)
app.run(host="0.0.0.0", port='5001', debug=True, threaded=True)


