from .xml_create import ConfigCreater
from .errortype import ReadXmlException


class Read:
    def __init__(self):
        """
        用于读取特定类型的xml文本
        """

    def read(self, path):
        """
        读取文本
        :param path: 文本的路径
        :return: xml字符串
        """
        with open(path) as file:
            content = "".join(file.readlines())
        return content

    @staticmethod
    def tile(xml_, element_list, interpret=True):
        """
        按照不同的元素组对xml文件进行读取
        :param xml_: 由read函数读取的xml文件
        :param element_list:
            需要提取的组标签，例如需要xml文件中的emile和key元素下的所有键值对，则使用
            ("emile", "key")
        :param interpret: 是否解析数据
            如果解析数据，T则被解析为True，F被解析为False，数字被解析为字符串类型
        :return: 字典形式的键值对
        """

        from xml.dom import minidom

        xml = minidom.parseString(xml_)
        root = xml.documentElement
        ret = dict()
        for item in element_list:
            elements = root.getElementsByTagName(item)
            for element in elements:
                id = element.getAttribute('id')
                text = element.childNodes[0].data.replace('\n', '')
                if interpret:
                    if text == "T" or text == "F":
                        if text == "T":
                            text = True
                        else:
                            text = False
                    elif str(text).find(".") == -1:
                        try:
                            text = int(text)
                        except Exception:
                            pass
                    else:
                        try:
                            text = float(text)
                        except Exception:
                            pass
                ret[id] = text
        return ret
