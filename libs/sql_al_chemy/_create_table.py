import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from typing import Type
# from libs.sql_al_chemy import SQL_TABLE_MODEL
from datetime import datetime

csv_file = "e:/github_code_lib/ad_report_fetcher/table.csv"
df = pd.read_csv(csv_file)

def create_table(class_name:str,table_name:str):
    print(f'class {class_name}(Base):')
    print(f'    __tablename__ = "{table_name}"')
    print(f'    primary_key:Mapped[int] = Column(Integer, primary_key=True, autoincrement=True,default=None,nullable=False )')
    for index, row in df.iterrows():
        field_name = row['字段']
        field_type = row['类型'].lower()

        if field_type == 'number':
            column_type = 'Integer'
        elif field_type == 'string':
            column_type = 'String'
        elif field_type == 'float':
            column_type = 'Float'
        elif field_type == 'bool':
            column_type = 'Boolean'
        elif field_type == 'json':
            column_type = 'JSON'
        elif field_type == 'object[]':
            column_type = 'JSON'
        elif field_type == 'datetime':
            column_type = 'DateTime'
        else:
            column_type = 'String'

        
        if field_type == 'number':
            python_type = 'int'
        elif field_type == 'string':
            python_type = 'str'
        elif field_type == 'float':
            python_type = 'float'
        elif field_type == 'bool':
            python_type = 'bool'
        elif field_type == 'json':
            python_type = 'dict'
        elif field_type == 'object[]':
            python_type = 'dict'
        elif field_type == 'datetime':
            python_type = 'datetime.datetime'
        else:
            python_type = 'str'

        if column_type == 'String':    
            print(f'    {field_name}:Mapped[{python_type}] = mapped_column({column_type}(64, collation="utf8mb4_0900_ai_ci"), nullable=True, default="")')
        elif column_type == 'DateTime':
            print(f'    {field_name}:Mapped[{python_type}] = mapped_column({column_type}, nullable=True, default=None)')
        elif column_type == 'Float':
            print(f'    {field_name}:Mapped[{python_type}] = mapped_column(DECIMAL(precision=10, scale=2), nullable=True, default=0)')
        elif column_type == 'JSON':
            print(f'    {field_name}:Mapped[{python_type}] = mapped_column({column_type}, nullable=True, default=None)')
        elif column_type == 'Boolean':
            print(f'    {field_name}:Mapped[{python_type}] = mapped_column({column_type}, nullable=True, default=None)')
        else:
            print(f'    {field_name}:Mapped[{python_type}] = mapped_column({column_type}, nullable=True, default="")')


# engine = create_engine('sqlite:///ad_report.db', echo=True)
# Base.metadata.create_all(engine)

# # 获取类的属性和方法
# class_attrs = dir(AdReport)
# class_dict = AdReport.__dict__

# # 构建类的字符串表示
# class_str = f"class {AdReport.__name__}:\n"
# for attr in class_attrs:
#     if not attr.startswith('__'):
#         class_str += f"    {attr} = {getattr(AdReport, attr)}\n"

# print(class_str)
create_table('AdReport','ad_report')