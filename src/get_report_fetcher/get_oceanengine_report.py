# -*- coding: utf-8 -*-
import os

import tomllib
from operator import invert
from typing import Literal, Mapping

from libs.tool import save_data_to_csv
from libs.tool import get_oauth_client_and_update_token
from libs.tool import find_toml_file
from libs.tool import FetcherResult
from libs.tool import parse_report_data
from libs.tool import split_date_range

REPORT_TOPIC = Literal[
            'BASIC_DATA', 'QUERY_DATA', 'BIDWORD_DATA', 'MATERIAL_DATA',
            'PRODUCT_DATA', 'ONE_KEY_BOOST_DATA', 'DMP_DATA', 'VIDEO_DUARATION_DATA'
        ]




class ReportFetcher(object):


    def __init__(self, advertiser_id, custom_config_path='./data/'):
        self.advertiser_id = advertiser_id

        self.custom_config_path = custom_config_path
        if not os.path.exists(self.custom_config_path):
            os.mkdir(self.custom_config_path)
        with open(find_toml_file('report_config.toml'), 'rb') as f:
            self.report_config = tomllib.load(f)

        self.oceanengine_client = get_oauth_client_and_update_token()








    def fetch_and_save_custom_configs(self):
        data_topics = self.report_config['report_topic']
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
        return result
    def fetch_report(self,
                     start_date:str,
                     end_date:str,
                     report_topic:REPORT_TOPIC,
                     report_type:Literal['hourly_report','daily_report','city_report','user_profile_report'],
                     report_class:Literal['campaign_type','delivery_mode'],
                     page_number:int|None = None)->FetcherResult:
        """
        :param start_date:开始时间。格式为：yyyy-MM-dd。例如2022-08-01

        :param end_date:结束时间。格式为：yyyy-MM-dd。例如2022-08-01

        :param report_topic:数据主题,枚举类型，BASIC_DATA广告基础数据，QUERY_DATA搜索词数据，BIDWORD_DATA关键词数据，
        MATERIAL_DATA素材数据，PRODUCT_DATA产品数据，ONE_KEY_BOOST_DATA一键起量（巨量广告升级版），DMP_DATA人群包数据，


        :param report_type:报告类型，枚举类型，枚举值：hourly_report小时报，daily_report日报，city_report地域报告，
        user_profile_report人群属性报告

        :param page_number:页码,如果为None，则获取从第一页开始的所有数据，如果非None，则获取指定页单页数据。

        :return:FetcherResult类
        """
        result = FetcherResult()
        query_params = {
            "advertiser_id": self.advertiser_id,
            'data_topic': 'BASIC_DATA',
            "dimensions":self.report_config[report_type][report_topic][report_class]['dimensions'],
            "metrics":self.report_config[report_type][report_topic][report_class]['metrics'],
            "start_time": start_date,
            "end_time": end_date,
            "order_by":self.report_config[report_type][report_topic][report_class]['order_by'],
            "page_size":100,
            'filters': self.report_config[report_type][report_topic][report_class]['filters']
        }
        if page_number is not None:
            query_params['page'] = page_number
        print(f'query_params:{query_params}')
        data = self.oceanengine_client.v3___0_report_custom_get(query_params)
        if data['code'] != 0:
            raise Exception(f'获取自定义报表失败,code:{data["code"]},message:{data["message"]},request_id:{data["request_id"]}')
        if page_number is not None:
            return self.update_fetch_report_result(result, page_number, data)

        page_number = 1
        self.update_fetch_report_result(result, page_number, data)

        while page_number < data['data']['page_info']['total_page']:
            page_number = page_number + 1
            query_params['page'] = page_number
            data = self.oceanengine_client.v3___0_report_custom_get(query_params)
            self.update_fetch_report_result(result, page_number, data)
        return result

    def fetch_report_all(self,
                        start_date: str,
                        end_date: str,
                        report_topic: REPORT_TOPIC,
                        report_type: Literal['hourly_report', 'daily_report', 'city_report', 'user_profile_report'],
                        report_class: Literal['campaign_type', 'delivery_mode'],
                        page_number: int | None = None)->list[Mapping]:
        """
        :param start_date:开始时间。格式为：yyyy-MM-dd。例如2022-08-01

        :param end_date:结束时间。格式为：yyyy-MM-dd。例如2022-08-01

        :param report_topic:数据主题,枚举类型，BASIC_DATA广告基础数据，QUERY_DATA搜索词数据，BIDWORD_DATA关键词数据，
        MATERIAL_DATA素材数据，PRODUCT_DATA产品数据，ONE_KEY_BOOST_DATA一键起量（巨量广告升级版），DMP_DATA人群包数据，


        :param report_type:报告类型，枚举类型，枚举值：hourly_report小时报，daily_report日报，city_report地域报告，
        user_profile_report人群属性报告

        :param page_number:页码,如果为None，则获取从第一页开始的所有数据，如果非None，则获取指定页单页数据。

        :return:FetcherResult类
        """
        result = []
        if report_type == 'hourly_report':
            data_interval = 'hourly'
        else:
            data_interval = 'daily'

        data_range = split_date_range(start_date, end_date, data_interval)
        for data_range_item in data_range:
            temp = self.fetch_report(start_date=data_range_item['start_date'],
                                     end_date=data_range_item['end_date'],
                                     report_topic=report_topic,
                                     report_type=report_type,
                                     report_class=report_class,
                                     page_number=page_number)
            result.append({'start_date':data_range_item['start_date'],'end_date':data_range_item['end_date'],'report':temp})
        return result






if __name__ == '__main__':
    report_fetcher = ReportFetcher(advertiser_id=1802369766232155)
    report_topic = 'BASIC_DATA'
    report_type = 'daily_report'
    report_class = 'delivery_mode'
    report = report_fetcher.fetch_report_all(start_date='2024-05-01',
                                         end_date='2024-08-31',
                                         report_topic=report_topic,
                                         report_type=report_type,
                                         report_class=report_class)

    for item in report:
        report_save_name = f'{report_fetcher.custom_config_path}{item['start_date']}_{item['end_date']}_{report_topic}_{report_type}_{report_class}.csv'
        data = parse_report_data(item['report'])
        save_data_to_csv(data, report_save_name)