from json import load

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from classes.models import Base, Publisher, Book, Shop, Sale, Stock


class BooksDb:
    def __init__(self, dsn):
        self.__engine = create_engine(dsn)
        self.__base = Base

    def create_tables(self):
        self.__base.metadata.drop_all(self.__engine)
        self.__base.metadata.create_all(self.__engine)

    def make_session(self) -> Session:
        return Session(self.__engine)

    def insert_data_from_json(self, file: str):
        with self.make_session() as session:
            with open(file, encoding='utf-8') as file:
                data = load(file)
                if data:
                    models = dict(publisher=Publisher, book=Book, shop=Shop, sale=Sale,
                                  stock=Stock)
                    for row in data:
                        model = models.get(row.get('model'))
                        pk = row.get('pk')
                        fields = row.get('fields')
                        if pk and fields:
                            session.add(model(id=pk, **fields))

                    session.commit()

    def get_publisher_info(self):
        answer = self.__input_id_name()
        with self.make_session() as session:
            base_query = session.query(Publisher.name, Shop.name, Sale.price * Sale.count, Sale.date_sale) \
                .join(Book, Stock, Shop, Sale)
            if not answer:
                result = base_query.all()
            elif answer.isdigit():
                result = base_query.filter(Publisher.id == int(answer)).all()
            else:
                result = base_query.filter(Publisher.name.ilike(f'%{answer}%')).all()

            self.__print_publisher_info(result)

    @staticmethod
    def __print_publisher_info(publishers_info):
        if publishers_info:
            for publisher_info in publishers_info:
                name, shop, price, date = publisher_info
                print(name, shop, price, date, sep=' | ')
        else:
            print('Совпадений не найдено')

    @staticmethod
    def __input_id_name() -> str:
        print('Введите id издателя или его имя, для получения информации.')
        print('Или оставьте поле пустым, чтобы получить информацию по всем издателям')
        return input().strip()
