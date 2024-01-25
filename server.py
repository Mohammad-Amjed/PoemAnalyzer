from flask import Flask, render_template, request
from camel_tools.sentiment import SentimentAnalyzer
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.dialectid import DialectIdentifier


app = Flask(__name__, template_folder='.')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']

        # Sentiment Analysis
        sa = SentimentAnalyzer.pretrained()
        sentiments = sa.predict(text)
        print(sentiments)
        # POS Tagging
        mle = MLEDisambiguator.pretrained()
        sentence = simple_word_tokenize(text)
        disambig = mle.disambiguate(sentence)
        pos_tags = [d.analyses[0].analysis['pos'] for d in disambig]
        nounCount = pos_tags.count("noun")
        verbCount = pos_tags.count("verb")
        verbNounRatio = nounCount / verbCount if verbCount > 0 else "N/A"
        #dialect analysis
        did = DialectIdentifier.pretrained()
        predictions = did.predict(text, 'region')
        print([predictions[0].top])
        results = {
            "sentiments": sentiments,
            "nounCount": nounCount,
            "verbCount": verbCount,
            "verbNounRatio": verbNounRatio,
            "dialect": predictions[0].top
        }

        return render_template('index.html', results=results)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
