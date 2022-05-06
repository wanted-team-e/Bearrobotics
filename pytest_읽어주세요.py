"""
사용 설명:
배포 전에는 삭제 필요!!
자세한 설명은 https://pytest-django.readthedocs.io/en/latest/database.html 참조

실제 데이터베이스 사용시 (실행 x):
(비권장, 실제 데이터 오염 가능성 존재)
@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'path/to/dbfile.sqlite3',
    }

테스트 방법
실제 데이터베이스에 있는 데이터를 복사 후 사용:
python -Xutf8 manage.py dumpdata > testdata.json
(-Xutf8를 붙여서 한국어 인식)
(만약 데이터가 너무 커서 특정 모델만 copy할시, app.modelname
python -Xutf8 manage.py dumpdata restaurant.Restaurant> testdata.json
)

이후 실행!
"""


"""
Model 제약조건 검토 필요
"""