# Finding Animals

---

# 프로젝트 소개

-   유기동물의 정보를 제공하는 서비스입니다.
-   반려동물을 잃어버려 찾고자 할 때, 유기동물의 정보를 제공하여 찾을 수 있도록 도와줍니다.
-   사용자는 반려동물의 종, 성별, 나이, 털색상 등과 사진을 입력하여 검색할 수 있습니다. (현재 사진 검색은 미지원)
-   검색 결과는 유기동물의 발견 일자, 구조 지역, 특징, 사진 등을 제공합니다.
-   공공데이터포털의 [대전광역시 유기동물 조회 서비스 API](https://www.data.go.kr/data/15016646/openapi.do)를 이용합니다.

## 프로젝트 구조

-   data: 데이터 수집 및 처리 디렉토리
-   finding_animals: Django 프로젝트 디렉토리
-   model: 머신러닝 모델 디렉토리 (추후 진행)

## 환경설정

-   Python 3.8.17
-   Django 4.1
<!-- - torch 2.0.0 -->