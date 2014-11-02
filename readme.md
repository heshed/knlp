KNLP 데몬
==============

* [http://konlpy.org] 라이브러리를 이용한 한국어 형태소 분석기 데몬

Install
--------------

    clone knlp
    pip -r requirements.txt'''

Run
--------------

    twistd web —-wsgi=knlp.app —-logfile=knlp.log -p tcp:8888

Usage
--------------

* open [http://localhost:8888?q=input_your_query]

License
--------------

* GPL v3[http://konlpy.org/ko/latest/#license]

More
--------------

* 현재 OSX 에서 데몬을 띄우고 쿼리를 날리면 결과를 보여준 후 죽는 문제가 있다.
