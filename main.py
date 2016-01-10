import re

from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def enter_text():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def converted():
    less = request.form.get('less', '').split(' ')
    more = request.form.get('more', '').split(' ')
    url = request.form.get('url', 'http://www.nytimes.com/2016/01/10/world/americas/el-chapo-mexican-drug-lord-interview-with-sean-penn.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=a-lede-package-region&region=top-news&WT.nav=top-news')

    soup = BeautifulSoup(requests.get(url).text)

    for script in soup(['script', 'style']):
        script.extract()
    text = soup.get_text()

    replacers = [convert(x.strip()) for x in re.split('Mr. |\.|\n|,', text) if x]
    print replacers[:100]

    fixed = unicode(soup)
    for text, new_text in replacers:
        fixed = fixed.replace(text, new_text)
    return fixed


def convert(text):
    return text, text.upper()

if __name__ == '__main__':
    app.run(debug=True)
