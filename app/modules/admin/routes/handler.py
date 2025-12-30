from ..service.service import Service

class Handler:
    def __init__(self, config, service:Service, env):
        self.config = config
        self.service = service
        self.env = env

    def get_data_for_dashboard(self):
        activities = self.env.modules.booking_module.service.get_status_booking()
        statistical = self.env.modules.booking_module.service.get_statistical()
        time_gold = self.env.modules.booking_module.service.get_time_gold()
        freq = self.env.modules.booking_module.service.get_frequency()
        return {
            'activities': activities,
            'statistical': statistical,
            'time_gold': time_gold,
            'frequency': freq
        }

    def get_data_for_settings(self):
        settings = self.env.modules.setting_module.service.get_data_setting()
        return {
            'setting': settings,
        }

