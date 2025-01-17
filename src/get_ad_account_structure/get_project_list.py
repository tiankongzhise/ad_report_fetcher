from libs.tool import create_oauth_client


class FeatchProjectList(object):
    def __init__(self,
                 advertiser_id:str,
                 custom_config_path:str='./data/'):
        self.advertiser_id = advertiser_id
        self.custom_config_path = custom_config_path
        self.oceanengine_client = create_oauth_client()

    def fetch(self):
        query={
            "advertiser_id": self.advertiser_id,
            "fields": [],
            "filtering":[],
            "page": 1,
            "page_size": 100
        }
        rsp = self.oceanengine_client.customer_center_advertiser_list_adApi(params=query)