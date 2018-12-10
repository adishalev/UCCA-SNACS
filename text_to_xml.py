import xml.etree.ElementTree as ET
import re
from statistics import SNACS as categories


def text_to_lists(filename):
    xmls = {}
    with open(filename, 'rb') as f:
        curr_key = ""
        for line in f.readlines():
            line = line.decode('utf-8')
            if line.startswith("ucca_passage"):
                curr_key = line.strip()
                xmls[curr_key] = []
            elif line.startswith("paragraph #"):
                xmls[curr_key].append(line.strip())
    return xmls


def lists_to_xmls(xmls_lists):
    categories_histogram = defaultdict(int)
    for x in xmls_lists.keys():
        passage_participants = 0
        xml_name = os.path.join(in_directory, x)
        xml_tree = ET.parse(xml_name)
        original_xml = get_one_xml(xml_tree, xml_tree, "")
        for original, annotated in zip(original_xml, xmls_lists[x]):
            annotation = annotated.strip().split(" ")[-1]
            type = ""
            m = re.search('type: (.+?) id:', original[0])
            if m:
                type = m.group(1)
            is_participant = type in categories
            if is_participant and annotation:
                passage_participants += 1
                categories_histogram[annotation] += 1
                from_id = str(original[1]).strip()
                to_id = original[0].strip().split(" ")[-1]
                nodes = xml_tree.iterfind(".//node[@ID='"+from_id+"']")
                has_edge = False
                for node in nodes:
                    e = node.find(".//edge[@toID='"+to_id+"']")
                    e.attrib['type'] = annotation
                    has_edge = True
        xml_name = os.path.join(out_directory, x)
        xml_tree.write(open(xml_name, 'wb'))


if __name__ == '__main__':
    import os
    from watch_all_entities import get_one_xml
    from collections import defaultdict

    data_dir = r'data/UCCA_SNACS_wiki_sample'
    in_directory = out_directory = os.path.join(data_dir, "xmls")
    text_file = os.path.join(data_dir, "annotated_data.txt")
    xmls_lists = text_to_lists(text_file)
    lists_to_xmls(xmls_lists)


