import time
import re
import copy
from pypinyin import lazy_pinyin


class AddressAlias:
    """
    去除地址后缀，如"上海市"->"上海"
    """

    @staticmethod
    def __check_rank_area(x):
        ret = re.search("第[一|二|三|四|五|六|七|八|九|十]", x)
        if ret is None:
            return False
        return True

    @staticmethod
    def __rstrip_autonomous_terms(x):
        __autonomous_terms = {'汉族', '蒙古族', '回族', '藏族', '维吾尔族', '苗族', '彝族', '壮族', '布依族', '朝鲜族', '满族', '侗族', '瑶族', '白族',
                              '土家族', '哈尼族', '哈萨克族', '傣族', '黎族', '傈僳族', '佤族', '畲族', '拉祜族', '水族', '东乡族', '纳西族', '景颇族',
                              '柯尔克孜族', '土族', '达斡尔族', '仫佬族', '羌族', '布朗族', '撒拉族', '毛南族', '仡佬族', '锡伯族', '阿昌族', '普米族',
                              '塔吉克族', '怒族', '乌孜别克族', '俄罗斯族', '鄂温克族', '德昂族', '保安族', '裕固族', '京族', '塔塔尔族', '独龙族', '鄂伦春族',
                              '赫哲族', '门巴族', '珞巴族', '基诺族', '高山族'}
        while True:
            done = True
            for i in range(len(x) - 2, 1, -1):
                if x[-i:] in __autonomous_terms or x[-i:] + '族' in __autonomous_terms:
                    x = x[:-i]
                    done = False
                    break
            if done: break
        return x

    @staticmethod
    def __rstrip_cun(text):
        if text[-1] == "村":
            for i in range(len(text) - 1, -1, -1):
                if text[i] != "村":
                    return text[:i + 2]
        return text

    @classmethod
    def province(cls, text):
        if not isinstance(text, str) or not text:
            return ""
        text = text.strip()
        if text.endswith('自治区'):
            return cls.__rstrip_autonomous_terms(text[:-3])
        province = re.sub("特别行政区$|省$|市$", "", text)
        return province

    @classmethod
    def city(cls, text):
        if not isinstance(text, str) or not text:
            return ""
        text = text.strip()
        if len(text) <= 2:
            return text
        if text[-3:] in ('自治州', '自治县'):
            return cls.__rstrip_autonomous_terms(text[:-3])
        if text[-2:] in ('地区', '林区'):
            return text[:-2]
        if text[-1] in ('市', '县', '盟'):
            return text[:-1]
        return text

    @classmethod
    def county(cls, text):
        if not isinstance(text, str) or not text:
            return ""
        text = text.strip()
        if len(text) <= 2:
            return text
        if len(text) > 4 and text[-3:] in ('自治州', '自治县', '自治旗'):
            return cls.__rstrip_autonomous_terms(text[:-3])
        if len(text) > 3 and text[-2:] in ('特区', '新区', '矿区', '前旗', '后旗', '左旗', '右旗', '中旗', '湖区'):
            return text[:-2]
        if len(text) > 2 and text[-1] in ('市', '县'):
            return text[:-1]
        if len(text) <= 5 and text[-1] == '区' and text[-3:] != "示范区":
            return cls.__rstrip_autonomous_terms(text[:-1])
        if text[-1] == '旗':
            return text[:-1]
        return text

    @classmethod
    def town(cls, text):
        if not isinstance(text, str) or not text:
            return ""
        text = text.strip()
        if len(text) <= 2:
            return text
        if len(text) > 13 and text[-12:] in ('保护开发区池北区特殊乡镇'):
            return text[:-12]
        if len(text) > 10 and text[-9:] in ('经济开发区特殊乡镇'):
            return text[:-9]
        if len(text) > 8 and text[-7:] in ('街道管理办公室'):
            return text[:-7]
        if len(text) > 7 and text[-6:] in ('实验农场地区'):
            return text[:-6]
        if len(text) > 6 and text[-5:] in ('街道办事处', '办事处街道', '农场办事处', "新区办事处"):
            return text[:-5]
        if len(text) > 5 and text[-4:] in ('矿区街道', "办事处乡", "林场地区", "街道地区", "新区街道", "水库地区"):
            return text[:-4]
        if len(text) > 4 and text[-3:] in ('办事处', '镇街道', "乡街道"):
            return text[:-3]
        if len(text) > 3 and text[-2:] in ('街道', '林场', '渔场', '牧场', '农场', '茶场', '新区', '地区', '矿区', '水库', '特区', '茶厂',
                                           '煤矿', '镇乡', '乡镇'):
            return text[:-2]
        if text[-1:] in ['镇', '乡']:
            return cls.__rstrip_autonomous_terms(text[:-1])
        return text

    @classmethod
    def community(cls, text):
        if not isinstance(text, str) or not text:
            return ""
        text = text.strip()
        if len(text) <= 2:
            return text
        if cls.__check_rank_area(text):
            return text
        if len(text) > 15 and text[-14:] in ("社区居委会筹备组和社区工作站", "社区居委会筹备组及社区工作站",
                                             "生态旅游管理委员会虚拟生活区"):
            return text[:-14]
        if len(text) > 14 and text[-13:] in ("新型工业园区管理委员会社区", "开发区管理委员会虚拟生活区"):
            return text[:-13]
        if len(text) > 12 and text[-11:] in ("煤炭产业园区管委会社区"):
            return text[:-11]
        if len(text) > 11 and text[-10:] in ("社区指导委员会生活区", "经济开发区管委会社区", "林场村委会虚拟生活区",
                                             "村民委员会虚拟生活区", "示范园区管理区委员会", "管理委员会虚拟生活区"):
            return text[:-10]
        if len(text) > 9 and text[-8:] in ("社区居委会筹备组", "煤矿生活区居委会", "家属委员会居委会", "管理区居民委员会",
                                           "村委会虚拟生活区", "居委会虚拟生活区", "管委会虚拟生活区", "生活区社区居委会",
                                           "村民委员会生活区", "生活区居民委员会"):
            return text[:-8]
        if len(text) > 8 and text[-7:] in ("社区居民委员会", "村委会虚拟社区", "社区村民委员会", "社区社区居委会",
                                           "林场社区生活区", "农场地区居委会", "渔民委员会社区", "嘎查虚拟生活区",
                                           "管理委员会社区", "居民委员会社区", "社区虚拟生活区", "类似居委会社区",
                                           "社区居委委员会"):
            return text[:-7]
        if len(text) > 7 and text[-6:] in ("社区服务中心", "社区居民委员", "村民委员会委", "管理区生活区",
                                           "社区村民委会", "管委会管理区"):
            if text[-6] == "村":
                return cls.__rstrip_cun(text[:-5])
            return cls.__rstrip_cun(text[:-6])
        if len(text) > 6 and text[-5:] in ("社区居委会", "村民委员会", "虚拟生活区", "牧民委员会", "居民委员会", "社区委员会", "林场生活区", "农场生活区",
                                           "牧场生活区", "林场生活区", "林场管理区", "管区生活区", "村委委员会", "社区居季会", "社区居民会", "村民委员会",
                                           "社区村委会", "嘎查委员会", "管理区社区", "村委会社区", "委会生活区", "新区办事处", "社区生活区", "管委会社区",
                                           "社区管委会", "新区办事处", "生活区社区", "村民委员会"):
            if text[-5] == "村":
                return cls.__rstrip_cun(text[:-4])
            return cls.__rstrip_cun(text[:-5])
        if len(text) > 5 and text[-4:] in ("村委员会", "村民小组", "社区居委", "村民委会", "村民员会", "社区委会",
                                           "嘎查委会", "嘎查社区", "农场地区"):
            if len(text) > 7 and text[-6:-4] == "直辖":
                return text[:-6]
            if text[-4] == "村":
                return cls.__rstrip_cun(text[:-3])
            return cls.__rstrip_cun(text[:-4])
        if len(text) > 4 and text[-3:] in ("村委会", "居委会", "社区村", "牧委会", "生活区",
                                           "委员会", "生产队", "管理区", "委会员", "管委会"):
            if text[-3] == "村":
                return cls.__rstrip_cun(text[:-2])
            return cls.__rstrip_cun(text[:-3])
        if len(text) > 3 and text[-2:] in ("社区", "委会", "嘎查", "村会", "村委"):
            if text[-2] == "村":
                return cls.__rstrip_cun(text[:-1])
            return cls.__rstrip_cun(text[:-2])
        if text[-1:] in ["村"]:
            alias = cls.__rstrip_autonomous_terms(text[:-1])
            if alias == text[:-1]:
                return alias
        return text

    @classmethod
    def alias(cls, prv, cty, cnty, twn, cmnt):
        return [
            cls.province(prv),
            cls.city(cty),
            cls.county(cnty),
            cls.town(twn),
            cls.community(cmnt)
        ]


