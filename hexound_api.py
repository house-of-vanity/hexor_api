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
"""API for hexound v2
.. moduleauthor:: AB <github.com/house-of-vanity>
"""

import json
import logging
import os
from flask import Response, render_template, request, Flask, send_file, jsonify
from flask_cors import CORS
from api.database import DataBase
from api.tools.passwd import hash_password, verify_password
from api.tools.response import wrap
from sqlite3 import IntegrityError

HOME_DIR = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, static_folder=os.path.realpath("{}/mods".format(HOME_DIR)))

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
    """
          **Perform action with users**
          - Create user with hashed password.
          - ...

          :param action: Requested action
          :type action: string
          :returns: json

          - Example::

              $ curl --data "name=khui&pass=pizda" http://localhost:5000/usr/create

          - Expected Success Response::

              {
                "date": "Fri May 31 21:05:30 2019",
                "exception": null,
                "message": "User khui created.",
                "traceback": null,
                "type": "Info"
              }

          - Fail Response - user exists::

              {
                "date": "Fri May 31 21:08:42 2019",
                "exception": "IntegrityError",
                "message": "Username isn't available.",
                "traceback": [
                  "  File \"hexound_api.py\", line 69, in usr_reg    db.user(action=action, name=name, pass_hash=pass_hash)",
                  "  File \"/root/repos/hexound_api/database.py\", line 78, in user    self.execute(sql)",
                  "  File \"/root/repos/hexound_api/database.py\", line 68, in execute    cursor.execute(sql)"
                ],
                "type": "Error"
              }

          - Fail Response - protocol violation::

              {
                "date": "Fri May 31 21:22:04 2019",
                "exception": "BadRequestKeyError",
                "message": "Lack of parameters.",
                "traceback": [
                  "  File \"hexound_api.py\", line 67, in usr_reg    pass_ = data['pass']",
                  "  File \"/usr/local/lib/python3.6/dist-packages/werkzeug/datastructures.py\", line 442, in __getitem__    raise exceptions.BadRequestKeyError(key)"
                ],
                "type": "Error"
              }

    """
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
    db = DataBase(scheme=os.path.realpath("{}/data.sql".format(HOME_DIR)))
    CORS(app)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log = logging.getLogger('fiend_sucker')
    app.run(host='0.0.0.0')
