from addr_auto_fill import AddressAlias

with open("../sources/pcasv_alias.txt") as f:
    for i in f.readlines():
        l = i.strip().split(",")
        try:
            assert AddressAlias.alias(*l) == l
        except:
            print(l, AddressAlias.alias(*l))