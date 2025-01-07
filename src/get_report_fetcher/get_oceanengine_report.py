# -*- coding: utf-8 -*-
import os

from pydantic import BaseModel

from libs.tool import save_data_to_csv
from libs.tool import get_oauth_client_and_update_token

class FetcherResult(BaseModel):
    total_page :int= 0,
    success_page:list[int]= [],
    data:list[dict]= [],
    error_page:list[int]= [],
    success_page_count:int= 0


class ReportFetcher(object):


    def __init__(self, advertiser_id, custom_config_path='./data/'):
        self.advertiser_id = advertiser_id

        self.custom_config_path = custom_config_path
        if not os.path.exists(self.custom_config_path):
            os.mkdir(self.custom_config_path)

        self.oceanengine_client = get_oauth_client_and_update_token()

        self.basic_data_report_result = FetcherResult()


        self._fetch_report_result_mapping = {
            'BASIC_DATA': {
                '': self.basic_data_report_result
            }
        }



    def fetch_and_save_custom_configs(self):
        data_topics = [
            'BASIC_DATA', 'QUERY_DATA', 'BIDWORD_DATA', 'MATERIAL_DATA',
            'PRODUCT_DATA', 'ONE_KEY_BOOST_DATA', 'DMP_DATA', 'VIDEO_DUARATION_DATA'
        ]
        for topic in data_topics:
            data = self.get_customer_config(data_topics=[topic])
            dimensions_file_name = f'{self.custom_config_path}{topic}_dimensions.csv'
            metrics_file_name = f'{self.custom_config_path}{topic}_metrics.csv'
            save_data_to_csv(data['data']['list'][0]['dimensions'], dimensions_file_name)
            save_data_to_csv(data['data']['list'][0]['metrics'], metrics_file_name)

    def get_customer_config(self, data_topics):
        query_params = {
            "advertiser_id": self.advertiser_id,
            "data_topics": data_topics
        }
        data = self.oceanengine_client.v3___0_report_custom_config_get(query_params)
        if data['code'] != 0:
            raise Exception(f'获取自定义报表可用指标和维度失败,code:{data["code"]},message:{data["message"]},requestId:{data["requestId"]}')
        return data

    def update_fetch_report_result(self, report_topic, report_type,report_rsp):
        obj = self._fetch_report_result_mapping[report_topic][report_type]
        obj.total_page = report_rsp['data']['page_info']['total_page']
        obj.success_page.append(report_rsp['data']['page_info']['page'])



    def fetch_basic_data_report(self, start_date, end_date, report_type=''):
        common_dimensions = [
            'ad_id', 'ad_name', 'campaign_id', 'campaign_name', 'creative_id', 'creative_name',
            'creative_status', 'creative_type', 'creative_word_id', 'creative_word_name',
            'creative_word_status', 'creative_word_type', 'creative_word_value', 'creative_word_value_type',
            'creative_word_value_value', 'create']
        common_metrics = [
            'ad_cost', 'ad_cost_rank', 'ad_cost_rank_rate', 'ad_cost_rank_rate_rank', 'ad_cost_rank_rate_rank_rate',
            'ad_cost_rank_rate_rank_rate_rank', 'ad_cost_rank_rate_rank_rate_rank_rate',
            'ad_cost_rank_rate_rank_rate_rank_rate_rank', 'ad_cost_rank_rate_rank_rate_rank_rate_rank_rate',
        ]
        add_dimensions = []
        add_metrics = []

        if report_type == '':
            add_dimensions = []
            add_metrics = []

        page_number = 1
        query_params = {
            "advertiser_id": self.advertiser_id,
            'data_topic': 'BASIC_DATA',
            "dimensions":common_dimensions.extend(add_dimensions),
            "metrics":common_metrics.extend(add_metrics),
            "start_time": start_date,
            "end_time": end_date,
            "order_by":[{"field":'',"type":'DESC'},{"field":'',"type":'ASC'}],
            "page":page_number,
            "page_size":100
        }
        data = self.oceanengine_client.v3___0_report_custom_get(query_params)
        if data['code'] != 0:
            raise Exception(f'获取自定义报表失败,code:{data["code"]},message:{data["message"]},requestId:{data["requestId"]}')

        while page_number < data['data']['page_info']['total_page']:
            page_number = page_number + 1
            query_params['page'] = page_number



if __name__ == '__main__':
    report_fetcher = ReportFetcher(advertiser_id=1801616765879323)
    report_fetcher.fetch_and_save_custom_configs()