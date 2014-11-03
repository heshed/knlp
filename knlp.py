#!/usr/bin/env python
#-*- coding:utf-8 -*-
import urlparse
import json
import konlpy
from twisted.python import log

__author__ = 'binaa1'

class KONLPY:
    def __init__(self):
        self.kkma = konlpy.tag.Kkma()
        self.hannanum = konlpy.tag.Hannanum()
        self.mecap = konlpy.tag.Mecab()

    def query(self, q):
        return {
            'kkma_morphs': self.kkma.morphs(q),
            'kkma_nouns': self.kkma.nouns(q),
            'kkma_sentences': self.kkma.sentences(q),
            'kkma_pos': self.kkma.pos(q),
            'hannaum_morphs': self.hannanum.morphs(q),
            'hannaum_nouns': self.hannanum.nouns(q),
            'hannaum_analyze': self.hannanum.analyze(q),
            'hannaum_pos': self.hannanum.pos(q),
            'mecap_morphs': self.mecap.morphs(q),
            'mecap_nouns': self.mecap.nouns(q),
            'mecap_pos': self.mecap.pos(q),
        }

def process(konlpy, environ):
    if environ['REQUEST_METHOD'] == 'GET':
        params = urlparse.parse_qs(environ['QUERY_STRING'])
        q = params.get('q', '')[0]
        log.msg(q)
        enc_q = q.decode('utf-8')
        result = konlpy.query(enc_q)
        rt = json.dumps({'params': params, 'result': result})
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
    konlpy = KONLPY()

    # get uri and query parsing
    uri = environ['PATH_INFO']

    # uri checker and switching
    process, header = URI_MAP.get(uri, URI_MAP.get('/'))

    # result
    result = process(konlpy, environ)

    # output
    start_response('200 OK', header)
    return [result]