from get_project_list import FeatchProjectList
from get_promotion_list import FeatchPromotionList
from libs.tool import create_oauth_client
from libs.db import oceanengine_engine,OceanAdPromotionListTable,OceanAdProjectListTable
from sqlmodel import Session


class GetAdAccountStructure(object):
    def __init__(self,cc_account_id : str|int):
        self.oceanengine_client = create_oauth_client()
        self.cc_account_id: str|int = cc_account_id
        self.advertiser_list:list = []

    def get_advertiser_list(self):
        result = []
        query = {
            "cc_account_id": self.cc_account_id,
            "page_size":100,
            "page":1
        }
        rsp = self.oceanengine_client.customer__center_advertiser_list_adApi(query)
        if rsp['code'] != 0:
            raise Exception(f'get_advertiser_list error:{rsp}')
        result.extend(rsp['data']['list'])
        while rsp['data']['page_info']['page']<rsp['data']['page_info']['total_page']:
            page = rsp['data']['page_info']['page']+1
            query['page'] = page
            rsp = self.oceanengine_client.customer__center_advertiser_list_adApi(query)
            if rsp['code'] != 0:
                raise Exception(f'get_advertiser_list error:{rsp}')
            result.extend(rsp['data']['list'])
        for item in result:
            self.advertiser_list.append(item['advertiser_id'])
        return result
    def fetch(self):
        result = {
            'project_list':[],
            'promotion_list':[]
        }
        self.get_advertiser_list()
        for advertiser_id in self.advertiser_list:
            result['project_list'].extend(FeatchProjectList(self.oceanengine_client).fetch(advertiser_id))
            result['promotion_list'].extend(FeatchPromotionList(self.oceanengine_client).fetch(advertiser_id))
        return result




if __name__ == '__main__':
    ad_account_structure = GetAdAccountStructure(cc_account_id=1800168496063497)
    result = ad_account_structure.fetch()
    with Session(oceanengine_engine) as session:
        # for item in result['project_list']:
        #     session.add(OceanAdProjectListTable(**item))
        # for item in result['promotion_list']:
        #     session.add(OceanAdPromotionListTable(**item))
        session.bulk_insert_mappings(OceanAdProjectListTable,result['project_list'])
        session.bulk_insert_mappings(OceanAdPromotionListTable,result['promotion_list'])
        session.commit()
