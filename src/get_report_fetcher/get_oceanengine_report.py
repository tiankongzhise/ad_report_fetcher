# -*- coding: utf-8 -*-
from libs.oceanengine_sdk.src.oceanengine_sdk_py.oncenengine_sdk_client import OceanengineSdkClient
from libs.oceanengine_sdk.src.oceanengine_sdk_py.db.db_module import DbModule



def get_customer_config(advertiser_id,data_topics):
    """
    获取自定义报表可用指标和维度
    :return:
    """
    db_client = DbModule()
    db_client.get_db_connect()
    client = OceanengineSdkClient()
    client.oauth_sign()
    params = {
        "advertiser_id": "123456789",
        "fields": []
    }

