<img src="https://image.rocketpunch.com/company/79452/beeorobotigseukoria_logo_1591678224.png?s=400x400&t=inside" alt="erd"/>

# Team_E_Business Tasks _ Bearrobotics
원티드 프리온보딩 코스 _ 두번째 기업과제 _ 베어로보틱스

### 배포 주소 [GoTo](http://13.125.224.101/api)
### 팀 노션 [GoTo](https://www.notion.so/Bearrobotics-a520ef6ae09246488ab573ad247083ee)
- 요구사항 분석, 정보 공유 및 프로젝트 진행을 위해 사용


## 과제 해석
이 서비스는 매장별 매출과 같은 민감한 통계자료가 있기 때문에 가입한
유저들중 등급에 따라 이용이 가능한 단계가 구분되어 있는 서비스라고 해석하였습니다.

## 구현 요구사항
- [x] 레스토랑(지점) CRUD
    - 각 레스토랑의 정보를 담을 수 있는 테이블 생성
    - 레스토랑(지점) 등록, 조회, 수정, 삭제
- [x] POS 정보 CRUD
    - 각 레스토랑의 POS 정보를 담을 수 있는 테이블 생성
    - POS 정보 등록, 조회, 수정, 삭제
- [x] 레스토랑별 POS 정보 검색
    - `strat_time`, `end_time`, `time window size`로 검색할 시 `restaurant`별 `total_price` / `Number of payments by payment method` / `Number of payments by number of partys` 조회
    - 레스토랑별 총 매출, 지불방식별 결제 수, 방문자 수별 결제 수를 조회할 때 사용하는 파라미터는 다음과 같습니다. 
        - 필수 
            - start_time=YYYY-mm-dd HH:MM:SS
            - end_time=YYYY-mm-dd HH:MM:SS
            - timeunit=year/month/week/day/hour
        - 추가 선택
            - min_price=integer value
            - max_price=integer value
            - min_party=integer value
            - max_party=integer value
            - group=group name(string value)
- Bonus Points
    - [x] POS 정보 총 검색
        - `start_time`, `end_time`, `time window size`로 검색할 시 `total_price` 조회
        - 전체 총 매출을 조회할 때 사용하는 파라미터는 다음과 같습니다.
            - 필수
                - start_time=YYYY-mm-dd HH:MM:SS
                - end_time=YYYY-mm-dd HH:MM:SS
                - timeunit=year/month/week/day/hour
            - 추가 선택
                - group=group name(string value)
                - address=string value
    - [x] 메뉴 CRUD
        - 메뉴 정보를 담을 수 있는 테이블 생성
            - `menu`테이블과 `restaurant`테이블은 `group`으로 연결
        - 메뉴별 POS 정보 검색
            - `start_time`, `end_time`, `time window size`로 검색할 시 `menu`별 `total_price` 조회
    - [x] 유저 인증
        - jwt 기반 인증
          - custom middleware, authentication 구현
          - permission 적용

## 구현

### 기술 스택
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/> <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=SQLite&logoColor=white"/> <img src="https://img.shields.io/badge/PyCharm-000000?style=flat-square&logo=PyCharm&logoColor=white"/> <img src="https://img.shields.io/badge/VSCode-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white"/> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=Docker&logoColor=white"/> <img src="https://img.shields.io/badge/AWS EC2-232F3E?style=flat-square&logo=Amazon AWS&logoColor=white"/>

### 개발 기간
- 2022.05.02 - 2022.05.09

> ### ERD
<img src="./source/bearrobotics_erd.png" alt="erd"/>

> ### API 명세
> http://13.125.224.101/swagger

> ### 구현 과정 중 특이사항
>- utils/db_uploader.py를 사용하여 주어진 데이터셋을 database에 바로 저장해 요구사항을 확인, 구현하였습니다.
>- 각 restaurant의 임의의 필터링을 거친 정렬된 KPI 자료들을 확인할 수 있도록 구현하였습니다.


### Step to run
```
$ python -m venv venv
$ source venv/Scripts/activate
$ python install -r requirements.txt
$ python manage.py runserver
```

## Author
### 강정희
* 프로젝트 초기 세팅
* Group model 모델링 및 구축
* 레스토랑(지점) CRUD API
    - 이름, 도시, 상세 주소, 그룹 정보를 필수로 받아 레스토랑 정보를 생성
    - 레스토랑 고유 id값으로 상세 정보 조회하고 'CONFIRM' 권한을 가진 사용자는 레스토랑의 정보를 수정하거나 삭제할 수 있음
* POS 정보 검색 API
    - 검색에 필요한 파라미터 예외처리 로직 구축
        - start_time, end_time, timeunit은 필수로 입력하도록 구현
        - 지정된 형식이 아니거나 이전 범위가 이후 범위보다 클 경우(기간, 판매 가격, 방문자 수 등의 범위) 400 code 리턴
    - api/pos/total_price?parameters...
        - 파라미터로 넘어온 검색 기간과 시간 단위에 따라 레스토랑별 총 매출 확인 가능
    - api/pos/payment?parameters...
        - 파라미터로 넘어온 검색 기간과 시간 단위에 따라 레스토랑, 결제 방식별 결제 수 확인 가능
* 레스토랑별 POS 정보 검색 API
    - 레스토랑 고유 id값으로 지점마다의 총 매출, 결제 수 등 확인 가능

### 김채욱
* 프로젝트 초기 세팅
* Restaurant model 모델링 및 구축
* POS 정보 검색 API
    - pos/party?parameters...
        - 파라미터로 넘어온 검색 기간과 시간 단위에 따라 레스토랑, 방문자 수별 결제 수 확인 가능
* Test Code
    - Restaurant/ Guest API를 각 method 별로 테스트 기능을 작성
    - Model 부분은 facotry boy와 faker를 이용해 테스트
    - pytest.ini설정 및 conftest 파일에 전체 함수 정의

### 이형준
* 프로젝트 초기 세팅
* Employee, Menu 모델링 및 구축
* Employee jwt 토큰 기반 인증(signup, login)
  * custom middleware, authentication
  * custom permission
* Employee CRUD
* Menu CRUD
* 전체 permission 분기 설정
* 배포
  * AWS EC2
  * DOCKER
* test code
  * user CRUD & get headers

### 서재환
* Guest model 모델링 및 ERD 작성

* POS CRUD API
   - POS 관련 CRUD api 작성

* DB UPLOADER 및 CSV file 작성
   - api 조회를 위한 데이터베이스 세팅

* 그룹 API 
   - 특정 그룹에 속한 것과 상관없이 모든 POS 정보 조회
   - 그룹이름이 그룹테이블에 있는지 조회하고 해당 그룹에 속한 POS 정보를 조회
   - 특정 기간 동안 특정 그룹의 POS 정보를 조회
   - 특정 기간 동안 특정 그룹에 속하는 POS 정보를 시간, 일, 주, 달, 연 중 하나로 그룹핑하여 POS 정보를 조회

* 주소 API
   - 찾으려는 주소가 있는지 조회하고 주소에 해당하는 레스토랑이 POS에 있는지 조회
   - 찾으려는 주소가 있는지 조회하고 있을 경우 특정기간에 한해서 주소에 해당하는 레스토랑이 POS 있는지 조회
   - 특정기간 동안 찾으려는 주소에 POS 정보를 시간, 일, 주, 달, 연 중 하나로 그룹핑하여 POS 정보를 조회합니다.

