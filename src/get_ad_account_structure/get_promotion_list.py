from libs.tool import create_oauth_client
from libs.db import oceanengine_engine,OceanAdPromotionListTable
from sqlmodel import Session
import json

class FeatchPromotionList(object):
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
            "page_size": 20
        }
        rsp = self.oceanengine_client.v3___0_promotion_list(params=query)
        return rsp
    @staticmethod
    def special_trans(rsp):
        # print(f's f {rsp}')
        if rsp['code'] != 0:
            return rsp
        new_list = []
        for item in rsp['data']['list']:
            # 替换7d无法再python中命名的问题
            if '7d_retention' in item:
                item['d7_retention'] = item.pop('7d_retention')
            if 'status_second' in item:
                item['status_second'] = json.dumps(item['status_second'])
            if 'shop_multi_roi_goals' in item:
                item['shop_multi_roi_goals'] = json.dumps(item['shop_multi_roi_goals'])

            new_list.append(item)
        rsp['data']['list'] = new_list
        # print(f's e {rsp}')
        return rsp

if __name__ == '__main__':
    fetcher = FeatchPromotionList(advertiser_id=1802369766232155)
    result = []
    rsp = fetcher.fetch()
    fetcher.special_trans(rsp)
    # print(rsp['data']['page_info'])
    result.extend(rsp['data']['list'])
    while rsp['data']['page_info']['page']<rsp['data']['page_info']['total_page']:
        page = rsp['data']['page_info']['page']+1
        rsp = fetcher.fetch(page)
        fetcher.special_trans(rsp)
        result.extend(rsp['data']['list'])
        # print(rsp['data']['page_info'])
    # promotion = OceanAdPromotionListTable.model_validate(result[0])

    # for temp in result:
    #     for item in temp.keys():
    #         if temp[item] is not None:
    #             if type(temp[item]) not in [str, int, float, bool,dict,None]:
    #                 print(f'key:{item},value:{temp[item]}',type(temp[item]))

        # print(f'\n key:{item},value:{result[0][item]}\n')
    # print(result[0])
    with Session(oceanengine_engine) as session:
        session.bulk_insert_mappings(OceanAdPromotionListTable,result)
        session.commit()
