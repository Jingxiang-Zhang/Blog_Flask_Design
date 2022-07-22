from xml.dom import minidom


class ConfigCreater:
    def __init__(self):
        self.xml = minidom.Document()
        impl = minidom.getDOMImplementation()
        self.dom = impl.createDocument(None, None, None)
        self.server_ini = self.dom.createElement("server_ini")
        self.dom.appendChild(self.server_ini)

    def export_xml(self, file_path):
        """
        将xml导出
        :param file_path: 文件路径
        :return: None
        """
        with open(file_path, "w") as file:
            self.dom.writexml(file, '', ' ', '\n', 'utf-8')

    def xml_tostring(self):
        """
        返回字符串化的xml
        :return: None
        """
        return self.dom.toxml()

    def add_item(self, group, key, value):
        """
        添加一项元素
        :param group: 该键值对所属的组名称
        :param key: 元素的键
        :param value: 元素的值
        :return: None
        """
        item = self.dom.createElement(str(group))
        item.setAttribute("id", str(key))
        item.appendChild(self.xml.createTextNode(str(value)))
        self.server_ini.appendChild(item)


