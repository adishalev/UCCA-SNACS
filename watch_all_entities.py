import xml.etree.ElementTree as ET


def extract_text(xml_tree):
    text = []
    for layer in xml_tree.iter("layer"):
        if layer.attrib['layerID'] == '0':
            for node in layer.iter('node'):
                text.append(node.find('attributes').attrib['text'])
    return " ".join(text)


def get_node_by_id(xml_tree, node_id):
    """
    returns the sub xml tree that node_id is its root
    :param node_id:
    :return:
    """
    for elem in xml_tree.iter("node"):
        if 'ID' in elem.attrib and elem.attrib['ID'] == node_id:
            return elem

def get_all_participants(xml_tree):
    """
    returns the sub xml tree that node_id is its root
    :param node_id:
    :return:
    """
    participants = []
    for elem in xml_tree.iter("edge"):
        if 'type' in elem.attrib and elem.attrib['type'] == "A":
            participants.append(elem.attrib['toID'])
    return participants

def get_all_entities_new(start_node, type):
    """
    returns the sub xml tree that node_id is its root
    :param node_id:
    :return:
    """
    entities = []
    if start_node is None:
        return entities
    for elem in start_node.iter("edge"):
        if 'type' in elem.attrib and (elem.attrib['type'] == type or type == "none"):
            entities.append((elem.attrib['toID'], elem.attrib['type']))
    return entities


def get_all_entities(xml_tree, child_parent_dict, start_node, type):
    """
    returns the sub xml tree that node_id is its root
    :param node_id:
    :return:
    """
    entities = []
    if start_node is None:
        return entities
    if start_node == xml_tree:
        for elem in start_node.iter("edge"):
            start_id = child_parent_dict[elem].attrib["ID"]
            if 'type' in elem.attrib and (elem.attrib['type'] == type or type == "none"):
                entities.append((elem.attrib['toID'], elem.attrib['type'], start_id))
                entities.extend(get_all_entities(xml_tree, child_parent_dict, get_node_by_id(xml_tree, elem.attrib['toID']), type))
    else:
        start_id = start_node.attrib["ID"]
        for elem in start_node.findall("edge"):
            if 'type' in elem.attrib and (elem.attrib['type'] == type or type == "none"):
                entities.append((elem.attrib['toID'], elem.attrib['type'], start_id))
                entities.extend(get_all_entities(xml_tree, child_parent_dict, get_node_by_id(xml_tree, elem.attrib['toID']), type))
    return entities


def get_terminals(xml_tree, start_node):
    """
    returns the sub xml tree that node_id is its root
    :param node_id:
    :return:
    """
    terminals = []
    if start_node is None:
        return []
    if start_node == xml_tree:
        for elem in start_node.iterate("edge"):
            if 'type' in elem.attrib and elem.attrib['type'] == "Terminal":
                terminals.append(elem.attrib['toID'])
            else:
                terminals.extend(get_terminals(xml_tree, get_node_by_id(xml_tree, elem.attrib['toID'])))
    else:
        for elem in start_node.findall("edge"):
            if 'type' in elem.attrib and elem.attrib['type'] == "Terminal":
                terminals.append(elem.attrib['toID'])
            else:
                terminals.extend(get_terminals(xml_tree, get_node_by_id(xml_tree, elem.attrib['toID'])))
    return terminals


def get_all_entities_which_contains(xml_name, xml_tree, start_node, substr, type='none'):
    first = True
    old_paragrph_num = 0
    participants = get_all_entities(xml_tree, start_node, type)
    for p_to_id, p_type, p_start_id in participants:
        p_elem = get_node_by_id(xml_tree, p_to_id)
        terminals = sorted(get_terminals(xml_tree, p_elem))
        terminal_position = []
        for t_id in terminals:
            attributes = get_node_by_id(xml_tree, t_id).find('attributes')
            terminal_position.append((attributes.attrib['text'], int(attributes.attrib['paragraph']), int(attributes.attrib['paragraph_position'])))
        terminal_position = sorted(terminal_position, key=lambda x: (int(x[1]), int(x[2])))
        if terminal_position:
            text_list = [x[0].lower() for x in terminal_position]
            partial_text = " ".join([x[0] for x in terminal_position])
            if substr.lower() in text_list or substr == "":
                if first:
                    print(xml_name)
                    text = extract_text(xml_tree)
                    print(text)
                    first = False
                if terminal_position[0][1] >= old_paragrph_num:
                    print("paragraph #" +str(terminal_position[0][1])+": "+ partial_text + " , type: " + \
                          p_type + " id: " + p_to_id)
                    old_paragrph_num = terminal_position[0][1]

                else:
                    break
    return first



def get_one_xml(xml_tree, start_node, substr, type='none'):
    old_paragrph_num = 0
    res = []
    parent_map = dict((c, p) for p in xml_tree.getiterator() for c in p)
    participants = get_all_entities(xml_tree, parent_map, start_node, type)
    for p_to_id, p_type, p_start_id in participants:
        p_elem = get_node_by_id(xml_tree, p_to_id)
        terminals = sorted(get_terminals(xml_tree, p_elem))
        terminal_position = []
        for t_id in terminals:
            attributes = get_node_by_id(xml_tree, t_id).find('attributes')
            terminal_position.append((attributes.attrib['text'], int(attributes.attrib['paragraph']),
                                      int(attributes.attrib['paragraph_position'])))
        terminal_position = sorted(terminal_position, key=lambda x: (int(x[1]), int(x[2])))
        if terminal_position:
            text_list = [x[0].lower() for x in terminal_position]
            partial_text = " ".join([x[0] for x in terminal_position])
            if substr.lower() in text_list or substr == "":
                if terminal_position[0][1] >= old_paragrph_num:
                    res_str = "paragraph #" + str(terminal_position[0][1]) + ": " + partial_text + " , type: " + \
                          p_type + " id: " + p_to_id
                    #print(res_str)
                    old_paragrph_num = terminal_position[0][1]
                    res.append((res_str, p_start_id))
                else:
                    break
    return res


def get_all_xmls(xmls_dict):
    import os
    directory = r'xmls'
    res = {}
    for filename in xmls_dict.keys():
        if filename.endswith(".xml"):
            xml_name = os.path.join(directory, filename)
            xml_tree = ET.parse(xml_name)
            res[filename] = get_all_entities_which_contains(xml_name, xml_tree, xml_tree, "", "none")
            break
        else:
            continue


if __name__ == '__main__':
    import os
    directory = r'xmls'
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            xml_name = os.path.join(directory, filename)
            xml_tree = ET.parse(xml_name)
            get_all_entities_which_contains(xml_name, xml_tree, xml_tree, "", "none")
            break
        else:
            continue


