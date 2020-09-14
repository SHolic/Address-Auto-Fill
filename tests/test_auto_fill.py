from addr_auto_fill import AddressAutoFill


def test_fill(auto_fill, test_case, answer, **kwargs):
    assert auto_fill(*test_case, **kwargs) == answer


if __name__ == "__main__":
    auto_fill_instance = AddressAutoFill(addr_std_path="../sources/pcasv.txt",
                                         addr_alias_path="../sources/pcasv_alias.txt",
                                         pinyin_path="../sources/addr_pinyin.txt")
    test_cases = [
        # 错位，补全
        ["江苏", "崇川"],  # ['江苏省', '南通市', '崇川区', '', '']
        ['', '鹿泉', '', '铜冶'],  # ['河北省', '石家庄市', '鹿泉区', '铜冶镇', '']
        ['北京', '东华门', '', ''],  # ['北京市', '北京市', '东城区', '东华门街道', '']

        #     # 错字， 多写了字
        #     ['长沙', '咸', '湖南'],  # ['湖南省', '长沙市', '', '', '']
        #     ['长沙啊啊', '湖南'],  # ['湖南省', '长沙市', '', '', '']
        #
        #     # 错别字
        #     ["难京"],  # ['江苏省', '南京市', '', '', '']
        #     ['内蒙古', '爆头', '土默特右旗', ''],  # ['内蒙古自治区', '包头市', '土默特右旗', '', '']
        #
        #     # 繁体字
        #     ["重慶"],  # ['重庆市', '重庆市', '', '', '']
        #
        #     # 平级冲突，
        #     ["南通南京"],  # ['江苏省', '', '', '', '']
        #
        #     # 多个结果，
        #     ['', '', '朝阳区', ''],  # ['', '', '朝阳区', '', '']
        #
        #     # 后缀错误
        #     ['江苏省', '南京市', '', '永阳镇', '东山村'],  # ['江苏省', '南京市', '溧水区', '永阳街道', '东山村委会']
        #
        #     # 异级冲突，填写完整的地址氪信度越高，且越相信地址级别大的
        #     ['广东', '东莞', '三角'],  # ['广东省', '东莞市', '', '', '']
        #     ['广东', '东莞', '三角镇'],  # ['广东省', '', '', '三角镇', '']
        #     ['广东', '东莞市', '三角镇'],  # ['广东省', '东莞市', '', '', '']
        #     ['重庆', '西区', '江津', '双福'],   # ['重庆市', '重庆市', '江津区', '双福街道', '']
        #     ['', '涟源', '涟源', '金石镇'],  # ['湖南省', '娄底市', '涟源市', '金石镇', '']
        #
        #     # 一个地址包含多条信息
        #     ['', '', '上海长宁', ''],  # ['上海市', '上海市', '长宁区', '', '']
        #     ['浙江省', '杭州市,拉萨市', '西湖区', ''],  # ['浙江省', '杭州市', '西湖区', '', '']
        #     ['', '浩特市', '内蒙古呼和,新城区', ''],  # ['内蒙古自治区', '呼和浩特市', '新城区', '', '']
        #     ['西藏', '乌鲁木齐市,拉萨市', '新疆,天山区,堆龙德庆县', ''],  # ['新疆维吾尔自治区', '乌鲁木齐市', '天山区', '', '']
        #     ['吉林', '长春', '南关区,通榆县', '包拉温都乡'],  # ['吉林省', '白城市', '通榆县', '包拉温都蒙古族乡', '']
        #     ["南山区航天科技广场"],  # ['', '', '南山区', '', '']
        #     ["顺河乡", "吕庄村"],
        #     ["杭州市", "顺河乡", "吕庄村"],
        #     ["城北村"]
    ]
    answers = [
        ['江苏省', '南通市', '崇川区', '', ''],
        ['河北省', '石家庄市', '鹿泉区', '铜冶镇', ''],
        ['北京市', '北京市', '东城区', '东华门街道', '']
    ]

    for t, a in zip(test_cases, answers):
        test_fill(auto_fill=auto_fill_instance,
                  test_case=t,
                  answer=a)
