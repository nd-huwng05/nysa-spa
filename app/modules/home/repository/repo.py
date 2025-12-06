from app.core.logger import logger
from app.core.environment import Environment
from .models import RoleSection, Section


class Repository:
    def __init__(self, env: Environment):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def get_section_nav(role_auth_method):
        try:
            if role_auth_method is None:
                return Section.query.filter(Section.role == RoleSection.DEFAULT).all()
            else:
                role_auth = role_auth_method.value
                if role_auth == RoleSection.ADMIN.value or  role_auth == RoleSection.STAFF.value:
                    return Section.query.filter(Section.role.value == role_auth).all()
                else:
                    return Section.query.filter(Section.role == RoleSection.DEFAULT, Section.role == RoleSection.CUSTOMER).all()
        except Exception as e:
            logger.error("Can't get section nav", data=e)
            raise Exception("500 Server Error")



