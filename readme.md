# 2020 소프트웨어 개발 보안 경진대회 소개딩
## 팀 : 범죄도시
---

## 웹 페이지 구성

1. 로그인페이지 (mainPage app)
   - login (로그인 페이지)
   - sign up (회원가입 페이지)
   - complete (회원가입 완료 페이지)

2. Welcome 페이지 및 뉴스 (이하 innerMain)
  
3. 범죄 분포 및 CCTV 분포 지도

4. 지역별 범죄 차트

5. 순찰경로

6. 범죄 발생 예측

---

## 설치 파이선 패키지(pip3)

- 개발
  - pip3 install django(vserion = 3.1)
  - pip3 install pylint-django

- 웹

  - pip3 install Django (필)
<!-- pip3 install django-bootstrap4 -->

- 부트스트랩 (웹 템플릿)
  - 템플릿 사이트 : <a>https://startbootstrap.com/</a>
  - 템플릿 사용 Document : <a>https://www.w3schools.com/bootstrap4/default.asp</a>

- 어썸폰트 (폰트)
  - Awsome Font (계정필요, CDN) : <a>https://fontawesome.com/</a>

- 언스플래시 소스 (사진)
  - 사진 다운 및 링크 생성 : <a>https://source.unsplash.com/</a>
  
- 데이터 가공

  - pip3 install Pandas
  - pip3 install Numpy

- 지도

  - pip3 install folium
  - pip3 install gpxpy
  - pip3 install geojson

- 크롤링
  
  - pip3 install requests
  - pip3 install lxml
  - pip3 install html5lib
---

## 데이터 주의사항

- csv 인코딩 주의 :  euc-kr을 utf-8로 바꾸어야 함

## 명령어 주의

- pip update, pip3 update <-- "절대" 하지 말것
- 윈도우 python 명령어 버전 확인 (2인지 3인지)
- 본 프로젝트는 python3 기준으로 작성되었음
- 리눅스, macOS 기준(python3가 기본이 아닌 시스템 기준) python3 명령어로 구동시켜아 함

- python3 manage.py collectstatic
- python3 manage.py makemigration
- python3 manage.py migrate
- python3 manage.py runserver 8000
- python3 manage.py runserver [ip]:[port]