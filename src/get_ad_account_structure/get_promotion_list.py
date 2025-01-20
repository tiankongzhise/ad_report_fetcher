from libs.oceanengine_sdk.src.oceanengine_sdk_py import OceanengineSdkClient
import json


class FeatchPromotionList(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self,ocean_client:OceanengineSdkClient):
        self.oceanengine_client = ocean_client
    def fetch(self, advertiser_id: str | int):
        result = []
        rsp = self.fetch_promotion_list(advertiser_id)
        self.special_trans(rsp)
        # print(rsp['data']['page_info'])
        result.extend(rsp['data']['list'])
        while rsp['data']['page_info']['page'] < rsp['data']['page_info']['total_page']:
            page = rsp['data']['page_info']['page'] + 1
            rsp = self.fetch_promotion_list(advertiser_id, page)
            self.special_trans(rsp)
            result.extend(rsp['data']['list'])
        return result


    def fetch_promotion_list(self, advertiser_id, page:int=1):
        query={
            "advertiser_id": advertiser_id,
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
        return rsp

if __name__ == '__main__':
    from libs.tool import create_oauth_client
    from sqlmodel import Session
    from libs.db import oceanengine_engine,OceanAdPromotionListTable
    ocean_client = create_oauth_client()
    fetcher = FeatchPromotionList(ocean_client)
    promotion_list = fetcher.fetch(advertiser_id=1802369766232155)
    with Session(oceanengine_engine) as session:
        for item in promotion_list:
            session.add(OceanAdPromotionListTable(**item))
        session.commit()