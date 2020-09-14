import tantivy
import jieba
import time
from tqdm import tqdm


class AddressAutoSearch:
    def __init__(self, addr_std_path, addr_alias_path):
        start_time = time.time()
        self.index = self.__create_index()
        self.__add_documents(addr_std_path, addr_alias_path)
        self.searcher = self.index.searcher()
        end_time = time.time()
        print(f"Build time is {round(end_time - start_time, 2)} s.")

    @staticmethod
    def __create_index():
        schema_builder = tantivy.SchemaBuilder()
        schema_builder.add_text_field("addr", stored=True)
        schema_builder.add_text_field("addr_alias", stored=True)
        schema = schema_builder.build()
        index = tantivy.Index(schema)
        return index

    def __add_documents(self, addr_std_path, addr_alias_path):
        writer = self.index.writer()

        addr_std = [i.strip().split(",") for i in open(addr_std_path).readlines()]
        addr_alias = [i.strip().split(",") for i in open(addr_alias_path).readlines()]

        addr_std_all, addr_alias_all = list(), list()
        for std, alias in tqdm(zip(addr_std, addr_alias)):
            for i in range(len(std)):
                std_list, alias_list = list(), list()
                for addr in std[:i + 1]:
                    std_list += jieba.lcut(addr)
                for addr in alias[:i + 1]:
                    alias_list += jieba.lcut(addr)

                addr_std_all.append(" ".join(std_list))
                addr_alias_all.append(" ".join(alias_list))

                writer.add_document(tantivy.Document(
                    addr=[" ".join(std_list)],
                    addr_alias=[" ".join(alias_list)]
                ))

        open("./sources/db_std.txt", "w").writelines([i+"\n" for i in addr_std_all])
        open("./sources/db_alias.txt", "w").writelines([i + "\n" for i in addr_alias_all])

        writer.commit()
        self.index.reload()

    def fill(self, text):
        query = self.index.parse_query(text, ["addr"])
        (best_score, best_doc_address) = self.searcher.search(query, 1).hits[0]
        best_doc = self.searcher.doc(best_doc_address)
        return best_doc


if __name__ == "__main__":
    auto_search = AddressAutoSearch("./sources/pcasv.txt", "./sources/pcasv_alias.txt")
    print(auto_search.fill("江苏省"))
    print(auto_search.fill("长沙 咸 湖南"))
    print(auto_search.fill("广东 东莞 三角"))
