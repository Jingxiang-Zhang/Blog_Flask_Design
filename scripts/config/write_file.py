from .xml_create import ConfigCreater


class Write:
    def __init__(self, key=None):
        """
        用于写入xml文件
        :param key: 用于加密、解密的秘钥，如果为None则不对文件加密
        """
        self.key = key
        if not key:
            print("warning: you are trying to generate an unencrypted configuration file")
        self.config_creater = ConfigCreater()

    def write(self, file_path):
        """
        用于开始写文件
        :param file_path: 文件路径
        :return: None
        """
        self.config_creater.export_xml(file_path)

    def add_item(self, *args, **kwargs):
        """
        添加一项元素
        :param group: 该键值对所属的组名称
        :param key: 元素的键
        :param value: 元素的值
        :return: None
        """
        self.config_creater.add_item(*args, **kwargs)


