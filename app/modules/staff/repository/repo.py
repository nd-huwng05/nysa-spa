from .models import Staff

class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    def get_all_active_staff(self):
        return self.db.session.query(Staff).filter(Staff.is_active==True).all()
