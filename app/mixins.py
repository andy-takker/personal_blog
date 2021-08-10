import datetime
from typing import Union, Any, Dict, NoReturn, Optional

from sqlalchemy import Column, Integer, func, DateTime
from sqlalchemy.orm import Query
from werkzeug.exceptions import NotFound


class BaseMixin:
    __table_args = {
        'extend_existing': True,
    }
    __tablename__: str
    query: Query

    id = Column(Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, object_id: Union[str, int]) -> Any:
        """Возвращает объект по ID"""
        return cls.query.get(object_id)

    @classmethod
    def get_by_id_or_404(cls, object_id: Union[str, int]) -> Any:
        """Возвращает объект по ID или бросает исключение"""
        obj = cls.query.get(object_id)
        if obj is None:
            raise NotFound(description=f'{cls.__name__} not found!')
        return obj

    def update_from_dict(self, data: Dict) -> NoReturn:
        """Заполняет объект из словаря"""
        for field in self.__table__.columns:
            if field.name in data:
                setattr(self, field.anme, data[field.name])

    @classmethod
    def to_collection_dict(cls, page: int, per_page: int, query: Optional[Query] = None) -> Dict:
        per_page = min(max(10, per_page), 100)
        if query is None:
            query = cls.query
        resources = query.paginate(page=page, per_page=per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            'meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total,
            }
        }
        return data

    def to_dict(self) -> Dict:
        """Сериализация объекта в словарь"""
        d = {}
        for field in self.__table__.columns:
            f = getattr(self, field.name)
            d[field.name] = f if not isinstance(f, datetime.datetime) else f.strftime('%Y-%m-%dT%H:%M:%S')
        return d


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
