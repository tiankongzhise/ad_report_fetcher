from typing import Type
from sqlalchemy.orm import Session
from sqlalchemy import UniqueConstraint,and_,or_,select
from .type import SQL_TABLE_MODEL

class CURD(object):
    @staticmethod
    def insert_ignore(data: list[dict],
                                table: Type[SQL_TABLE_MODEL],
                                session: Session) -> dict:
        """
        :param data: 需要插入的数据
        :param table: 使用sqlalchemyV2定义的表模型
        :param session: 已经链接到对应数据库的Session
        :return: 插入的结果，包含插入，忽略，以及被忽略的是哪些
        """

        try:
            with session:
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
                # 处理没有唯一约束的情况
                if unique_columns == []:
                    unique_columns = table.__table__.primary_key.colums.keys()
                set1 = set(unique_columns)
                set2 = set(data[0].keys())

                if set2.issuperset(set1):
                    query_params = {}
                    for col in unique_columns:
                        query_params.update({col: [item[col] for item in data]})
                    conditions = and_(getattr(table, col).in_(query_params[col]) for col in unique_columns)
                    existing_db_records = session.scalars(select(table).filter(or_(conditions))).all()
                else:
                    existing_db_records = []

                # 创建已存在记录的(project_id, advertiser_id)集合用于快速查找
                existing_keys = [
                    tuple(str(getattr(record, col)) for col in unique_columns)
                    for record in existing_db_records
                ]

                # 过滤出需要插入的新记录
                new_records = [
                    obj for obj in orm_objects
                    if tuple(str(getattr(obj, col)) for col in unique_columns) not in existing_keys
                ]

                # 批量插入新记录
                if new_records:
                    session.add_all(new_records)
                    session.commit()

                # 统计结果
                total_records = len(orm_objects)
                ignored_records = len(existing_db_records)
                inserted_records = len(new_records)

                # 创建已存在记录的(project_id, advertiser_id)集合用于快速查找
                ignore_keys = [
                    tuple({col: str(getattr(record, col))} for col in unique_columns)
                    for record in existing_db_records
                ]

            return {
                'total_records': total_records,
                'ignored_records': ignored_records,
                'inserted_records': inserted_records,
                'existing_db_records': ignore_keys
            }


        except Exception as e:
            session.rollback()
            print(f"发生错误: {e}")
            raise e

