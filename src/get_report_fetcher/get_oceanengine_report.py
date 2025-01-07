# -*- coding: utf-8 -*-
from libs.oceanengine_sdk.src.oceanengine_sdk_py.oncenengine_sdk_client import OceanengineSdkClient
from libs.oceanengine_sdk.src.oceanengine_sdk_py.db.db_client import DbClient
from libs.format_converter import convert_dict_keys
import datetime
import pandas as pd


def get_customer_config(advertiser_id,data_topics):
    """
    获取自定义报表可用指标和维度
    :return:
    """
    db_client = DbClient('baidudb')
    oceanengine_param = db_client.select('select * from bd_auth_token where userName = "创想策划汇"')
    format_oceanengine_param = convert_dict_keys(oceanengine_param[0], 'snake')
    client = OceanengineSdkClient(format_oceanengine_param)
    new_oauth_token = client.oauth_sign()
    print(f'new_oauth_token:{new_oauth_token}')
    new_oauth_token = {'app_id': '1805969627151371', 'secret_key': '0cb84b67505483a617f983e3eaf33434b690baab', 'access_token': '6d697d51304d20b1d12417c1975b0c482763621e', 'refresh_token': 'dad5cf8c101b81fdd851d82fbcc1fab1e4fce632', 'expires_time': datetime.datetime(2025, 1, 7, 23, 45, 52, 719997), 'refresh_expires_time': datetime.datetime(2025, 2, 5, 23, 45, 52, 719997), 'auth_code': 'e15b25e0db733a81c4a6019d561d3c74ed23a5be', 'user_id': '92403628013', 'user_name': '创想策划汇'}
    format_oauth_token = convert_dict_keys(new_oauth_token, 'small_camel')
    print(format_oauth_token)
    update_sql, update_data = db_client.generate_sql(
        table_name="bd_auth_token",
        operation="update",
        columns=["accessToken", "refreshToken", "expiresTime", "refreshExpiresTime"],
        data=format_oauth_token,
        conditions="userName = '创想策划汇' and appId=1805969627151371"
    )
    print(f'sql:{update_sql},data:{update_data}')
    update_result = db_client.update(update_sql, update_data)
    print(f'update_result:{update_result}')
    query_params = {
        "advertiser_id": advertiser_id,
        "data_topics": data_topics
    }
    _data = client.v3___0_report_custom_config_get(query_params)
    dimensions_list = _data['data']['list'][0]['dimensions']
    metrics_list = _data['data']['list'][0]['metrics']
    df_dimensions = pd.DataFrame(dimensions_list)
    df_metrics = pd.DataFrame(metrics_list)
    df_dimensions.to_csv('dimensions.csv', index=False, encoding='utf-8_sig')
    df_metrics.to_csv('metrics.csv', index=False, encoding='utf-8_sig')




if __name__ == '__main__':
    get_customer_config(advertiser_id=1801616765879323,data_topics=['BASIC_DATA'])