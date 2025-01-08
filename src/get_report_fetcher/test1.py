# -*- coding: utf-8 -*-
import os
import pandas as pd
from pandas.tseries.holiday import after_nearest_workday


def find_files_with_dimensions(folder_path,file_tag):
    """
    返回指定文件夹下全部包含 'dimensions' 的文件名列表。

    :param folder_path: 文件夹路径
    :return: 包含 'dimensions' 的文件名列表
    """
    files_with_dimensions = []

    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"文件夹路径 {folder_path} 不存在")
        return files_with_dimensions

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 只处理文件
        if os.path.isfile(file_path):
            try:
                if file_tag in filename:
                    files_with_dimensions.append({"filename":filename.replace(f'_{file_tag}.csv',""),
                    "file_path":file_path})
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")

    return files_with_dimensions

def get_file_data(file_path):
    df = pd.read_csv(file_path)
    return df

def compare_df_column(df1, df2, column='field'):
    """
    比较两个 DataFrame 中指定列的不同值。

    :param df1: 第一个 DataFrame
    :param df2: 第二个 DataFrame
    :param field: 要比较的列名
    :return: 不同值的集合
    """
    set1 = set(df1[column]) if column in df1.columns else set()
    set2 = set(df2[column]) if column in df2.columns else set()
    union_field = set1 & set2
    differences_in_df1 = set1 -set2
    differences_in_df2 = set2 - set1
    return union_field,differences_in_df1,differences_in_df2

# 示例调用
if __name__ == '__main__':
    folder_path = 'data'
    file_tag = 'metrics'
    result = find_files_with_dimensions(folder_path,file_tag)
    print(f"包含 '{file_tag}' 的文件: {result}")
    std_df = pd.DataFrame()
    compare_df_list = []
    for item in result:
        if item["filename"] == "BASIC_DATA":
            std_df = get_file_data(item["file_path"])
        else:
            compare_df_list.append({"filename":item["filename"],'df':get_file_data(item["file_path"])})

    common_field_list = []
    for item in compare_df_list:
        union_field,differences_in_df1,differences_in_df2 = compare_df_column(std_df, item['df'])
        print(f"{item['filename']}和BASIC_DATA中都存在的字段：{union_field}")
        print(f"{item['filename']}中存在BASIC_DATA中不存在的字段：{differences_in_df2}")
        print(f"{item['filename']}中不存在BASIC_DATA中存在的字段：{differences_in_df1}")
        if item["filename"] == "VIDEO_DUARATION_DATA":
            continue
        common_field_list.append(union_field)

    common_set = set()
    first_set = set()
    sec_set = set()
    for item in common_field_list:
        print(f"{item}")
        if item:
            if first_set == set():
                first_set = item
                continue
            elif sec_set == set():
                sec_set = item
                common_set = first_set & sec_set
                if common_set == set():
                    print('不存在公共字段')
                    break
            else:
                # pre_common_set_tag = len(common_set)
                common_set = common_set & item
                # if common_set == set():
                #     print(f'pre_common_set_tag:{pre_common_set_tag}')
                #     print(item)

    print(f'common_set:{common_set}')

