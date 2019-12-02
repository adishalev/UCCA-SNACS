import os
from ucca.convert import *
import xml.etree.ElementTree as ET


def convert(in_path, out_path):
    xmls = [xml for xml in os.listdir(in_path) if xml.endswith(".xml")]
    for xml in xmls:
        xml_tree = ET.parse(os.path.join(in_path, xml))
        root = to_standard(from_standard(xml_tree.getroot()))
        out_xml_name = os.path.join(out_path, xml)
        xml_string = ET.tostring(root).decode()
        output = textutil.indent_xml(xml_string)
        with open(out_xml_name, "w", encoding="utf-8") as h:
            h.write(output)


if __name__ == '__main__':
    in_path = '/Users/ashalev/PycharmProjects/UCCA-SNACS/data/out_of_domain/UCCA_English-20K-master/xml'
    out_path = '/Users/ashalev/PycharmProjects/UCCA-SNACS/data/out_of_domain/UCCA_English-20K-master/new_xml'
    convert(in_path, out_path)