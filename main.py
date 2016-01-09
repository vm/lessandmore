from flask import Flask, request, render_template
from readability import ParserClient

from convert import convert

app = Flask(__name__)

TOKEN = ''
parser = ParserClient(TOKEN)

@app.route('/')
def enter_text():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def post_text():
    link = request.form['article']
    less_words = request.form['less'].split(' ')
    more_words = request.form['more'].split(' ')
    response = parser.get_article(link).json()
    converted_content = convert(response['content'], less_words, more_words)
    return render_template(
        'converted.html',
        title=response['title'],
        author=response['author'],
        content=converted_content)


if __name__ == '__main__':
    app.run(debug=True)
