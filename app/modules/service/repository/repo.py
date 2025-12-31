from sqlalchemy.orm import joinedload

from .models import Category, Badge, Service, Feature, ServiceBadge
from app.utils.pagination import Pagination


class Repository:
    def __init__(self, db_session):
        self.session = db_session

    @staticmethod
    def get_all_category():
        return Category.query.all()

    @staticmethod
    def get_all_badge():
        return Badge.query.all()

    @staticmethod
    def get_all_services():
        return Service.query.all()

    @staticmethod
    def get_all_features():
        return Feature.query.all()

    @staticmethod
    def get_service_count():
        return Service.query.count()

    @staticmethod
    def get_list_services(pag : Pagination):
        return Service.query.offset(pag.offset()).limit(pag.size).all()

    @staticmethod
    def get_service_json(q: str):
        services = Service.query.filter(Service.name.ilike(f"%{q}%")).all()
        services_json = [s.to_json() for s in services]
        return services_json

    @staticmethod
    def get_list_services_filter(filters, pag: Pagination):
        query = Service.query.filter(Service.is_active == True)
        query = query.options(
            joinedload(Service.service_badges).joinedload(ServiceBadge.badge),
            joinedload(Service.categories)
        )

        if filters.get('text_search'):
            search_text = filters["text_search"].lower().strip()
            query = query.filter(Service.name.ilike(f'%{search_text}%'))
        if filters.get('category_id'):
            query = query.filter(Service.categories.any(Category.id == filters.get('category_id')))
        if filters.get('badge_id'):
            query = query.filter(Service.service_badges.any(ServiceBadge.badge_id == filters.get('badge_id')))
        if filters.get('feature_id'):
            query = query.filter(Service.features.any(Feature.id == filters.get('feature_id')))

        if filters.get('sort_by')=='price_asc':
            query = query.order_by(Service.price.asc())
        elif filters.get('sort_by')=='price_desc':
            query = query.order_by(Service.price.desc())
        elif filters.get('sort_by')=='newest':
            query = query.order_by(Service.id.desc())
        else:
            query = query.order_by(Service.id.asc())

        pagination = pag.to_dict(query.count())
        services = query.offset(pag.offset()).limit(pag.size).all()
        return services, pagination

    @staticmethod
    def get_list_services_by_ids(ids):
        service = Service.query.filter(Service.id.in_(ids)).all()
        return service

    def get_combo_services(self, pag : Pagination):
        combo = Service.query.filter(Service.type == "combo").all()
        return combo