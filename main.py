import re

from flask import Flask, request, render_template
from readability import ParserClient

app = Flask(__name__)

TOKEN = 'ee71317c7d5f30a39e53a83dd84a7646977e01c4'
parser = ParserClient(token=TOKEN)

@app.route('/')
def converted():
    less = request.args.get('less', '').split(' ')
    more = request.args.get('more', '').split(' ')
    url = request.args.get('url', 'http://espn.go.com/chalk/story/_/id/14521633/daily-fantasy-mark-cuban-invests-dfs-analytics-company-fantasy-labs')
    response = parser.get_article(url).json()
    converted_content = re.sub('<[^<]+?>', '', response['content'])
    return render_template(
        'converted.html',
        title=response['title'],
        author=response['author'],
        content=converted_content)


if __name__ == '__main__':
    app.run(debug=True)
