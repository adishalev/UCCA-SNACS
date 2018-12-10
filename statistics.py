import xml.etree.ElementTree as ET
import os
from collections import defaultdict
import itertools


Configuration = ["Configuration", "Identity", "Species", "Gestalt", "Possessor", "Whole", "Characteristic", "Possession",
                 "PartPortion", "Stuff", "Accompanier", "InsteadOf", "ComparisonRef", "RateUnit", "Quantity",
                 "Approximator", "SocialRel", "OrgRole"]
Participant = ["Participant", "Causer", "Agent", "Co-Agent", "Theme", "Co-Theme", "Topic", "Stimulus", "Experiencer",
               "Originator", "Recipient", "Cost", "Beneficiary", "Instrument"]
Circumstance = ["Circumstance", "Temporal", "Time", "StartTime", "EndTime", "Frequency", "Duration", "Interval",
                "Locus", "Source", "Goal", "Path", "Direction", "Extent", "Means", "Manner", "Explanation",
                "Purpose"]
Other = ["NAP", "A"]
SNACS = list(itertools.chain(Configuration, Participant, Circumstance, Other))


def contained(candidate, container):
    temp = container[:]
    try:
        for v in candidate:
            temp.remove(v)
        return True
    except ValueError:
        return False


def get_node_by_id(xml_tree, node_id):
    """
    returns the sub xml tree that node_id is its root
    :param node_id:
    :return:
    """
    for elem in xml_tree.iter("node"):
        if 'ID' in elem.attrib and elem.attrib['ID'] == node_id:
            return elem


def get_all_trees(xml_tree, child_parent_dict, type):
    """
    returns the sub xml tree that node_id is its root
    :param node_id:
    :return:
    """
    static_scenes = []
    for elem in xml_tree.iter("edge"):
        start_id = child_parent_dict[elem].attrib["ID"]
        if 'type' in elem.attrib and elem.attrib['type'] == type:
            static_scenes.append(get_node_by_id(xml_tree, start_id))
    return static_scenes


def get_all_state_trees(xml_tree, child_parent_dict):
    return get_all_trees(xml_tree, child_parent_dict, "S")


def get_all_process_trees(xml_tree, child_parent_dict):
    return get_all_trees(xml_tree, child_parent_dict, "P")



def get_relations_distribution_for_one_xml(scenes, type_histogram, couples):
    for start_node in scenes:
        participants = []
        for e in start_node.findall("edge"):
            if e.attrib["type"] in SNACS:
                participants.append(e.attrib["type"])
        participants = sorted(participants)
        if couples:
            if len(participants) > 1:
                couples = list(itertools.combinations(participants, 2))
                for couple in couples:
                    type_histogram[tuple(couple)] += 1
        else:
            type_histogram[tuple(participants)] += 1



def get_relations_distribution(directory, couples=False):
    static_type_histogram = defaultdict(int)
    dynamic_type_histogram = defaultdict(int)
    xml_files = [xml_file for xml_file in os.listdir(directory) if xml_file.endswith(".xml")]
    for xml_file in xml_files:
        xml_tree = ET.parse(os.path.join(directory, xml_file))
        parent_map = dict((c, p) for p in xml_tree.getiterator() for c in p)
        process_scenes = get_all_process_trees(xml_tree, parent_map)
        static_scenes = get_all_state_trees(xml_tree, parent_map)
        get_relations_distribution_for_one_xml(process_scenes, dynamic_type_histogram, couples)
        get_relations_distribution_for_one_xml(static_scenes, static_type_histogram, couples)
    return static_type_histogram, dynamic_type_histogram



def get_categories_distribution_for_one_xml(xml_tree, type_histogram):
    for e in xml_tree.iter("edge"):
        type_histogram[e.attrib['type']] += 1
        type_histogram['total'] += 1
        if e.attrib['type'] in SNACS:
            type_histogram['total_snacs'] += 1


def get_one_category_histogram(directory):
    type_histogram = defaultdict(int)
    xml_files = [xml_file for xml_file in os.listdir(directory) if xml_file.endswith(".xml")]
    for xml_file in xml_files:
        xml_tree = ET.parse(os.path.join(directory, xml_file))
        get_categories_distribution_for_one_xml(xml_tree, type_histogram)
    return type_histogram


def print_sample_vs_full_ucca_entities_distribution():
    directory = r'data/UCCA_wiki_full/xmls'
    types_full = get_one_category_histogram(directory)
    directory = r'data/UCCA_wiki_sample/xmls'
    types_sample = get_one_category_histogram(directory)
    for (key_sample, value_sample), (key_full, value_full) in zip(types_sample.items(), types_full.items()):
        print(key_sample + ": " + str(value_sample), str(value_sample*100.0/types_sample['total']) +
              ", "+ str(value_full), str(value_full * 100.0 / types_full['total']))


def print_snacs_participants_distribution():
    directory = r'data/UCCA_SNACS_wiki_sample_v1/xmls'
    types_sample = get_one_category_histogram(directory)
    for key_sample, value_sample in types_sample.items():
        if key_sample not in SNACS:
            continue
        print(key_sample + ": " + str(value_sample), str(value_sample*100.0/types_sample['total_snacs']))


