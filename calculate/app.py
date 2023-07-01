import os
from flask import Flask, render_template

import calculate


app = Flask(__name__)


@app.route('/')
def index():
    output_dict = calculate.get_data_dict()
    return render_template('index.html', data=output_dict)


if __name__ == '__main__':
    app.run(debug=True)
