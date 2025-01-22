import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))



from get_project_list import FeatchProjectList
from get_promotion_list import FeatchPromotionList
from libs.tool import get_oauth_client
from libs import sql_al_chemy
from libs.oceanengine_sdk.src.oceanengine_sdk_py import OceanengineSdkClient
from libs.tool import check_ocean_doc


class GetAdAccountStructure(object):
    def __init__(self,cc_account_id : str|int,ocean_client:OceanengineSdkClient=None):
        """
        初始化获取巨量广告账户结构
        :param cc_account_id:广告主id
        :param ocean_client:巨量引擎sdk客户端,可选，如果不传入则自动获取
        :return:self
        """
        if ocean_client is None:
            self.oceanengine_client = get_oauth_client()
        else:
            self.oceanengine_client = ocean_client
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
    def fetch(self)->dict:
        """
        获取广告账户结构
        :return:{
            'project_list':[],
            'promotion_list':[]
        }
        """
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
    item = GetAdAccountStructure(1800168496063497)
    result = item.fetch()
    # x = sql_al_chemy.CURD.insert_data_to_database(result['project_list'],sql_al_chemy.OceanAdProjectListTable,sql_al_chemy.ocean_session)
    # y = sql_al_chemy.CURD.insert_data_to_database(result['promotion_list'],sql_al_chemy.OceanAdPromotionListTable,sql_al_chemy.ocean_session)
    new_result = check_ocean_doc(sql_al_chemy.oceanengine.AdPromitionTable,result['promotion_list'])
    # key_not_in_table = set()
    # for temp in new_result:
    #     key_not_in_table.update(set(temp['key_not_in_tabla']))
    # print(key_not_in_table)
    print(new_result)

    project_not_in_key = {'star_task_version', 'native_setting', 'internal_advertiser_info'}#1802369766232155,7441783527307575307
    promotion_not_in_key = {'aweme_user_optimizable_detail', 'auto_extend_traffic', 'union_deep_cpabid'}#1802432785730570，7441783527307575307，7441785074430771254