def print_relations_distribution():
    directory = r'data/UCCA_SNACS_wiki_sample_v1/xmls'
    static, dynamic = get_relations_distribution(directory)
    print("************** Static *****************")
    for key, value in sorted( ((v,k) for k,v in static.items()), reverse=True):
        print ("%s: %s" % (key, value))
    print("************** Dynamic *****************")
    for key, value in sorted( ((v,k) for k,v in dynamic.items()), reverse=True):
        print ("%s: %s" % (key, value))


def print_couples_in_relations_distribution():
    directory = r'data/UCCA_SNACS_wiki_sample_v1/xmls'
    static, dynamic = get_relations_distribution(directory, True)
    print("************** Static *****************")
    for key, value in sorted( ((v,k) for k,v in static.items()), reverse=True):
        print ("%s: %s" % (key, value))
    print("************** Dynamic *****************")
    for key, value in sorted( ((v,k) for k,v in dynamic.items()), reverse=True):
        print ("%s: %s" % (key, value))



def get_terminals(start_node, xml_tree):
    """
    returns the sub xml tree that node_id is its root
    :param node_id:
    :return:
    """
    terminals = []
    if start_node is None:
        return []
    for elem in start_node.iter("edge"):
        if 'type' in elem.attrib and elem.attrib['type'] == "Terminal":
            terminals.append(elem.attrib['toID'])
        else:
            terminals.extend(get_terminals(get_node_by_id(xml_tree, elem.attrib['toID']), xml_tree))
    return terminals



def print_text_for_node(start_node, xml_tree, node_id, edge_type):
    attributes = start_node.find('attributes')
    if "implicit" in attributes.attrib and attributes.attrib["implicit"] == "True":
        res_str = "implicit , type: " + edge_type + " id: " + node_id
        print(res_str)
    terminals = sorted(get_terminals(start_node, xml_tree))
    terminal_position = []
    for t_id in terminals:
        attributes = get_node_by_id(xml_tree, t_id).find('attributes')
        terminal_position.append((attributes.attrib['text'], int(attributes.attrib['paragraph']),
                                  int(attributes.attrib['paragraph_position'])))
    terminal_position = sorted(terminal_position, key=lambda x: (int(x[1]), int(x[2])))
    if terminal_position:
        partial_text = " ".join([x[0] for x in terminal_position])
        res_str = "paragraph #" + str(terminal_position[0][1]) + ": " + partial_text + " , type: " + \
                  edge_type + " id: " + node_id
        print(res_str)


def print_scene(start_node, xml_tree):
    print_text_for_node(start_node, xml_tree, start_node.attrib["ID"], "scene")
    for e in start_node.findall("edge"):
        e_elem = get_node_by_id(xml_tree, e.attrib["toID"])
        print_text_for_node(e_elem, xml_tree, e.attrib["toID"], e.attrib["type"])



def get_scenes_that_contain(scenes, contained_participants):
    passed_cond_scenes = []
    for start_node in scenes:
        participants = []
        for e in start_node.findall("edge"):
            if e.attrib["type"] in SNACS:
                participants.append(e.attrib["type"])
        if contained(contained_participants, participants):
            passed_cond_scenes.append(start_node)
    return passed_cond_scenes


def get_scenes_with_relation(type, participants, directory):
    passage_scenes = defaultdict(list)
    xml_files = [xml_file for xml_file in os.listdir(directory) if xml_file.endswith(".xml")]
    for xml_file in xml_files:
        xml_tree = ET.parse(os.path.join(directory, xml_file))
        parent_map = dict((c, p) for p in xml_tree.getiterator() for c in p)
        if type == "P":
            scenes = get_all_process_trees(xml_tree, parent_map)
        else:
            scenes = get_all_state_trees(xml_tree, parent_map)
        passed_cond_scenes = get_scenes_that_contain(scenes, participants)
        if passed_cond_scenes:
            passage_scenes[xml_file] = (xml_tree, passed_cond_scenes)
    return passage_scenes


def print_scenes_with_relation(type, participants, size=-1):
    directory = r'data/UCCA_SNACS_wiki_sample/xmls'
    passed_cond_scenes = get_scenes_with_relation(type, participants, directory)
    count = 0
    for xml, (xml_tree, scenes_list) in passed_cond_scenes.items():
        if count < size or size == -1:
            print("****** " + xml + " ******")
            print()
        for scene in scenes_list:
            if count < size or size == -1:
                print_scene(scene, xml_tree)
                print()
            count += 1
    if size == -1 or size > count:
        size = count
    print("printed " + str(size) + " out of " + str(count) + " scenes.")




if __name__ == '__main__':
    #print_sample_vs_full_ucca_entities_distribution()
    #print_snacs_participants_distribution()
    #print_relations_distribution()
    #print_couples_in_relations_distribution()
    #print_scenes_with_relation("P", ["Experiencer"], -1)
    print_scenes_with_relation("S", ["OrgRole"], -1)
    #for category in Participant:
    #    print("---------------------- " + category + " ----------------------")
    #    print()
    #    print_scenes_with_relation("S", [category], 10)
    #    print()







