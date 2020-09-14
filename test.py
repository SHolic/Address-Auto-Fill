from addr_auto_fill import AddressAutoFill

auto_fill = AddressAutoFill(addr_std_path="./sources/pcasv.txt",
                            addr_alias_path="./sources/pcasv_alias.txt",
                            pinyin_path="./sources/addr_pinyin.txt")


print(auto_fill.mapping)