cd weapp

python manage.py test -v2  -- -c=integration_nose2.cfg --with-cov --cov-report=html -B --cov-config=.coveragerc --no-user-config -v --log-level=30 utils

@echo �������
@echo ��weapp/coverage_html_report/index.html�鿴���Ը����ʷ������

pause