from flask import Flask, request, render_template
import functions

import os

from dotenv import load_dotenv

load_dotenv()

#header = 'Faction name'

data, faction = functions.get_faction('8336')

#MQ: 8336
#NS: 9533


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])


def index():
    if request.method == 'POST':
        input_value = request.form['input_value']
        # process the input_value here

        print(input_value)
        data, faction = functions.get_faction(input_value)
        return render_template("index.html", data=data)#, faction=faction)
    data, faction = functions.get_faction('8336')
    #return render_template("index.html", data=data, faction=faction)

if "__name__" == "__main__":
    app.run(debug=True)


