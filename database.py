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
#

#import datetime as dt
import sqlite3
import json
import logging

log = logging.getLogger(__name__)

class DataBase:
    def __init__(self, scheme, basefile='data.sqlite'):
        
        self.scheme = ''
        try:
            self.conn = sqlite3.connect(basefile, check_same_thread=False)
        except:
            log.debug('Could not connect to DataBase.')
            return None
        with open(scheme, 'r') as scheme_sql:
            sql = scheme_sql.read()
            self.scheme = sql
            if self.conn is not None:
                try:
                    cursor = self.conn.cursor()
                    cursor.executescript(sql)
                except:
                    log.debug('Could not create scheme.')
            else:
                log.debug("Error! cannot create the database connection.")
        mods = None
        with open('mods.json') as f:
            mods = json.load(f)
        for mod in mods:
            try:
                isinstance(mod['time'], str)
            except:
                mod['time'] = '1522011600'
             
        log.debug('DB created.')

    def execute(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        return cursor.fetchall()

    def close(self):
        self.conn.close()
