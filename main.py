from flask import Flask, request
import json
import logging
from __future__ import unicode_literals

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, filename='test.log')


@app.route('/', methods=['Post'])
def main():
    logging.info(request.data)

    # Create session
    session = request.json['session']
    del session['new']
    del session['skill_id']
    #Create qwestion
    qw = request.json['request']["original_utterance"]
    #Create answ
    asnw = {
        'response':{
            'text':'Вы спросили - {}'.format(qw),
            'end_session': False,
            },
        'session':session,
        'version': 1.0
        }
    if request.json['request']["command"].lower() == 'хватит':
        asnw['response']['end_session'] = True
    return json.dumps(asnw)



if __name__ == '__main__':
    app.run()
