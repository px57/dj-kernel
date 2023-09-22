from django.apps import AppConfig

class StreamConfig(AppConfig):
    def init():
        from enterprise.models import EnterpriseModel
        StreamConfig.REAL_TABLE_NAME = {
            'EnterpriseModel':  'enterprise_enterprisemodel'
        }
        StreamConfig.INSTALLED_MODELS = [EnterpriseModel]
        StreamConfig.SERVER_CONFIG = {
            '127.0.0.1:8000': {
                'list_models': [EnterpriseModel]
            }
        }

    def get_models_with_name(__name__):
        for models in StreamConfig.INSTALLED_MODELS:
            if models.__name__ == __name__:
                return models
        return False

    def get_real_table_name(__name__):
        if __name__ in StreamConfig.REAL_TABLE_NAME:
            return StreamConfig.REAL_TABLE_NAME[__name__]
        return False

    name = 'stream'
    public_key = '50b9f4f2b81147b4ac7766b43c282fe8'
    secret_key = ''
