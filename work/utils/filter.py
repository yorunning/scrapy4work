from os import path
import re


def filter_category(category, *disallow_category_list):
    """
    分类过滤器
    :param category: 要判断的分类
    :param disallow_category_list: 要过滤的分类列表
    :return: 不要的分类，返回True
    """

    # disallow_category_list = disallow_category_list

    if category in disallow_category_list:
        return True
    return False


def filter_brand(brand):
    """
    违禁品过滤器
    :param brand: 要判断的品牌
    :return: 如果是违禁品，返回True
    """

    disallow_brand_file = path.join(path.abspath('./work/resource'), 'disallow_brand.txt')
    with open(disallow_brand_file, 'r') as f:
        disallow_brand_list = [line.strip() for line in f]

    for disallow_brand in disallow_brand_list:
        if re.match(brand, disallow_brand, flags=re.I):
            return True
    return False
