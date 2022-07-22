from .read_file import Read


class CheckPwd:
    def __init__(self):
        pass

    @staticmethod
    def check_pwd_input_with_force(path, group=("emile", "sql", "key", "sql_development")):
        """
        用于便捷的进行密码的输入
        :param path: config文件路径
        :param group:
            需要提取的组标签，例如需要xml文件中的emile和key元素下的所有键值对，则使用
            ("emile", "key")
        :return:
        """
        file = Read()
        file = file.read(path)
        ret = Read.tile(xml_=file, element_list=group, interpret=True)
        return ret
