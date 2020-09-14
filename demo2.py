from addr_auto_fill import AddressAutoFill

auto_fill = AddressAutoFill(addr_std_path="./sources/pcasv.txt",
                            addr_alias_path="./sources/pcasv_alias.txt",
                            pinyin_path="./sources/addr_pinyin.txt")

test_cases = [
    # 错位，补全
    ["河南省", "商丘"],
    ["江苏", "崇川"],  # ['江苏省', '南通市', '崇川区', '', '']
    ['', '鹿泉', '', '铜冶'],  # ['河北省', '石家庄市', '鹿泉区', '铜冶镇', '']
    ['北京', '东华门', '', ''],  # ['北京市', '北京市', '东城区', '东华门街道', '']

    # 错字， 多写了字
    ['长沙', '咸', '湖南'],  # ['湖南省', '长沙市', '', '', '']
    ['长沙啊啊', '湖南'],  # ['湖南省', '长沙市', '', '', '']

    # 错别字
    ["难京"],  # ['江苏省', '南京市', '', '', '']
    ['内蒙古', '爆头', '土默特右旗', ''],  # ['内蒙古自治区', '包头市', '土默特右旗', '', '']

    # 繁体字
    ["重慶"],  # ['重庆市', '重庆市', '', '', '']

    # 平级冲突，
    ["南通南京"],  # ['江苏省', '', '', '', '']

    # 多个结果，
    ['', '', '朝阳区', ''],  # ['', '', '朝阳区', '', '']
]

for case in test_cases:
    ret = auto_fill(*case, debug=True)
    print("Result", ret, "\n")