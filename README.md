# Address-Auto-Fill

**主要目的用于地址的补全（五级）**

# 1. 用途
- 地址数据标准化阶段，NER结束后可以使用本模块进行地址的补全

# 2. 用法

下载网盘数据，地址`sources`数据放根目录下

把`sources`文件夹和`addr_aito_fill.py`文件移至工作目录，具体用法见`demo.py`。
```python
from addr_auto_fill import AddressAutoFill


auto_fill = AddressAutoFill(addr_std_path="./sources/pcasv.txt",
                            addr_alias_path="./sources/pcasv_alias.txt",
                            pinyin_path="./sources/addr_pinyin.txt")

test_cases = [
    ["江苏", "崇川"],
    ["难京"],
    ["南通南京"],
    ["重慶"]
]

for case in test_cases:
    print("Origin", case)
    ret = auto_fill(*case, debug=True)
    print("Result", ret, "\n")
```

## 2.1. 参数
**AddressAutoFill**
- *text: 输入地址短语
- mode: 默认"exact"，模式有"exact"和"all"两种，第一种返回最相似的标准地址，第二种返回所有可能的地址
- alias: 默认False，表示返回的地址是全称还是缩写
- debug: 默认False，如果为True会印出一些中间过程

# 3. 测试案例
