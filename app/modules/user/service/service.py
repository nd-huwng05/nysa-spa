from app.core.environment import Environment
from ..config.config_module import UserConfig
from ..repository.repo import Repository

class Service:
    def __init__(self, repo:Repository, config: UserConfig, env: Environment):
        self.repo = repo
        self.env = env
        self.config = config

    def auth_user_pass(self, username:str, password:str):
        user = self.repo.get_user_by_username(username)
        if not user or not user.check_password_hash(password):
            raise ValueError('Invalid username or password')
        self.repo.update_last_login_at(user.id)
        self.repo.db.session.commit()
        return user

    def google_callback(self, userinfo):
        try:
            provider_id = userinfo.get('sub')
            user_auth_google = self.repo.get_user_auth_by_provider_id(provider_id)
            if not user_auth_google:
                avatar = userinfo.get('picture')
                name = userinfo.get('name')
                email = userinfo.get('email')
                user = self.repo.create_user(avatar, name)
                customer = self.env.modules.customer_module.service.get_customer_by_email(email)
                if not customer:
                    self.env.modules.customer_module.service.create_customer_has_account(name, email, user.id)
                else:
                    customer.user_id = user.id
                self.repo.create_auth_method_google(user.id, provider_id)
            else:
                self.repo.update_last_login_at(user_auth_google.user_id)
                user = user_auth_google.user
            self.repo.db.session.commit()
            return user
        except Exception as e:
            self.repo.db.session.rollback()
            raise e

    def get_user(self, id):
        return self.repo.get_user(id)