class AddressTextModifier:
    """
    标准化地址输入：
        文本提取：上海上海 -> 上海
        错别字：伤海 -> 上海
        漏字：呼和浩 -> 呼和浩特 (FIXME：暂未实现)
        繁体字：重慶 -> 重庆
    """

    def __init__(self, addr_std_path, addr_alias_path, addr_pinyin=None):
        self.addr_dict = self.__init_addr_dict(addr_std_path, addr_alias_path)
        self.pinyin = self.__init_pinyin(addr_pinyin) if addr_pinyin else None

    @staticmethod
    def __init_addr_dict(addr_std_path, addr_alias_path):
        lines = open(addr_std_path, "r").readlines() + \
                open(addr_alias_path, "r").readlines()
        addr_dict = list()
        for line in lines:
            addr_dict += line.strip().split(",")
        return set(addr_dict)

    @staticmethod
    def __init_pinyin(pinyin_path):
        pinyin = dict()
        with open(pinyin_path, "r") as f:
            for line in f.readlines():
                lines = line.strip().split(",")
                if lines[0] not in pinyin.keys():
                    pinyin[lines[0]] = list()
                pinyin[lines[0]] += lines[1:]
        return pinyin

    @staticmethod
    def __edit_distance(str1, str2):
        matrix = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                if str1[i - 1] == str2[j - 1]:
                    d = 0
                else:
                    d = 1
                matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)
        return matrix[len(str1)][len(str2)]

    @staticmethod
    def __trans_simplified_chinese(texts):
        try:
            import hanziconv
            texts = set([hanziconv.HanziConv.toSimplified(t) for t in texts])
        except:
            pass
        return set(texts)

    # def __pinyin_recognition(self, texts):
    #     pinyin_list = [re.findall(r"[a-zA-Z]+", t) for t in texts]
    #     if len(pinyin_list) > 0:
    #         py2zh = set([self.pinyin.get(p, "") for p in pinyin_list])
    #         py2zh = set([i for i in py2zh if i != ""])
    #         if len(py2zh) > 0:
    #             return set(texts) | py2zh
    #     return set(texts)

    def __text_recognition(self, texts):
        ret = set()
        for text in texts:
            length = len(text)
            for interval in range(1, min(30, length)):
                start = 0
                end = start + interval
                while end < length:
                    if text[start: end + 1] in self.addr_dict:
                        ret.add(text[start: end + 1])
                    start += 1
                    end += 1
        return ret

    def __get_homonym(self, ori_text):
        if ori_text in ("辖区", "市辖区", "直辖县", "市区", "林区", "矿区"):
            return set()
        if self.pinyin:
            homonym = self.pinyin.get("_".join(lazy_pinyin(ori_text)), [])
            if len(homonym) > 0:
                eds = [self.__edit_distance(ori_text, h) for h in homonym]
                min_ed = min(eds)
                fin_homonym = [homonym[i] for i in range(len(eds)) if eds[i] == min_ed]
                return set(fin_homonym)
        return set()

    def __fill_words(self, ori_text):
        """
        漏字补全，呼和浩 -> 呼和浩特
        """
        return set()

    @staticmethod
    def __drop_alias_duplicates(texts):
        # 检查是否有包含关系，如"上海市"包含"上海"，如有则去除没有后缀的地址
        if len(texts) == 0:
            return set()
        ret = set(texts) ^ set([j for i in texts for j in texts if i.find(j) > -1 and len(i) > len(j)])
        return ret

    @staticmethod
    def _drop_alias(text):
        if text != AddressAlias.province(text):
            return AddressAlias.province(text)
        if text != AddressAlias.city(text):
            return AddressAlias.city(text)
        if text != AddressAlias.county(text):
            return AddressAlias.county(text)
        if text != AddressAlias.town(text):
            return AddressAlias.town(text)
        if text != AddressAlias.community(text):
            return AddressAlias.community(text)
        return text

    def modify(self, text):
        # 繁转简
        texts = self.__trans_simplified_chinese({text})
        # 地址字抽取
        texts = self.__text_recognition(texts)
        # 同音词
        if len(texts) == 0:
            texts = self.__get_homonym(text)
        # TODO: 补全漏字
        if len(texts) == 0:
            texts = self.__fill_words(text)
        # 如果文本本身就是一个真实的地方，则去除包含字，如 text="上海市", 结果["上海市","上海","海市"] -> ["上海市"]
        if len(texts) > 1 and len(text) == max([len(word) for word in texts]):
            max_length_word_list = [word for word in texts if len(word) == len(text)]
            if len(max_length_word_list) == 1 and max_length_word_list[0] == text:
                texts = self.__drop_alias_duplicates(texts)
                if len(texts) == 1:
                    raw_text = list(texts)[0]
                    alias = self._drop_alias(raw_text)
                    if raw_text != alias:
                        texts.add(alias)
        # 去除""
        texts = {t for t in texts if t != ""}
        return texts


