import datetime

from requests import session
from sqlalchemy import func, or_, asc, desc

from app.core.environment import Environment
from app.modules.service.repository.models import Category, Badge, Service, ServiceBadge


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

    def get_services_by_filter(self, filters):
        query = Service.query

        if filters.get('category_id'):
            query = query.filter(Service.categories.id == filters.get('category_id'))
        if filters.get('duration'):
            query = query.filter(Service.duration_minutes <= filters.get('duration'))
        if filters.get('badge_id'):
            query = query.filter(Service.service_badges.id == filters.get('badge_id'))
        if filters.get('sort_by')=='price_asc':
            query = query.order_by(Service.price.asc())
        elif filters.get('sort_by')=='price_desc':
            query = query.order_by(Service.price.desc())
        elif filters.get('sort_by')=='newest':
            query = query.order_by(Service.create_at.desc())
        else:
            query = query.order_by(Service.create_at.asc())

        limit = filters.get('per_page')
        offset = (filters.get('page') - 1) * limit
        results = query.offset(offset).limit(limit).all()
        return results






