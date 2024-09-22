import requests
import json

from confluent_kafka import Producer
import proto.book_data_pb2 as pb2
from keywords import book_keywords

class NaverException(Exception):
    pass

def get_original_data(query: str) -> dict:
    client_id = "6yxU63bUcV180HWR4V3Y"
    client_secret = "TzF80YJekZ"
    url = "https://openapi.naver.com/v1/search/book.json"
    # requests.get() 메소드를 통해 res(=response) 응답 개체를 받아옴
    res = requests.get(
        url=url,
        headers={
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        },
        params={
            "query": query,
            "display": 100,
            "start": 1,
        }
    )
    # 에러 처리 : status code가 4 또는 5로 시작하면 클라이언트 에러 또는 서버 에러
    if res.status_code >= 400:
        raise NaverException(res.content)

    # json.loads() : 위 텍스트를 딕셔너리로 바꿔주는 메소드
    return json.loads(res.text)

if __name__ == '__main__':

    # kafka configs 세팅
    conf = {
        'bootstrap.servers': 'localhost:29092',
    }
    producer = Producer(conf)
    topic = "book"

    for keyword in book_keywords:
        original_data = get_original_data(query=keyword)

        for item in original_data['items']:
            book = pb2.Book()
            # dictionary -> protobuf
            book.title = item['title']
            book.author = item['author']
            book.publisher = item['publisher']
            book.isbn = item['isbn']
            book.price = int(item['discount'])
            book.publication_date = item['pubdate']
            book.source = 'naver'
            print("----")
            print(book)
            print("----")
            producer.produce(topic= topic, value=book.SerializeToString())
            producer.flush()
            print("전송 완료")
