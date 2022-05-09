
# Team_E_Business Tesks _ Bearrobotics
원티드 프리온보딩 코스 _ 두번째 기업과제 _ 베어로보틱스

### 팀 노션 [GoTo](https://www.notion.so/Bearrobotics-a520ef6ae09246488ab573ad247083ee)
- 요구사항 분석, 정보 공유 및 프로젝트 진행을 위해 사용

## 과제 해석
이 서비스는 프랜차이즈 레스토랑 정보를 업로드할 수 있고, POS 데이터를 서버에 한번에 적재하고 관련 통계를 확인할 수 있는 플랫폼 서비스입니다.

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
	- [ ] POS 정보 총 검색
		- `start_time`, `end_time`, `time window size`로 검색할 시 `total_price` 조회
		- 전체 총 매출을 조회할 때 사용하는 파라미터는 다음과 같습니다.
			- 필수
				- start_time=YYYY-mm-dd HH:MM:SS
				- end_time=YYYY-mm-dd HH:MM:SS
				- timeunit=year/month/week/day/hour
			- 추가 선택
				- group=group name(string value)
				- address=string value
	- [ ] 메뉴 CRUD
		- 메뉴 정보를 담을 수 있는 테이블 생성
			- `menu`테이블과 `restaurant`테이블은 `group`으로 연결
		- 메뉴별 POS 정보 검색
			- `start_time`, `end_time`, `time window size`로 검색할 시 `menu`별 `total_price` 조회

## 구현

### 기술 스택
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/> <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=SQLite&logoColor=white"/> <img src="https://img.shields.io/badge/PyCharm-000000?style=flat-square&logo=PyCharm&logoColor=white"/> <img src="https://img.shields.io/badge/VSCode-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white"/>

### 개발 기간
- 2022.05.02 - 2022.05.06

> ### ERD
<img src="./source/bearrobotics_erd.png" alt="erd"/>

> ### 구성 요소
- **레스토랑(지점)(Restaurant)**
	- id: 레스토랑 고유 id값
	- name : 레스토랑 이름
	- city : 도시
	- address : 상세 주소
	- group : 레스토랑이 속한 그룹
- **POS 정보(Guest)**
	- id : POS 정보 고유 id값
	- timestamp : POS에 등록된 시간
	- price : 결제 가격
	- number_of_party : 방문자 수
	- payment : 결제 수단
	- restaurant : 결제를 한 레스토랑
- **그룹(Group)**
	- id : 그룹 고유 id 값
	- name : 그룹 이름
- **메뉴(Menu)**
	- id : 메뉴 고유 id값
	- name : 메뉴 이름
	- price : 메뉴 가격
	- created_at : 메뉴 생성 날짜
	- update_at : 메뉴 업데이트 날짜
	- group : 메뉴가 속한 그룹
- **사용자(Employee)**
	- id : 사용자 고유 id값
	- email : 사용자 email
	- username : 사용자 이름
	- phone_number : 사용자 연락처
	- group : 사용자가 속한 그룹

> ### API 명세

#### 레스토랑(지점) 관련
레스토랑(지점) 생성 : POST /api/restaurant  
- 이름, 도시, 상세주소, 그룹의 정보를 입력받아 레스토랑을 생성합니다.  

레스토랑(지점) 조회 : GET /api/restaurant  
- 레스토랑 정보를 조회합니다.  

레스토랑(지점) 상세 : GET /api/restaurant/:pk  
-  pk 값에 해당하는 레스토랑 정보를 조회합니다. 

레스토랑(지점) 수정 : PUT /api/restaurant/:pk  
-  pk 값에 해당하는 레스토랑 정보를 수정합니다.  

레스토랑(지점) 삭제 : DELETE /api/restaurant/:pk
-  pk 값에 해당하는 레스토랑 정보를 삭제합니다.  


레스토랑(지점) 총 매출 조회 : GET /api/restaurant/:pk/total_price?start_time=YYYY-mm-dd 00:00:00&end_time=YYYY-mm-dd 00:00:00&timeunit=...  
-   pk 값에 해당하는 레스토랑의 총 매출 통계 정보를 파라미터로 넘어온 기간에 따라 필터링하여 조회합니다.  

레스토랑(지점) 결제 방식별 결제 수 조회 : GET /api/restaurant/:pk/payment?start_time=YYYY-mm-dd 00:00:00&end_time=YYYY-mm-dd 00:00:00&timeunit=...  
-   pk 값에 해당하는 레스토랑의 결제 방식별 결제 수 정보를 파라미터로 넘어온 기간에 따라 필터링하여 조회합니다.  

레스토랑(지점) 방문자 수별 결제 수 조회 : GET /api/reataurant/:pk/party?start_time=YYYY-mm-dd 00:00:00&end_time=YYYY-mm-dd 00:00:00&timeunit=...  
-   pk 값에 해당하는 레스토랑의 방문자 수별 결제 수 정보를 파라미터로 넘어온 기간에 따라 필터링하여 조회합니다.  


#### POS 정보 관련
POS 정보 생성 : POST /api/pos  
- 결제 시간, 결제 가격, 방문자 수, 결제 방식, 레스토랑 정보를 입력받아 POS 정보를 생성합니다.  

POS 정보 조회 : GET /api/pos  
- POS 정보를 조회합니다.   

