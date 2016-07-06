import logging

from flask import Flask
from flask.templating import render_template

import config
from views import TeamsAPIView, PartialsAPIView


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s]: %(levelname)s : %(message)s'
)


# Settings -----------------------------------------------------------------------------------------

# Flask
app = Flask(__name__)
app.config.from_object(config)


# App ----------------------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

teams_view = TeamsAPIView.as_view('times')
partials_view = PartialsAPIView.as_view('parciais')

app.add_url_rule('/times/', defaults={'slug': None}, view_func=teams_view, methods=['GET'])
app.add_url_rule('/times/<string:slug>/', view_func=teams_view, methods=['GET'])
app.add_url_rule('/times/<string:slug>/parciais/', view_func=partials_view, methods=['GET'])


#===================================================================================================
# __main__
#===================================================================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0')
