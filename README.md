# spark_kafka_project

## 1. 프로젝트 개요

- 실시간으로 웹 사이트들의 도서 정보를 가져와 가격의 최댓값, 최솟값 등 통계치를 계산하는 애플리케이션 작성
    - Kafka + Spark
    - Python 사용
    - kafka message format으로 protocol buffer 사용
        - https://protobuf.dev/
        - Json과 달리 스키마를 정의할 수 있고, 용량도 작으며 성능 우수


## 2. 시스템 구성

![image](https://github.com/user-attachments/assets/634309d9-ad72-4f4e-8e59-45daef0bf1bf)

- 카프카 브로커에 데이터를 전송하고, 컨슈머 부분은 스파크가 됨
- 스파크 스트리밍 애플리케이션이 카프카의 토픽으로부터 데이터를 받아와서 통계치 계산
- 프로듀서 단계에서 브로커로 데이터 전송을 할 때와 브로커로부터 컨슈머가 데이터를 받아올 때, 메세지의 포맷은 일반적으로 익숙한 string이나 int, json 같은 타입이 아닌 protocol buffer 사용
- protocol buffer는 언어나 플랫폼에 상관없이 구조화된 데이터를 전송하는 포맷


## 3. API 링크

- naver 책 검색 API
    - https://developers.naver.com/docs/serviceapi/search/book/book.md#개요
    - https://developers.naver.com/apps
- Kakao 책 검색 API
    - https://developers.kakao.com/docs/latest/ko/daum-search/dev-guide#search-book
    - https://developers.kakao.com/console/app
