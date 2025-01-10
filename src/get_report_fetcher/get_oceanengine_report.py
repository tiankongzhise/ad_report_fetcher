# -*- coding: utf-8 -*-
import os

from pydantic import BaseModel,Field
import tomllib

from libs.tool import save_data_to_csv
from libs.tool import get_oauth_client_and_update_token
from libs.tool import find_toml_file


class FetcherResult(BaseModel):
    total_page :int= 0,
    success_page:list[int]= Field(default_factory=list),
    data:list[dict]= Field(default_factory=list),
    error_page:list[int]= Field(default_factory=list),
    success_page_count:int= 0


class ReportFetcher(object):


    def __init__(self, advertiser_id, custom_config_path='./data/'):
        self.advertiser_id = advertiser_id

        self.custom_config_path = custom_config_path
        if not os.path.exists(self.custom_config_path):
            os.mkdir(self.custom_config_path)

        self.oceanengine_client = get_oauth_client_and_update_token()
        with open(find_toml_file('report_config.toml'), 'rb') as f:
            self.report_config = tomllib.load(f)






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
    @staticmethod
    def update_fetch_report_result(result: FetcherResult, page_number:int,report_rsp:dict):
        if report_rsp['code'] != 0:
            result.error_page.append(page_number)
            return f'page_number:{page_number} err,message:{report_rsp["message"]}'
        result.total_page = report_rsp['data']['page_info']['total_page']
        result.success_page.append(report_rsp['data']['page_info']['page'])
        result.data.extend(report_rsp['data']['rows'])
        result.success_page_count = len(result.success_page)
        return f'page_number:{page_number} success'
    def fetch_report(self, start_date, end_date, report_topic, report_type):
        result = FetcherResult()
        page_number = 1
        query_params = {
            "advertiser_id": self.advertiser_id,
            'data_topic': 'BASIC_DATA',
            "dimensions":self.report_config[report_type][report_topic]['dimensions'],
            "metrics":self.report_config[report_type][report_topic]['metrics'],
            "start_time": start_date,
            "end_time": end_date,
            "order_by":self.report_config[report_type][report_topic]['order_by'],
            "page":page_number,
            "page_size":100,
            'filters': self.report_config[report_type][report_topic]['filters']
        }
        data = self.oceanengine_client.v3___0_report_custom_get(query_params)
        if data['code'] != 0:
            raise Exception(f'获取自定义报表失败,code:{data["code"]},message:{data["message"]},request_id:{data["request_id"]}')
        self.update_fetch_report_result(result, 1, data)
        while page_number < data['data']['page_info']['total_page']:
            page_number = page_number + 1
            query_params['page'] = page_number
            data = self.oceanengine_client.v3___0_report_custom_get(query_params)
            self.update_fetch_report_result(result, page_number, data)
        return result



if __name__ == '__main__':
    report_fetcher = ReportFetcher(advertiser_id=1801616765879323)
    report_topic = 'BASIC_DATA'
    report_type = 'hourly_report'
    report = report_fetcher.fetch_report(start_date='2024-05-01', end_date='2024-08-31', report_topic=report_topic, report_type=report_type)
    report_save_name = f'{report_fetcher.custom_config_path}{report_topic}_{report_type}.csv'
    print(report)