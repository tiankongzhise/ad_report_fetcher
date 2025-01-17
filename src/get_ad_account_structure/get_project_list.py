from libs.tool import create_oauth_client
from libs.db import oceanengine_engine,OceanAdProjectListTable
from sqlmodel import Session


class FeatchProjectList(object):
    def __init__(self,
                 advertiser_id:str,
                 custom_config_path:str='./data/'):
        self.advertiser_id = advertiser_id
        self.custom_config_path = custom_config_path
        self.oceanengine_client = create_oauth_client()

    def fetch(self,page:int=1):
        query={
            "advertiser_id": self.advertiser_id,
            "fields": [],
            "page": page,
            "page_size": 100
        }
        rsp = self.oceanengine_client.v3___0_project_list(params=query)
        return rsp


if __name__ == '__main__':
    fetcher = FeatchProjectList(advertiser_id=1802369766232155)
    result = []
    rsp = fetcher.fetch()
    print(rsp['data']['page_info'])
    result.extend(rsp['data']['list'])
    while rsp['data']['page_info']['page']<rsp['data']['page_info']['total_page']:
        page = rsp['data']['page_info']['page']+1
        rsp = fetcher.fetch(page)
        result.extend(rsp['data']['list'])
        print(rsp['data']['page_info'])



    with Session(oceanengine_engine) as session:
        session.bulk_insert_mappings(OceanAdProjectListTable,rsp['data']['list'])
        session.commit()
