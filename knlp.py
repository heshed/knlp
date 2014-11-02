#!/usr/bin/env python
#-*- coding:utf-8 -*-
import urlparse
import json
import konlpy
from twisted.python import log

__author__ = 'binaa1'

class KKMA:
    def __init__(self):
        self.kkma = konlpy.tag.Kkma()

    def query(self, q):
        return {
            'morphs': self.kkma.morphs(q),
            'nouns': self.kkma.nouns(q),
            'sentences': self.kkma.sentences(q),
            'pos': self.kkma.pos(q),
        }

def process(kkma, environ):
    if environ['REQUEST_METHOD'] == 'GET':
        params = urlparse.parse_qs(environ['QUERY_STRING'])
        q = params.get('q', '')[0]
        log.msg(q)
        enc_q = q.decode('utf-8')
        kkma_result = kkma.query(enc_q)
        rt = json.dumps({'params': params, 'result': kkma_result})
        return rt


URI_MAP = {
    '/': (process, [('Content-type', 'json')]),
}

def app(environ, start_response):
    '''
    @usage
    start :
        twistd web  --wsgi=knlp.app --logfile=knlp.log --port=tcp:8888
    stop :
        kill -9 `cat twistd.pid`
    '''

    # init konlpy
    kkma = KKMA()

    # get uri and query parsing
    uri = environ['PATH_INFO']

    # uri checker and switching
    process, header = URI_MAP.get(uri, URI_MAP.get('/'))

    # result
    result = process(kkma, environ)

    # output
    start_response('200 OK', header)
    return [result]