from application import app
import nltk

nltk.download('stopwords')
nltk.download('punkt')

app.run(host="0.0.0.0", port='5001', debug=True, threaded=True)


