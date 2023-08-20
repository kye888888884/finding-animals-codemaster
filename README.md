# Finding Animals

유기동물 검색 서비스

> 데모 사이트: [finding-animals.kro.kr](http://finding-animals.kro.kr:8000/)

---

# 프로젝트 소개

-   유기동물의 정보를 제공하는 서비스입니다.
-   반려동물을 잃어버려 찾고자 할 때, 유기동물의 정보를 제공하여 찾을 수 있도록 도와줍니다.
-   사용자는 반려동물의 종, 성별, 나이, 털색상 등과 사진을 입력하여 검색할 수 있습니다.
-   검색 결과는 유기동물의 발견 일자, 구조 지역, 특징, 사진 등을 제공합니다.
-   공공데이터포털의 [대전광역시 유기동물 조회 서비스 API](https://www.data.go.kr/data/15016646/openapi.do)를 이용합니다.

## 서비스 개발 동기

-   어렸을 때 반려동물을 잃어버려 무척 속상했던 경험이 있는데, 공공데이터포털의 유기동물 공고 API를 이용하면 앞으로 이런 아픔을 치유하는 데에 도움이 되겠다 싶어 개발을 시작하게 되었습니다.

## 타 서비스와의 차별점

-   타 서비스와는 달리 털 색, 종, 성별 등을 입력하여 검색할 수가 있습니다.
-   타 서비스와는 달리 사진을 입력값으로 주어 유사한 동물들을 찾아주는 서비스를 제공할 수 있습니다.

## 프로젝트 구조

-   data: 데이터 수집 및 처리 디렉토리
-   finding_animals: Django 프로젝트 디렉토리
-   model: 머신러닝 모델 디렉토리

## 환경설정

### 웹서버 및 데이터 수집

```
Python 3.8.17
Django 4.1
```

## 품종 분류 모델

1. 훈련에 사용된 데이터

-   Oxford-IIIT Pet Dataset과 Kaggle에 있는 강아지와 고양이 품종 데이터셋 중 api데이터와 유효한 데이터셋

-   강아지 37풍종
    아메리칸 불리 : 'americanBully',
    비글 : 'beagle',
    비숑프리제 : 'bichonFrize',
    보더콜리 : 'borderCollie',
    보스턴 테리어 : 'bostonTerrier',
    복서 : 'boxer',
    불테리어 : 'bullTerrier',
    불독: 'bulldog',
    치와와 : 'chihuahua',
    잉글리시 코커 스페니얼 : 'cockerSpaniel',
    웰시코기 : 'corgi',
    닥스훈트 : 'dachshund',
    도베르만 : 'doberman',
    도사견 : 'dosa',
    프랜치 불독 : 'frenchBulldog',
    포인터 : 'germanShorthairedPointer',
    그레이트 덴 : 'greatDane',
    허스키 : 'husky',
    이테리 그레이하운드 : 'italianGreyhound',
    진돗개 : 'jindo',
    말티즈 : 'maltese',
    미니어처 슈너우저 : 'miniaturePinscher',
    믹스견 : 'mix',
    페키니즈 : 'pekingese',
    포메라니안 : 'pomeranian',
    푸들 : 'poodle',
    풍산개 : 'poongSan',
    퍼그 : 'pug',
    리트리버 : 'retriever',
    사모예드 : 'samoyed',
    삽살개 : 'sapsaree',
    슈나우저 : 'schnauzer',
    세퍼드 : 'shepherd',
    시바견 : 'shiba',
    시츄 : 'shihTzu',
    스피츠 : 'spitz',
    요크 셔테리어 : 'yorkshireTerrier'

-   고양이 13품종
    아비시안 : 'abyssinian',
    아메리칸 숏헤어 : 'americanShorthair',
    벵갈 : 'bengal',
    브리티쉬 숏헤어 : 'britishShorthair',
    코리안 숏헤어 : 'koreanShorthair',
    메인 쿤: 'maineCoon',
    노르웨이 숲 고양이 : 'norwegianForest',
    페르시안 : 'persian',
    렉돌: 'ragdoll',
    러시안 블루 : 'russianBlue',
    샴: 'siamese',
    스핑크스 : 'sphynx',
    터키 앙고라: 'turkishAngora'

2. 시도한 모델

-   VGG16 : 초기에 사용했던 모델로 반려동물들을 35가지 품종으로 라벨링해 학습 -> 0.6정도의 낮은 정확도
-   Xception : VGG16에 비해 높은 정확도를 보여줌 -> epoch 30정도에서 0.9에 수렴
-   inceptionResnet_v2 : Xceoption모델과 학습률에서는 비슷하지만 조금 더 빠른 학습이 가능하여 최종 선택

3. 모델링

-   api에 강아지의 데이터 수가 압도적으로 많은 것을 고려해 데이터 증강 후 강아지 37종, 고양이 13종의 데이터로 학습
-   inceptionResnet_v2으로 파인튜닝하여 고양이와 강아지를 각각 분류하는 모델을 2가지 생성

4. 성능

-   고양이 13종 분류 모델

    -   Accuracy: 0.7537
    -   Precision: 0.7794
    -   Recall: 0.7717
    -   F1 Score: 0.7673

-   강아지 37종 분류 모델
    -   Accuracy: 0.8271
    -   Precision: 0.7625
    -   Recall: 0.7225
    -   F1 Score: 0.7327

5. 웹 활용

-   이미지를 입력값으로 품종 분류
-   추출한 feature Mattrix로 자신이 원하는 반려동물과 가장 유사한 api의 반려동물 추천

##

---

# 기능

-   반려동물의 종류, 성별, 종, 털색을 입력하여 검색할 수 있습니다.
-   검색 결과는 사진으로 표시되며, 5개씩 페이지네이션 됩니다.
-   검색 결과를 보호 상태, 지역으로 필터링할 수 있습니다.
-   동물 사진 검색 시 사진에서 특징을 추출하여 유사한 동물을 찾아줍니다. 실종된 동물을 찾을 때 도움이 될 것으로 기대합니다.