class AddressAutoFill:

    def __init__(self, addr_std_path, addr_alias_path, pinyin_path=None):
        start_time = time.time()
        self.mapping = self.__init_mapping(addr_std_path, addr_alias_path)
        #         self.alias_mapping = self.__init_alias_mapping(addr_std_path, addr_alias_path)
        self.addr_modifier = AddressTextModifier(addr_std_path, addr_alias_path, pinyin_path)
        print(f"Finish load data with using {round(time.time() - start_time, 2)}s.")

    @staticmethod
    def __init_mapping(addr_std_path, addr_alias_path):
        mapping = dict()

        std_lines = open(addr_std_path, "r").readlines()
        alias_lines = open(addr_alias_path, "r").readlines()

        for std, alias in zip(std_lines, alias_lines):
            std_list = std.strip().split(",")
            alias_list = alias.strip().split(",")

            for i in range(len(std_list)):
                forward_addr_list = std_list[:i + 1] + [""] * (len(std_list) - i - 1)

                if std_list[i] not in mapping.keys():
                    mapping[std_list[i]] = set()
                if alias_list[i] not in mapping.keys():
                    mapping[alias_list[i]] = set()
                # mapping
                mapping[std_list[i]].add(",".join(forward_addr_list))
                mapping[alias_list[i]].add(",".join(forward_addr_list))
        return mapping

    @staticmethod
    def __init_alias_mapping(addr_std_path, addr_alias_path):
        mapping = dict()
        std_lines = open(addr_std_path, "r").readlines()
        alias_lines = open(addr_alias_path, "r").readlines()
        for std, alias in zip(std_lines, alias_lines):
            std_list = std.strip().split(",")
            alias_list = alias.strip().split(",")
            for i in range(len(std_list)):
                forward_std_list = std_list[:i + 1] + [""] * (len(std_list) - i - 1)
                forward_alias_list = alias_list[:i + 1] + [""] * (len(alias_list) - i - 1)
                key = ",".join(forward_alias_list)
                value = ",".join(forward_std_list)
                if key not in mapping.keys():
                    mapping[key] = set()
                mapping[key].add(value)
        for k, v in mapping.items():
            if len(v) > 1:
                print(k, v)
        return mapping

    @staticmethod
    def fill_alias_duplicates_with_score(texts):
        # 为拆分后的词语生成对应的权重，如"上海市"-->"上海,上海市"对应分数为"0.4，0.6"
        ret = dict(zip(texts, [1]*len(texts)))
        # res = copy.deepcopy(texts)
        # print(res)
        for i in texts:
            for j in texts:
                if i.find(j)>-1 and len(i)>len(j):
                    # print(i,j)
                    ret[i]=len(i)/len(i+j)
                    ret[j]=len(j)/len(i+j)
                    # try:
                    #     res.remove(j)
                    # except Exception:
                    #     continue
        return ret

    @staticmethod
    def __filter_contain(candidates, addrs):
        # 检查输入地址addr有多少在候选名单candidates中没有出现的
        # 输出没有出现次数最小的candidates
        if len(candidates) == 0:
            return list()
        ret_candidates = {t: list() for t in range(len(addrs) + 1)}
        for candidate in candidates:
            joint_candidate = ",".join([c for c in candidate if c != ""])
            error_list = [0 if joint_candidate.find(a) > -1 else 1 for a in addrs]
            ret_candidates[sum(error_list)].append(candidate)
        for t in range(len(addrs) + 1):
            if len(ret_candidates[t]) > 0:
                return ret_candidates[t]
        return list()

    @staticmethod
    def __inverse_fillter_contain(candidates, addrs):
        # 检查候选地址candidates有多少在输入地址addr中没有出现的
        # 输出没有出现次数最小的candidates
        if len(candidates) == 0:
            return list()
        ret_candidates = {t: list() for t in range(6)}
        joint_addr = ",".join(addrs)
        for candidate in candidates:
            error_list = [0 if joint_addr.find(c) > -1 else 1 for c in candidate]
            ret_candidates[sum(error_list)].append(candidate)
        for t in range(6):
            if len(ret_candidates[t]) > 0:
                return ret_candidates[t]
        return list()

    @staticmethod
    def filter_contain_with_weight(candidates, addrs):
        # addrs 由两部分组成（dict{展开后的输入},[clean后的list]）
        # 依据加权后的分数依次返回
        if len(candidates) == 0:
            return list()
        ret_candidates = dict()
        for candidate in candidates:
            # 先计算根据输入地址的token计算和其候选之间的相似度
            score = sum([len(a)/len(c) for a in addrs.keys() for c in candidate if a in c])
            # 先计算根据输入地址的token计算和其候选之间的相似度
            score = score+sum([0 if c =='' else addrs[c] for c in candidate for a in addrs.keys() if c in a])
            if score not in ret_candidates:
                ret_candidates[score] = []
            ret_candidates[score].append(candidate)
        print(ret_candidates)
        return ret_candidates[max(list(ret_candidates.keys()))]


    @staticmethod
    def __drop_duplidates(candidates):
        ret_set = set()
        for candidate in candidates:
            ret_set.add(",".join(candidate))
        return [ret.split(",") for ret in ret_set]

    @staticmethod
    def __filter_length(candidates):
        if len(candidates) == 0:
            return list()
        # 选取最短的候选名单
        min_length = min([len([c for c in candidate if c != ""]) for candidate in candidates])
        if min_length == 1:
            min_length = 2

        ret = list()
        for candidate in candidates:
            if len([c for c in candidate if c != ""]) == 1:
                if candidate[0] in ("上海市", "天津市", "北京市", "重庆市"):
                    candidate[1] = candidate[0]
                ret.append(candidate)
                continue
            if len([c for c in candidate if c != ""]) <= min_length:
                ret.append(candidate)

        return ret

    @staticmethod
    def __fill_directed_area(candidates):
        directed_cnty = {
            "河南省": ["济源市"],
            "湖北省": ["仙桃市", "潜江市", "天门市", "神农架林区"],
            "海南省": ["五指山市", "琼海市", "文昌市", "万宁市", "东方市", "屯昌县",
                    "定安县", "澄迈县", "临高县", "保亭黎族苗族自治县", "琼中黎族苗族自治县",
                    "白沙黎族自治县", "陵水黎族自治县", "昌江黎族自治县", "乐东黎族自治县"],
            "新疆维吾尔自治区": ["石河子市", "阿拉尔市", "图木舒克市", "五家渠市", "北屯市",
                         "铁门关市", "双河市", "可克达拉市", "昆玉市", "胡杨河市"]
        }
        ret = []
        for candidate in candidates:
            if len([c for c in candidate if c != ""]) == 2 and candidate[0] in directed_cnty.keys():
                if candidate[1] in directed_cnty[candidate[0]]:
                    candidate[2] = candidate[1]
            ret.append(candidate)
        return ret

    @staticmethod
    def _alias(candicates):
        return [AddressAlias.alias(candidate[0], candidate[1], candidate[2], candidate[3], candidate[4]) \
                for candidate in candicates]

    def fill_alias(self, *addr):
        input_num = len(addr)
        return self.fill(*addr)[:3]

    def fill(self, *addr, alias=False, mode="exact", debug=False, inverse_check=True):
        if mode not in ["all", "exact"]:
            raise ValueError("\"mode\" variable should be \"exact\" or \"all\"!")

        if debug:
            print("origin", addr)

        clear_input = set()
        for a in addr:
            clear_input = clear_input | self.addr_modifier.modify(a)

        clear_input_with_score = self.fill_alias_duplicates_with_score(list(clear_input))

        if debug:
            print("clear", clear_input)

        candidates = [candidate.split(",") for clear_word in clear_input \
                      for candidate in self.mapping[clear_word]]
        candidates = self.__drop_duplidates(candidates)

        if debug:
            print("raw_candidates", candidates)

        candidates0 = self.filter_contain_with_weight(candidates, clear_input_with_score)
        candidates = self.__filter_contain(candidates, clear_input)

        if debug:
            print("filter_contain", candidates)

        if inverse_check:
            candidates = self.__inverse_fillter_contain(candidates, clear_input)

        if debug:
            print("inverse_filter_contain", candidates)

        if mode == "exact":
            candidates = self.__filter_length(candidates)

        candidates = self.__fill_directed_area(candidates)

        if debug:
            print("candidates", candidates)
            print("**candidates**", candidates0)

        if alias:
            candidates = self._alias(candidates)

        if len(candidates) == 0:
            if mode == "exact":
                return ["", "", "", "", ""]
            return [["", "", "", "", ""]]

        if mode == "exact":
            if len(candidates) == 1:
                return candidates[0]
            a1 = list(set([i[0] for i in candidates]))
            a2 = list(set([i[1] for i in candidates]))
            a3 = list(set([i[2] for i in candidates]))
            a4 = list(set([i[3] for i in candidates]))

            a5 = list(set([AddressAlias.community(i[4]) for i in candidates]))
            return [
                a1[0] if len(a1) == 1 else "",
                a2[0] if len(a2) == 1 else "",
                a3[0] if len(a3) == 1 else "",
                a4[0] if len(a4) == 1 else "",
                a5[0] if len(a5) == 1 else "",
            ]
        if mode == "all":
            return candidates
        return candidates

    def __call__(self, *args, **kwargs):
        return self.fill(*args, **kwargs)

