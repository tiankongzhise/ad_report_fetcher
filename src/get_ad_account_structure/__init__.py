import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import UniqueConstraint,and_,or_,select


from get_project_list import FeatchProjectList
from get_promotion_list import FeatchPromotionList
from libs.tool import get_oauth_client
from libs import sql_al_chemy


class GetAdAccountStructure(object):
    def __init__(self,cc_account_id : str|int):
        self.oceanengine_client = get_oauth_client()
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
    def fetch(self):
        result = {
            'project_list':[],
            'promotion_list':[]
        }
        self.get_advertiser_list()
        for advertiser_id in self.advertiser_list:
            result['project_list'].extend(FeatchProjectList(self.oceanengine_client).fetch(advertiser_id))
            result['promotion_list'].extend(FeatchPromotionList(self.oceanengine_client).fetch(advertiser_id))
        return result

def insert_data_to_database(data:list[dict],
                            table:sql_al_chemy.OceanAdProjectListTable|sql_al_chemy.OceanAdPromotionListTable,
                            session:Session)->dict:
    with session:
        try:
            # 将原始数据转换为ORM对象列表
            orm_objects = [
                table(**project)
                for project in data
            ]
            # 获取唯一约束中的列名
            unique_columns = []
            if hasattr(table, '__table_args__'):
                for constraint in table.__table_args__:
                    if isinstance(constraint, UniqueConstraint):
                        unique_columns = constraint.columns.keys()
                        break
            #处理没有唯一约束的情况
            if unique_columns is None:
                unique_columns = table.__table__.primary_key.colums.keys()


            # 构建批量查询条件
            conditions = [
                (and_(getattr(table, col) == obj[col]) for col in unique_columns)
                for obj in orm_objects
            ]
            # 一次性查询所有已存在的记录
            stmt = select(table).where(
                or_(*conditions)
            )
            existing_db_records = session.scalars(stmt).all()

            # 创建已存在记录的(project_id, advertiser_id)集合用于快速查找
            existing_keys = {
                (str(getattr(existing_db_records, col)) for col in unique_columns)
                for record in existing_db_records
            }

            # 过滤出需要插入的新记录
            new_records = [
                obj for obj in orm_objects
                if (str(getattr(existing_db_records, col)) for col in unique_columns) not in existing_keys
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




if __name__ == '__main__':
    item = GetAdAccountStructure()
    result = item.fetch()
    print(result)
