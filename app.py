from flask import Flask, flash, redirect, render_template, request, session, abort
import pandas as pd
from nltk.collocations import *
import nltk, string

app = Flask(__name__)
 
@app.route('/', methods=['GET','POST'])
def choice():

    # open file
    df = pd.read_csv("input.csv")

    # dropdown
    count = df["datum_fixed"].value_counts()
    tuples = [tuple((x, y)) for x, y in count.items()]

    # show results
    if request.method == 'POST':
        select = request.form.get('option')
        # tuple -> string -> dirty solution
        s = select[2:12]
    
        # filter out dates
        f = df[df["datum_fixed"] == s]

        #define stop words
        stop = nltk.corpus.stopwords.words('dutch') + [s for s in string.punctuation] +["'","`"]

        #tokenize and clean
        l = f.tekst.apply(nltk.word_tokenize,language='dutch')
        l = [s.lower() for h in l for s in h if s.lower() not in stop]

        #find trigrams
        finder = TrigramCollocationFinder.from_words(l, window_size = 3)
        pairs = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))

        def prettify(uglyness):
            for s in uglyness:
                try:
                    n = ' '.join(s)
                except: 
                    m = s

            return[n,m]

        q = [prettify(p) for p in pairs]

    return render_template(
        'body.html',**locals())


if __name__ == "__main__":
    app.run()
