# -*- coding: utf-8 -*-
import os
import json
import  dotenv

from sqlalchemy import Column,String,Integer,DateTime,Text,Boolean,DECIMAL,JSON, URL,UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import MetaData







dotenv.load_dotenv()


# 从环境变量中读取配置
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# 数据库配置
OCEANENGINE_DATABASE_URL = URL.create(
    "mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database="oceanengine",
)

# 创建同步引擎
engine = create_engine(
    OCEANENGINE_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=3600,
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),
    json_deserializer=lambda obj: json.loads(obj),
)

ocean_session = Session(engine)

# 基类
class Base(DeclarativeBase):
    # 定义类属性来处理特殊字段映射
    FIELD_MAPPING = {
        '7d_retention': 'd7_retention',
        'd7_retention': '7d_retention'
    }

    def __init__(self, **kwargs):
        # 处理输入数据中的特殊字段
        for old_key, new_key in self.FIELD_MAPPING.items():
            if old_key in kwargs:
                kwargs[new_key] = kwargs.pop(old_key)
        # 处理 list 类型字段转换为 JSON
        if 'status_second' in kwargs and isinstance(kwargs['status_second'], list):
            kwargs['status_second'] = json.dumps(kwargs['status_second'], ensure_ascii=False)
            
        if 'shop_multi_roi_goals' in kwargs and isinstance(kwargs['shop_multi_roi_goals'], list):
            kwargs['shop_multi_roi_goals'] = json.dumps(kwargs['shop_multi_roi_goals'], ensure_ascii=False)
            
        # 修改这里：直接设置属性而不是调用 super().__init__
        for key, value in kwargs.items():
            setattr(self, key, value)
    def to_dict(self):
        # 获取对象的字典表示
        result = {c.key: getattr(self, c.key) 
                 for c in self.__table__.columns}
        
        # 处理特殊字段映射
        for db_key, api_key in self.FIELD_MAPPING.items():
            if db_key in result:
                result[api_key] = result.pop(db_key)
                
        return result



class OceanAdProjectListTable(Base):
    __tablename__ = 'oceanengine_ad_project_list'
    auto_key = Column(Integer, autoincrement=True, nullable=False, default=None, primary_key=True)
    project_id = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    advertiser_id = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    delivery_mode = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    delivery_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    app_promotion_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    marketing_goal = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    ad_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    opt_status = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    name = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    project_create_time = Column(DateTime, nullable=True)
    project_modify_time = Column(DateTime, nullable=True)
    status = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    status_first = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    status_second = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    aigc_dynamic_creative_switch = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    star_task_id = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    star_auto_material_addition_switch = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    pricing = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    package_name = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    app_name = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    feed_delivery_search = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    search_bid_ratio = Column(DECIMAL(precision=5, scale=2), nullable=True)
    audience_extend = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    keywords = Column(JSON, nullable=True)
    blue_flow_package = Column(JSON, nullable=True)
    related_product = Column(JSON, nullable=True)
    dpa_categories = Column(JSON, nullable=True)
    dpa_product_target = Column(JSON, nullable=True)
    dpa_adtype = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    delivery_product = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    delivery_medium = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    multi_delivery_medium = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    download_url = Column(Text(collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    download_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    download_mode = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    launch_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    promotion_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    open_url = Column(Text(collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    ulink_url = Column(Text(collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    subscribe_url = Column(Text(collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    asset_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    multi_asset_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    micro_promotion_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    quick_app_id = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    micro_app_instance_id = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    optimize_goal = Column(JSON, nullable=True)
    value_optimized_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    landing_page_stay_time = Column(Integer, nullable=True)
    delivery_range = Column(JSON, nullable=True)
    audience = Column(JSON, nullable=True)
    delivery_setting = Column(JSON, nullable=True)
    track_url_setting = Column(JSON, nullable=True)
    open_url_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    open_url_field = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    open_url_params = Column(Text(collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    budget_group_id = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    if_newcustomerdelivery = Column(Boolean, nullable=True)
    internal_advertiser_info = Column(JSON, nullable=True)
    landing_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    star_task_version = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')

    __table_args__ = (
        UniqueConstraint('project_id','advertiser_id', name='idx_only'),
    )

class OceanAdPromotionListTable(Base):
    __tablename__ = 'oceanengine_ad_promotion_list'
    auto_key = Column(Integer, autoincrement=True, nullable=False, default=None, primary_key=True)
    promotion_id = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    promotion_name = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    if_newcustomerdelivery = Column(Boolean, nullable=True)
    project_id = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    advertiser_id = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    promotion_create_time = Column(DateTime, nullable=True)
    promotion_modify_time = Column(DateTime, nullable=True)
    aigc_dynamic_creative_switch = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    learning_phase = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    status = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    status_first = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    status_second = Column(JSON, nullable=True, default='')
    opt_status = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    star_task_id = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    star_task_version = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    star_auto_material_addition_switch = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    native_setting = Column(JSON, nullable=True)
    has_carry_material = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    blue_flow_package = Column(JSON, nullable=True)
    promotion_related_product = Column(JSON, nullable=True)
    promotion_materials = Column(JSON, nullable=True)
    source = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    is_comment_disable = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    ad_download_status = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    materials_type = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    budget = Column(DECIMAL(precision=10, scale=2), nullable=True)
    budget_mode = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    bid = Column(DECIMAL(precision=10, scale=2), nullable=True)
    cpa_bid = Column(DECIMAL(precision=10, scale=2), nullable=True)
    deep_cpabid = Column(DECIMAL(precision=10, scale=2), nullable=True)
    roi_goal = Column(DECIMAL(precision=10, scale=2), nullable=True)
    first_roi_goal = Column(DECIMAL(precision=10, scale=2))
    union_bid_ratio = Column(DECIMAL(precision=10, scale=2), nullable=True)
    union_bid = Column(DECIMAL(precision=10, scale=2), nullable=True)
    union_cpa_bid = Column(DECIMAL(precision=10, scale=2), nullable=True)
    union_deep_cpa_bid = Column(DECIMAL(precision=10, scale=2), nullable=True)
    union_roi_goal = Column(DECIMAL(precision=10, scale=2), nullable=True)
    shop_multi_roi_goals = Column(JSON, nullable=True)
    schedule_time = Column(Text(collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    d7_retention = Column(DECIMAL(precision=10, scale=2), nullable=True)
    material_score_info = Column(JSON, nullable=True)
    creative_auto_generate_switch = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    config_id = Column(String(32, collation='utf8mb4_0900_ai_ci'))
    brand_info = Column(JSON, nullable=True)
    union_deep_cpabid = Column(DECIMAL(precision=10, scale=2), nullable=True)
    auto_extend_traffic = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    aweme_user_optimizable_detail = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')

    __table_args__ = (
        UniqueConstraint('promotion_id', name='idx_only'),
    )





metadata_obj = MetaData()
metadata_obj.create_all(engine)