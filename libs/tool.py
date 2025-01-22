from typing import Mapping,Iterator,Literal,Mapping,Type
import os,sys
import datetime

import pandas
import tomllib
from pydantic import BaseModel,Field
from datetime import datetime, timedelta
from sqlmodel import Session,select,update
from libs import sql_al_chemy

from libs.db import oauth_engine,OauthTable
from libs.oceanengine_sdk.src.oceanengine_sdk_py.oncenengine_sdk_client import OceanengineSdkClient
from libs.oceanengine_sdk.src.oceanengine_sdk_py.db.db_client import DbClient
from libs.format_converter import convert_dict_keys


class FetcherResult(BaseModel):
    total_page :int= 0

    # noinspection PyDataclass
    success_page:list[int]= Field(default_factory=list)
    # noinspection PyDataclass
    data:list[dict]= Field(default_factory=list)
    # noinspection PyDataclass
    error_page:list[int]= Field(default_factory=list)
    success_page_count:int= 0





def find_config_path(
        filename: str = 'pyproject.toml',
        raise_error_if_not_found: bool = False,
        usecwd: bool = False,
) -> str:
    """
    Search in increasingly higher folders for the given file

    Returns path to the file if found, or an empty string otherwise
    """

    def _is_interactive():
        """ Decide whether this is running in a REPL or IPython notebook """
        main = __import__('__main__', None, None, fromlist=['__file__'])
        return not hasattr(main, '__file__')

    if usecwd or _is_interactive() or getattr(sys, 'frozen', False):
        # Should work without __file__, e.g. in REPL or IPython notebook.
        path = os.getcwd()
    else:
        # will work for .py files
        frame = sys._getframe()
        current_file = __file__

        while frame.f_code.co_filename == current_file:
            assert frame.f_back is not None
            frame = frame.f_back
        frame_filename = frame.f_code.co_filename
        path = os.path.dirname(os.path.abspath(frame_filename))

    def _walk_to_root(path: str) -> Iterator[str]:
        """
        Yield directories starting from the given directory up to the root
        """
        if not os.path.exists(path):
            raise IOError('Starting path not found')

        if os.path.isfile(path):
            path = os.path.dirname(path)

        last_dir = None
        current_dir = os.path.abspath(path)
        while last_dir != current_dir:
            yield current_dir
            parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
            last_dir, current_dir = current_dir, parent_dir

    for dirname in _walk_to_root(path):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return check_path

    if raise_error_if_not_found:
        raise IOError('File not found')

    return ''


def save_data_to_csv(data:list[Mapping], file_name):
    """
    将数据保存为csv文件
    :param data: 数据
    :param file_name: 文件名
    :return:None
    """
    df = pandas.DataFrame(data)
    df.to_csv(file_name, index=False, encoding='utf-8_sig')
    print(f'数据保存成功，文件名：{file_name}')

def get_oauth_client(is_update_db:bool=True):
    """
    从数据库读入oauth相关参数，初始化OceanengineSdkClient，然后调用oauth_sign()自动获取最新的access_token

    :param is_update_db:判断是否将更新的token更新到数据库

    :return:oauth oceanengine client
    """

    from sqlalchemy import select


    db_config_toml_path = find_config_path(filename='db_config.toml')
    if not db_config_toml_path:
        raise FileNotFoundError('未找到 db_config.toml 文件')
    with open(db_config_toml_path, 'rb') as f:
        all_db_config = tomllib.load(f)
        oauth_config = all_db_config['oauth']

    with sql_al_chemy.oauth_session as session:
        query_app_id = oauth_config['where_conditions']['appId']
        stmt = (
            select(sql_al_chemy.OauthTable).where(sql_al_chemy.OauthTable.appId == query_app_id)
        )
        oauth_table_data = session.scalars(stmt).one()
        format_oceanengine_param = params_transform(oauth_table_data)
        client = OceanengineSdkClient(format_oceanengine_param)
        new_oauth_token = client.oauth_sign()
        print(f'new_oauth_token:{new_oauth_token}')
        oauth_table_data.accessToken = new_oauth_token['access_token']
        oauth_table_data.refreshToken = new_oauth_token['refresh_token']
        oauth_table_data.expiresTime = new_oauth_token['expires_time']
        oauth_table_data.refreshExpiresTime = new_oauth_token['refresh_expires_time']
        if is_update_db:
            try:
                session.add(oauth_table_data)
                session.commit()
                print(f'更新数据库成功，更新数据：{oauth_table_data.to_dict()}')
            except Exception as e:
                session.rollback()
                raise f'get_oauth_client更新数据库失败，错误信息：{e}'
    return client

