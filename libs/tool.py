from typing import Mapping,Iterator
import pandas
import os,sys
import tomllib

from libs.oceanengine_sdk.src.oceanengine_sdk_py.oncenengine_sdk_client import OceanengineSdkClient
from libs.oceanengine_sdk.src.oceanengine_sdk_py.db.db_client import DbClient
from libs.format_converter import convert_dict_keys



def find_toml_file(
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

def get_oauth_client_and_update_token():
    """
    从数据库读入oauth相关参数，初始化OceanengineSdkClient，然后调用oauth_sign()自动获取最新的access_token与refresh_token.
    并将最新的"accessToken", "refreshToken", "expiresTime", "refreshExpiresTime"更新到oauth数据库中。
    :return:oauthed_oceanengine_client
    """

    db_config_toml_path = find_toml_file(filename='db_config.toml')
    if not db_config_toml_path:
        raise FileNotFoundError('未找到 db_config.toml 文件')
    with open(db_config_toml_path, 'rb') as f:
        all_db_config = tomllib.load(f)
        oauth_config = all_db_config['oauth']

    db_client = DbClient(oauth_config['oauth_data_db'])
    oceanengine_param = db_client.select(f'select * from {oauth_config['oauth_data_table']} where {oauth_config['oauth_data_flag_column_name']} = "{oauth_config['oauth_data_column_value_uid']}"')
    format_oceanengine_param = convert_dict_keys(oceanengine_param[0], 'snake')
    client = OceanengineSdkClient(format_oceanengine_param)
    new_oauth_token = client.oauth_sign()
    print(f'new_oauth_token:{new_oauth_token}')
    format_oauth_token = convert_dict_keys(new_oauth_token, 'small_camel')
    print(format_oauth_token)
    update_sql, update_data = db_client.generate_sql(
        table_name=oauth_config['oauth_data_table'],
        operation="update",
        columns=["accessToken", "refreshToken", "expiresTime", "refreshExpiresTime"],
        data=format_oauth_token,
        conditions=f'{oauth_config["oauth_data_flag_column_name"]} = "{oauth_config["oauth_data_column_value_uid"]}"'
    )
    print(f'sql:{update_sql},data:{update_data}')
    update_result = db_client.update(update_sql, update_data)
    print(f'update_result:{update_result}')
    return client