import requests
import json

# 카프카 프로듀서를 통해 데이터를 전송하기 위한 라이브러리
from confluent_kafka import Producer

import proto.book_data_pb2 as pb2
from keywords import book_keywords

class KakaoException(Exception):
    pass

def get_original_data(query: str) -> dict:
    rest_api_key = "2581882b8ab7e2c66d02a981b483d26c"
    url = "https://dapi.kakao.com/v3/search/book"
    # requests.get() 메소드를 통해 res(=response) 응답 개체를 받아옴
    res = requests.get(
        url=url,
        headers={
            "Authorization": f"KakaoAK {rest_api_key}",
        },
        params={
            "query": query,
            "sort": 50,
            "start": 1
        }
    )
    # 에러 처리 : status code가 4 또는 5로 시작하면 클라이언트 에러 또는 서버 에러
    if res.status_code >= 400:
        raise KakaoException(res.content)

    # json.loads() : 위 텍스트를 딕셔너리로 바꿔주는 메소드
    return json.loads(res.text)

if __name__ == '__main__':

    # kafka configs 세팅
    conf = {
        'bootstrap.servers': 'localhost:29092', # docker container 설정 시 로컬에서는 9092가 아닌 29092로 요청을 보내도록 설정함
    }

    producer = Producer(conf)
    topic = "book"

    for keyword in book_keywords:
        original_data = get_original_data(query=keyword)
        for item in original_data['documents']:
            book = pb2.Book()

            book.title = item['title']
            book.author = '.'.join(item['authors']) # authors의 kakao json 형식은 list로 되어 있음 -> proto로 지정한 string 형식으로 변환 설정
            book.publisher = item['publisher']
            book.isbn = item['isbn']
            book.price = int(item['price'])
            book.publication_date = item['datetime']
            book.source = 'kakao'
            print("----")
            print(book)
            print("----")
            producer.produce(topic=topic, value=book.SerializeToString()) # book은 protocol buffer 형태 이므로 string으로 변환해야 함
            producer.flush() # 한 번에 많은 양의 데이터를 보내면 producer가 terminating되므로 flush를 사용해서 지연시킴(기다리게 함)
            print("전송 완료")