from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def enter_text():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def post_text():
    text = request.form['text']
    less = request.form['less'].split(' ')
    more = request.form['more'].split(' ')
    return text


if __name__ == '__main__':
    app.run(debug=True)
