# -*- coding: utf-8 -*-
"""地名多语言显示 / 罗马化（拼音）工具。

目标：让省/市/区县/乡镇/街道在不同语言下显示「外文名（中文）」，
便于搜索引擎收录、外国用户搜索到。中文界面仍只显示中文，保持原样。
- 省级行政区：尽量使用通用英文名（如 Beijing / Shanghai / Guangdong）。
- 其它层级（市/区/县/乡镇/街道）：使用拼音罗马化（如 Guang Zhou / Tian He），
  并去掉省/市/区/县/镇/乡/街道等行政后缀，更贴近真实检索词。
"""
from pypinyin import pinyin, Style

# 省级行政区通用英文名（覆盖数据中出现及常见的 34 个）
PROVINCE_EN = {
    "北京市": "Beijing",
    "天津市": "Tianjin",
    "上海市": "Shanghai",
    "重庆市": "Chongqing",
    "河北省": "Hebei",
    "山西省": "Shanxi",
    "内蒙古自治区": "Inner Mongolia",
    "辽宁省": "Liaoning",
    "吉林省": "Jilin",
    "黑龙江省": "Heilongjiang",
    "江苏省": "Jiangsu",
    "浙江省": "Zhejiang",
    "安徽省": "Anhui",
    "福建省": "Fujian",
    "江西省": "Jiangxi",
    "山东省": "Shandong",
    "河南省": "Henan",
    "湖北省": "Hubei",
    "湖南省": "Hunan",
    "广东省": "Guangdong",
    "广西壮族自治区": "Guangxi",
    "海南省": "Hainan",
    "四川省": "Sichuan",
    "贵州省": "Guizhou",
    "云南省": "Yunnan",
    "西藏自治区": "Tibet",
    "陕西省": "Shaanxi",
    "甘肃省": "Gansu",
    "青海省": "Qinghai",
    "宁夏回族自治区": "Ningxia",
    "新疆维吾尔自治区": "Xinjiang",
    "台湾省": "Taiwan",
    "香港特别行政区": "Hong Kong",
    "澳门特别行政区": "Macau",
}

# 需要在拼音展示时去掉的行政后缀（长优先，避免误截）
_SUFFIXES = ["自治区", "特别行政区", "自治州", "市辖区", "街道办事处",
             "街道", "地区", "盟", "市", "区", "县", "镇", "乡"]

_PINYIN_CACHE = {}


def _to_pinyin(text):
    """把中文转成首字母大写的拼音，如 '广州市' -> 'Guang Zhou Shi'。带缓存。"""
    if text in _PINYIN_CACHE:
        return _PINYIN_CACHE[text]
    syls = pinyin(text, style=Style.NORMAL, heteronym=False)
    py = " ".join(s[0] for s in syls).title()
    _PINYIN_CACHE[text] = py
    return py


def _strip_suffix(name):
    """去掉末尾的行政后缀，返回（去后缀名, 是否改动）。"""
    for suf in _SUFFIXES:
        if name.endswith(suf) and len(name) > len(suf):
            return name[:-len(suf)], True
    return name, False


def romanize(name):
    """返回地名的罗马化（拼音）形式，去掉行政后缀，如 '广州市' -> 'Guang Zhou'。"""
    base, _changed = _strip_suffix(name)
    return _to_pinyin(base)


def display_name(name, lang):
    """用于页面展示：中文语言返回原名；其它语言返回 '外文（中文）'。"""
    if lang in ("zh-CN", "zh-TW"):
        return name
    en = PROVINCE_EN.get(name)
    if en:
        return "%s (%s)" % (en, name)
    return "%s (%s)" % (romanize(name), name)


def title_name(name, lang):
    """用于 <title>/面包屑纯文本：中文返回原名；其它语言返回外文/拼音（不含中文）。"""
    if lang in ("zh-CN", "zh-TW"):
        return name
    return PROVINCE_EN.get(name) or romanize(name)
