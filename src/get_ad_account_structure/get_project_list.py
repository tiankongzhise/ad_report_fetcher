import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from libs.oceanengine_sdk.src.oceanengine_sdk_py import OceanengineSdkClient




class FeatchProjectList(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, ocean_client:OceanengineSdkClient):
        self.oceanengine_client = ocean_client

    def fetch(self, advertiser_id: str | int):
        result = []
        page = 1
        rsp = self.fetch_project_list(advertiser_id, page)
        if rsp['code'] != 0:
            raise Exception(f'FeatchProjectList fetch error,rsp:{rsp}')
        result.extend(rsp['data']['list'])
        while rsp['data']['page_info']['page'] < rsp['data']['page_info']['total_page']:
            page = rsp['data']['page_info']['page'] + 1
            rsp = self.fetch_project_list(advertiser_id, page)
            if rsp['code'] != 0:
                raise Exception(f'FeatchProjectList fetch error,rsp:{rsp}')
            result.extend(rsp['data']['list'])
        return result

    def fetch_project_list(self, advertiser_id: str | int, page:int=1):
        query={
            "advertiser_id": advertiser_id,
            "fields": [],
            "page": page,
            "page_size": 100
        }
        rsp = self.oceanengine_client.v3___0_project_list(params=query)
        return rsp


if __name__ == '__main__':

    from libs.tool import create_oauth_client
    from sqlalchemy import select,or_
    from libs import sql_al_chemy
    ocean_client = create_oauth_client()
    fetcher = FeatchProjectList(ocean_client)
    promotion_list = fetcher.fetch(advertiser_id=1802432784180266)
    with sql_al_chemy.ocean_session as session:
        try:
            # 将原始数据转换为ORM对象列表
            orm_objects = [
                sql_al_chemy.OceanAdProjectListTable(**project)
                for project in promotion_list
            ]
            
            # 查询已存在的记录
            # 构建批量查询条件
            conditions = [
                (sql_al_chemy.OceanAdProjectListTable.project_id == obj.project_id) & 
                (sql_al_chemy.OceanAdProjectListTable.advertiser_id == obj.advertiser_id)
                for obj in orm_objects
            ]
            # 一次性查询所有已存在的记录
            stmt = select(sql_al_chemy.OceanAdProjectListTable).where(
                or_(*conditions)
            )
            result = session.execute(stmt)
            existing_db_records = result.scalars().all()

            # 创建已存在记录的(project_id, advertiser_id)集合用于快速查找
            existing_keys = {
                (str(record.project_id), str(record.advertiser_id)) 
                for record in existing_db_records
            }
            
            # 过滤出需要插入的新记录
            new_records = [
                obj for obj in orm_objects 
                if (str(obj.project_id), str(obj.advertiser_id)) not in existing_keys
            ]
            
            
            # 批量插入新记录
            if new_records:
                session.add_all(new_records)
                session.commit()
            
            # 统计结果
            total_records = len(orm_objects)
            ignored_records = len(existing_db_records)
            inserted_records = len(new_records)
            
            print(f"总数据量: {total_records}")
            print(f"成功插入: {inserted_records}")
            print(f"重复忽略: {ignored_records}")
            print("\n被忽略的记录:")
            for record in existing_db_records:
                print(f"项目ID: {record.project_id}, 广告主ID: {record.advertiser_id}, 项目名称: {record.name}")

        except Exception as e:
            session.rollback()
            print(f"发生错误: {e}")
            raise e


