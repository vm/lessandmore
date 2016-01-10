import re

from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import requests

from model import Transformer

app = Flask(__name__)
t = Transformer(threshold=0.4)

@app.route('/')
def enter_text():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def converted():
    less = request.form.get('less', 'drugs').split(' ')
    more = request.form.get('more', 'candy').split(' ')
    url = request.form.get('url', 'http://www.nytimes.com/2016/01/10/world/americas/el-chapo-mexican-drug-lord-interview-with-sean-penn.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=a-lede-package-region&region=top-news&WT.nav=top-news')

    soup = BeautifulSoup(requests.get(url).text)

    for script in soup(['script', 'style']):
        script.extract()
    text = soup.get_text()

    replacers = [
        convert(x.strip(), less, more)
        for x in re.split('Mr. |\.|\n|,', text)
        if x
    ]

    fixed = unicode(soup)
    for text, new_text in replacers:
        fixed = fixed.replace(text, new_text)
    return fixed


def convert(text, less, more):
    return text, t.transform(text, less, more)

if __name__ == '__main__':
    app.run(debug=True)
