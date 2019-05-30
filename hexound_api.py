'''
Documentation, License etc.

@package hexound_api
'''
from flask import Response, render_template, request, Flask, send_file, jsonify
import json
import logging
from flask_cors import CORS
from database import DataBase

app = Flask(__name__, static_folder='mods')
db = DataBase(scheme='data.sqlite')

CORS(app)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('fiend_sucker')

@app.route("/mods")
def mods():
    mods = None
    limit = request.args.get('limit', default = 20, type = int)
    offset = request.args.get('offset', default = 0, type = int)
    with open('mods.json') as f:
        mods = json.load(f)
    for mod in mods:
        try:
            isinstance(mod['time'], str)
        except:
            mod['time'] = '1522011600'
    return jsonify(mods[offset:offset+limit])

@app.route("/usr", methods = ['POST'])
def usr_reg():
    if request.method == 'POST':
        data = request.form
        try:
            login = data['login']
            password = data['password']
        except:
            return 'GTFO'
        log.debug('Going to register with {}:{}'.format(login, password))
    else:
        return 'GTFO'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