def parse_report_data(report_data:FetcherResult)->list[dict]:
    """
    :param report_data:数据报告结果
    :return 由结果dict组成的list
    解析report_data中的data，返回一个由dict组成的list
    """
    if not report_data.data:
        return []
    result = []
    for item in report_data.data:
        temp_dict = {}
        temp_dict.update(item['dimensions'])
        temp_dict.update(item['metrics'])
        result.append(temp_dict)
    return result


def split_date_range(start_date:str,
                     end_date:str,
                     interval:Literal['hourly', 'daily', int])->list[Mapping]:
    """
    将日期区间按需求分割成对应的日期区间dict形成的list。

    :param start_date: 开始日期，格式为 'YYYY-MM-DD'
    :param end_date: 结束日期，格式为 'YYYY-MM-DD'
    :param interval: 分割间隔，可以是 'hourly', 'daily', 或一个整数
    :return: 包含日期区间的dict列表
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    result = []


    if interval == 'daily':
        def next_month(date):
            if date.month == 12:
                return date.replace(year=date.year + 1, month=1, day=1)
            else:
                return date.replace(month=date.month + 1, day=1)

        def get_month_end(date):
            next_m = next_month(date)
            return next_m - timedelta(days=1)

        current = start
        while current < end:
            month_end = get_month_end(current)
            if month_end > end:
                month_end = end
            result.append({'start_date': current.strftime('%Y-%m-%d'), 'end_date': month_end.strftime('%Y-%m-%d')})
            current = next_month(current)
        return  result

    if interval == 'hourly':
        delta = timedelta(days=7)
    elif isinstance(interval, int):
        delta = timedelta(days=interval)
    else:
        raise ValueError("Invalid interval type. Must be 'hourly', 'daily', or an integer.")

    current = start
    while current < end:
        next_interval = current + delta
        if next_interval > end:
            next_interval = end
        result.append({'start_date': current.strftime('%Y-%m-%d'), 'end_date': next_interval.strftime('%Y-%m-%d')})
        current = next_interval+timedelta(days=1)

    return result

def create_oauth_client():
    """
    从数据库读入oauth相关参数，初始化OceanengineSdkClient，然后调用oauth_sign()自动获取最新的access_token与refresh_token.
    并将最新的"accessToken", "refreshToken", "expiresTime", "refreshExpiresTime"更新到oauth数据库中。
    :return:oauthed_oceanengine_client
    """

    db_config_toml_path = find_config_path(filename='db_config.toml')
    if not db_config_toml_path:
        raise FileNotFoundError('未找到 db_config.toml 文件')
    with open(db_config_toml_path, 'rb') as f:
        all_db_config = tomllib.load(f)
        oauth_config = all_db_config['oauth']

    with Session(oauth_engine) as session:
        query_app_id = oauth_config['where_conditions']['appId']
        oauth_table_data: OauthTable = session.exec(select(OauthTable).where(OauthTable.appId == query_app_id)).one()
        client = OceanengineSdkClient(params_transform(oauth_table_data))
        new_oauth_token = client.oauth_sign()
        # new_oauth_token = {'app_id': '1805969627151371', 'secret_key': '0cb84b67505483a617f983e3eaf33434b690baab', 'access_token': 'b5a3436b7f9bfae4e0f56552a8dfbd417d4c8f76', 'refresh_token': '3d00db4b32c603d0c9da3ad92fd5742683ae0863', 'expires_time': datetime.datetime(2025, 1, 8, 21, 23, 44), 'refresh_expires_time': datetime.datetime(2025, 2, 6, 21, 23, 44), 'auth_code': 'e15b25e0db733a81c4a6019d561d3c74ed23a5be', 'user_id': '92403628013', 'user_name': '创想策划汇'}
        print(f'new_oauth_token:{new_oauth_token}')
        oauth_table_data.accessToken = new_oauth_token['access_token']
        oauth_table_data.refreshToken = new_oauth_token['refresh_token']
        oauth_table_data.expiresTime = new_oauth_token['expires_time']
        oauth_table_data.refreshExpiresTime = new_oauth_token['refresh_expires_time']
        session.add(oauth_table_data)
        session.commit()
        session.refresh(oauth_table_data)
        print(f'update_result:{oauth_table_data}')
        return client

def params_transform(params:OauthTable|sql_al_chemy.OauthTable)->Mapping:
    """
    将params转化为对于的形式
    :param params:
    :param trans_type:
    :return:
    """
    result = {
    "app_id" : params.appId,
    "secret_key" : params.secretKey,
    "access_token" : params.accessToken,
    "refresh_token" : params.refreshToken,
    "expires_time" : params.expiresTime,
    "refresh_expires_time" : params.refreshExpiresTime,
    "auth_code" : params.authCode,
    "user_id" : params.userId,
    "user_name" : params.userName,
    }

    return result

def parse_html(item:str,data_id:str,file_name:str = 'table_define.csv'):
    from bs4 import BeautifulSoup
    import pandas as pd
    soup = BeautifulSoup(item['data']['content'], 'html.parser')



    # Find the div with the class 'table-container qz-card-type-block'
    # Find the table with class 'data-table' and data-id 't75ae23f-jVgXbLbE'
    table = soup.find('table', class_='data-table', attrs={'data-id': data_id})


    # # Check if the div was found and print its content
    # if div_container:
    #     print(div_container.prettify())
    # else:
    #     print("Div not found")


    result = []
        
    if table:
        # Find the tbody inside the table
        tbody = table.find('tbody')

        if tbody:
            # Extract rows from tbody
            rows = tbody.find_all('tr')
            
            # Iterate through rows and extract data
            for row in rows:
                # 查找<tr>下的<span>元素，并检查其data-level属性
                span = row.find('span', attrs={'data-level': lambda x: x and int(x) >= 3})
                if span:
                    continue
        
                # Extract table headers (th) or table data (td)
                cells = row.find_all(['th', 'td'])
                # row_data = [cell.get_text(strip=True) for cell in cells ]
                row_data = []
                for cell in cells:
                    if cell.find('span', attrs={'data-type': 'tag'}):
                        cell_span = cell.find_all('span')
                        temp_list = []
                        for temp in cell_span:
                            if temp['data-type'] == 'tag':
                                temp_list.append(temp.get_text(strip=True))
                        temp_text = cell.get_text(strip=True)
                        row_data.append(*[temp_text.replace(tag_str,'') for tag_str in temp_list])

                        # print(f'span cell:{cell_span}')
                        # print(f'value:{[temp.get_text(strip=True) for temp in cell_span if not temp.has_attr('data-type') or temp['data-type'] != 'tag']}')
                        # row_data.append([temp.get_text(strip=True) for temp in cell_span if not temp.has_attr('data-type') or temp['data-type'] != 'tag']) 
                    else:
                        row_data.append(cell.get_text(strip=True))
                result.append(row_data)



                # row_data = []
                # for cell in cells:
                #     cell_span = cell.find_all('span')
                #     if cell_span:
                #         print(f'cell_span:{cell_span}')
                #         row_data.append([cell.get_text(strip=True) for temp in cell_span if temp.find('span', attrs={'data-type': lambda x:x != 'tag'})]) 
                #     else:
                #         print(f'cell_get:{cell}')
                #         row_data.append(cell.get_text(strip=True))
                    
                # result.append(row_data)
                
        else:
            print("Tbody not found inside the table")
    else:
        print("Table not found inside the div")
    df = pd.DataFrame(result[1:],columns=result[0])
    df.to_csv(file_name,index=False,encoding = 'utf-8-sig')

def check_ocean_doc(table:Type[sql_al_chemy.SQL_TABLE_MODEL],return_list:list[dict])->list[dict]:
    """
    检查table和return_list中的keys是否一致
    :param table:
    :param return_list:
    :return: 
    """
    result = []
    table_keys = table.__table__.columns.keys()
    for temp in return_list:
        temp_keys = temp.keys()
        if set(temp_keys) == set(table_keys):
            continue
        key_not_in_table = [key for key in temp_keys if key not in table_keys]
        result.append(
            {
                'key_not_in_tabla':key_not_in_table,
                'value_of_out_key':[{key:(temp[key],type(temp[key]))} for key in key_not_in_table],
                # 'table_keys':table_keys,
                'return_id':{"advertiser_id":temp.get('advertiser_id'),"project_id":temp.get('project_id'),'promotion_id':temp.get('promotion_id')}
            }
        )
    return result
