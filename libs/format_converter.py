import re
def camel_to_snake(key):
    """
    将驼峰命名法的字符串转换为下划线命名法。

    :param key: 驼峰命名法的字符串
    :return: 下划线命名法的字符串
    """
    # 使用正则表达式将驼峰命名法转换为下划线命名法
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_small_camel(snake_str):
    """
    将下划线命名法的字符串转换为驼峰命名法。

    :param snake_str: 下划线命名法的字符串
    :return: 驼峰命名法的字符串
    """
    components = snake_str.split('_')
    # 将第一个组件保持原样，其余组件首字母大写，然后连接起来
    return components[0] + ''.join(x.capitalize() or '_' for x in components[1:])


def snake_to_big_camel(snake_str):
    """
    将下划线命名法的字符串转换为驼峰命名法。

    :param snake_str: 下划线命名法的字符串
    :return: 驼峰命名法的字符串
    """
    components = snake_str.split('_')
    # 将每个组件的首字母大写，然后连接起来
    return ''.join(x.capitalize() or '_' for x in components)


def convert_dict_keys(d, conventions):
    """
    将字典的键从驼峰命名法转换为下划线命名法。

    :param d: 输入的字典
    :return: 转换后的字典
    """
    if conventions == 'snake':
        return {camel_to_snake(k): v for k, v in d.items()}
    if conventions == 'small_camel':
        return {snake_to_small_camel(k): v for k, v in d.items()}
    if conventions == 'big_camel':
        return {snake_to_big_camel(k): v for k, v in d.items()}