POS 정보 상세 : GET /api/pos/:pk  
- pk 값에 해당하는 POS 정보를 조회합니다.  

POS 정보 수정 : PUT /api/pos/:pk  
- pk 값에 해당하는 POS 정보를 수정합니다.  

POS 정보 삭제 : DELETE /api/pos/:pk
- pk 값에 해당하는 POS 정보를 삭제합니다.  

POS 정보 중 레스토랑별 총 매출 조회 : GET /api/pos/total_price?start_time=YYYY-mm-dd 00:00:00&end_time=YYYY-mm-dd 00:00:00&timeunit=...  
-   레스토랑별 총 매출 통계 정보를 파라미터로 넘어온 기간에 따라 필터링하여 조회합니다.

POS 정보 중 레스토랑, 결제 방식별 결제 수 조회 : GET /api/pos/payment POS?start_time=YYYY-mm-dd 00:00:00&end_time=YYYY-mm-dd 00:00:00&timeunit=...  
-   레스토랑, 결제 방식별 결제 수 정보를 파라미터로 넘어온 기간에 따라 필터링하여 조회합니다.

정보 중 레스토랑, 방문자 수별 결제 수 조회 : GET /api/pos/party?start_time=YYYY-mm-dd 00:00:00&end_time=YYYY-mm-dd 00:00:00&timeunit=...  
-   레스토랑, 방문자 수 별 결제 수 정보를 파라미터로 넘어온 기간에 따라 필터링하여 조회합니다.


#### 사용자 정보 관련
사용자 생성 : POST /api/users/signup
- 이메일, 이름, 비밀번호를 입력받아 사용자 회원가입을 진행합니다.

사용자 조회 : GET /api/users
- 가입된 사용자들을 조회합니다.

사용자 정보 상세 : GET /api/users/:pk
- pk 값에 해당하는 사용자 정보를 조회합니다.

사용자 정보 수정 : PUT /api/users/:pk
- pk 값에 해당하는 사용자 정보를 수정합니다.

사용자 정보 삭제 : DELETE /api/users/:pk
- pk 값에 해당하는 사용자 정보를 삭제합니다.


#### BONUS PART
**그룹 API**

그룹에 속한 모든 POS조회 : GET /api/group/
- 특정 그룹에 속한 것과 상관없이 모든 POS 정보를 조회합니다.

그룹에 속한 POS 조회 : GET /api/group/그룹이름
- 그룹이름이 그룹테이블에 있는지 조회하고 해당 그룹에 속한 POS 정보를 조회합니다.

그룹+기간에 해당하는 POS 조회: GET /api/group/그룹이름/?start_date=YYYY-mm-dd 00:00:00&end_date=YYYY-mm-dd 00:00:00
- 특정 기간 동안 특정 그룹의 POS 정보를 조회합니다.

그룹 + 기간 + 시간에 해당하는 POS 조회: GET /api/group/total_price?start_time=YYYY-mm-dd 00:00:00&end_time=YYYY-mm-dd 00:00:00&timeunit=...  
- 특정 기간 동안 특정 그룹에 속하는 POS 정보를 시간, 일, 주, 달, 연 으로 그룹핑하여 결제 정보를 조회합니다.


**주소 API**

찾으려는 주소가 있는지 조회 : GET /api/address/주소이름/
- 찾으려는 주소가 있는지 조회하고 주소에 해당하는 레스토랑이 POS에 있는지 확인

메뉴 생성 : POST /api/menu
- 이름, 가격, 그룹의 정보를 입력받아 메뉴를 생성합니다.

메뉴 조회 : GET /api/menu
- 메뉴 정보를 조회합니다.

메뉴 상세 : GET /api/menu/:pk
- pk 값에 해당하는 메뉴 정보를 조회합니다.

메뉴 수정 : PUT /api/menu/:pk
- pk 값에 해당하는 메뉴 정보를 수정합니다.

메뉴 삭제 : DELETE /api/menu/:pk
- pk 값에 해당하는 메뉴 정보를 삭제합니다.
  
POS 정보 중 레스토랑, 메뉴별 총 매출 조회 : GET /api/menu/total_price?start_time=YYYY-mm-dd 00:00:00&end_time=YYYY-mm-dd 00:00:00&timeunit=...  
- 레스토랑, 메뉴별 총 매출 통계 정보를 파라미터로 넘어온 기간에 따라 필터링하여 조회합니다.

> ### 구현 과정 중 특이사항
- utils/db_uploader.py를 사용하여 주어진 데이터셋을 database에 바로 저장해 요구사항을 확인, 구현하였습니다.
- 각 restaurant의 임의의 필터링을 거친 정렬된 KPI 자료들을 확인할 수 있도록 구현하였습니다.


### Step to run
```
$ python -m venv venv
$ source venv/Scripts/activate
$ python install -r requirements.txt
$ python manage.py runserver
```

## Author
- Team Leader : 강정희
	- modeling, restaurant API, exception handling : [강정희](https://github.com/Jjenny-K)
	- modeling, restaurant API, test code : [김채욱](https://github.com/kcw2297)
	- modeling, total_price by POS API : [서재환](https://github.com/woodstock1993)
	- modeling, user API, menu API, dockerize : [이형준](https://github.com/leeceo97)
- 이름을 클릭하면 개인 repository도 확인 가능합니다.

