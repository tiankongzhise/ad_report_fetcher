# -*- coding: utf-8 -*-
import datetime
import os

from sqlmodel import SQLModel, Field,  create_engine
from sqlmodel import Column,Integer,String,Text,JSON,DateTime,UniqueConstraint,DECIMAL,Boolean

from sqlalchemy import MetaData

import dotenv
dotenv.load_dotenv()


# 从环境变量中读取配置
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# 构建认证数据库引擎
oauth_engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/baidudb"
)

class OauthTable(SQLModel, table=True):
    __tablename__ = 'bd_auth_token'

    key: int = Field(sa_column=Column(Integer, autoincrement=True, nullable=False,default=None, primary_key=True, index=True))
    appId: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    authCode: str = Field(sa_column=Column(Text(collation='utf8mb4_0900_ai_ci')))
    secretKey: str = Field(sa_column=Column(String(64, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    grantType: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    userName: str = Field(sa_column=Column(String(64, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    userId: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    refreshToken: str = Field(sa_column=Column(Text(collation='utf8mb4_0900_ai_ci')))
    accessToken: str = Field(sa_column=Column(Text(collation='utf8mb4_0900_ai_ci')))
    bdccAccountDict: dict = Field(sa_column=Column(JSON, nullable=True))
    expiresTime: datetime.datetime = Field(sa_column=Column(DateTime, nullable=True))
    refreshExpiresTime: datetime.datetime = Field(sa_column=Column(DateTime, nullable=True))
    tableUpdateTime: datetime.datetime = Field(sa_column=Column(DateTime, default=None))

    __table_args__ = (
        UniqueConstraint('userId', name='idx_only'),
    )

oceanengine_engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/oceanengine",
    echo = True
)

class OceanAdProjectListTable(SQLModel,table=True):
    __tablename__ = 'oceanengine_ad_project_list'
    auto_key: int = Field(sa_column=Column(Integer, autoincrement=True, nullable=False,default=None, primary_key=True))
    project_id:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    advertiser_id:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    delivery_mode:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    delivery_type:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    app_promotion_type:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    marketing_goal:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    ad_type:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    opt_status:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    name:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    project_create_time:datetime.datetime = Field(sa_column=Column(DateTime, nullable=True))
    project_modify_time:datetime.datetime = Field(sa_column=Column(DateTime, nullable=True))
    status:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    status_first:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    status_second:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    aigc_dynamic_creative_switch:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    star_task_id:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    star_auto_material_addition_switch:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    pricing:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    package_name:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    app_name:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    feed_delivery_search:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    search_bid_ratio:float = Field(sa_column=Column(DECIMAL(precision=5, scale=2), nullable=True))
    audience_extend:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    keywords:dict = Field(sa_column=Column(JSON, nullable=True))
    blue_flow_package:dict = Field(sa_column=Column(JSON, nullable=True))
    related_product:dict = Field(sa_column=Column(JSON, nullable=True))
    dpa_categories:dict = Field(sa_column=Column(JSON, nullable=True))
    dpa_product_target:dict = Field(sa_column=Column(JSON, nullable=True))
    dpa_adtype:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    delivery_product:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    delivery_medium:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    multi_delivery_medium:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    download_url:str = Field(sa_column=Column(Text( collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    download_type:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    download_mode:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    launch_type:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    promotion_type:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    open_url:str = Field(sa_column=Column(Text( collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    ulink_url:str = Field(sa_column=Column(Text( collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    subscribe_url:str = Field(sa_column=Column(Text( collation='utf8mb4_0900_ai_ci'), nullable=True,default=''))
    asset_type:str=Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    multi_asset_type:str=Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    micro_promotion_type:str=Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    quick_app_id:str=Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    micro_app_instance_id:str=Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    optimize_goal:dict = Field(sa_column=Column(JSON, nullable=True))
    value_optimized_type:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    landing_page_stay_time:int = Field(sa_column=Column(Integer, nullable=True))
    delivery_range:dict = Field(sa_column=Column(JSON, nullable=True))
    audience:dict = Field(sa_column=Column(JSON, nullable=True))
    delivery_setting:dict = Field(sa_column=Column(JSON, nullable=True))
    track_url_setting:dict = Field(sa_column=Column(JSON, nullable=True))
    open_url_type:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    open_url_field:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    open_url_params:str = Field(sa_column=Column(Text( collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    budget_group_id:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    if_newcustomerdelivery:bool = Field(sa_column=Column(Boolean, nullable=True))
    internal_advertiser_info:dict = Field(sa_column=Column(JSON, nullable=True))
    landing_type:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    star_task_version:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))



    __table_args__ = (
        UniqueConstraint('project_id','advertiser_id', name='idx_only'),
    )

class OceanAdPromotionListTable(SQLModel, table=True):
    __tablename__ = 'oceanengine_ad_promotion_list'
    auto_key: int = Field(sa_column=Column(Integer, autoincrement=True, nullable=False,default=None, primary_key=True))
    promotion_id: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    promotion_name: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    if_newcustomerdelivery: bool = Field(sa_column=Column(Boolean, nullable=True))
    project_id:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    advertiser_id:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    promotion_create_time: datetime.datetime = Field(sa_column=Column(DateTime, nullable=True))
    promotion_modify_time: datetime.datetime = Field(sa_column=Column(DateTime, nullable=True))
    aigc_dynamic_creative_switch:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    learning_phase: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    status: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    status_first: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    status_second: dict = Field(sa_column=Column(JSON, nullable=True, default=''))
    opt_status: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    star_task_id: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    star_task_version: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    star_auto_material_addition_switch: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    native_setting: dict = Field(sa_column=Column(JSON, nullable=True))
    has_carry_material:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    blue_flow_package:dict = Field(sa_column=Column(JSON, nullable=True))
    promotion_related_product: dict = Field(sa_column=Column(JSON, nullable=True))
    promotion_materials: dict = Field(sa_column=Column(JSON, nullable=True))
    source:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    is_comment_disable:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    ad_download_status:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    materials_type:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    budget: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    budget_mode: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    bid: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    cpa_bid: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    deep_cpabid: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    roi_goal: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    first_roi_goal: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2)))
    union_bid_ratio: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    union_bid: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    union_cpa_bid: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    union_deep_cpa_bid: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    union_roi_goal: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    shop_multi_roi_goals: dict = Field(sa_column=Column(JSON, nullable=True))
    schedule_time:str = Field(sa_column=Column(Text(collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    d7_retention:float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    material_score_info: dict = Field(sa_column=Column(JSON, nullable=True))
    creative_auto_generate_switch: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    config_id: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci')))
    brand_info: dict = Field(sa_column=Column(JSON, nullable=True))
    union_deep_cpabid: float = Field(sa_column=Column(DECIMAL(precision=10, scale=2), nullable=True))
    auto_extend_traffic: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    aweme_user_optimizable_detail:str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))

    __table_args__ = (
        UniqueConstraint('promotion_id', name='idx_only'),
    )


class OceanAdHourExternalActionTable(SQLModel):
    __tablename__ = 'oceanengine_ad_hour_external_action'
    auto_key: int = Field(sa_column=Column(Integer, autoincrement=True, nullable=False,default=None, primary_key=True, index=True))


tables_to_create = [OceanAdPromotionListTable.__table__,OceanAdProjectListTable.__table__]

SQLModel.metadata.create_all(bind=oceanengine_engine,tables=tables_to_create)