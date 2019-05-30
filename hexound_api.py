#
# Copyright (c) 2019, UltraDesu <ultradesu@hexor.ru>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#     names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY UltraDesu <ultradesu@hexor.ru> ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL UltraDesu <ultradesu@hexor.ru> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from flask import Response, render_template, request, Flask, send_file, jsonify
import json
import logging
from flask_cors import CORS
from database import DataBase
from tools.passwd import hash_password, verify_password
from tools.response import wrap
from sqlite3 import IntegrityError

app = Flask(__name__, static_folder='mods')
db = DataBase(scheme='data.sql')

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

@app.route("/usr/<action>", methods = ['POST', 'GET'])
def usr_reg(action):
    if request.method == 'POST':
        data = request.form
        if action == 'create':
            try:
                name = data['name']
                pass_ = data['pass']
                pass_hash = hash_password(pass_)
                db.user(action=action, name=name, pass_hash=pass_hash)
            except IntegrityError as e:
                return jsonify(wrap(message="Username isn't available.", exception=e))
            except KeyError as e:
                return jsonify(wrap(message="Lack of parameters.", exception=e))
            return jsonify(wrap(message="User %s created." % name, type_='Info'))
    else:
        return jsonify(wrap(message="Only POST method is available."))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
