from application import app
from application.search import defaultArr, stem
import nltk

nltk.download('stopwords')
nltk.download('punkt')
defaultArr = stem(defaultArr)
app.run(host="0.0.0.0", port='5001', debug=False, threaded=True)


