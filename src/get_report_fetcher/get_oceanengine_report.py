# -*- coding: utf-8 -*-
import os
from libs.tool import save_data_to_csv
from libs.tool import get_oauth_client_and_update_token

class ReportFetcher:
    def __init__(self, advertiser_id, custom_config_path='./data/'):
        self.advertiser_id = advertiser_id
        self.custom_config_path = custom_config_path
        if not os.path.exists(self.custom_config_path):
            os.mkdir(self.custom_config_path)
        self.oceanengine_client = get_oauth_client_and_update_token()

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


if __name__ == '__main__':
    report_fetcher = ReportFetcher(advertiser_id=1801616765879323)
    report_fetcher.fetch_and_save_custom_configs()