import xml.etree.ElementTree as ET
import re

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
    print(len(xmls))
    return xmls


categories = ["Agent", "Theme", "Causer", "Experiencer", "Topic", "Originator", "Possessor", "Possession",
              "Stimulus", "Instrument", "Circumstance", "Manner", "Explanation", "Means", "Gestalt", "Characteristic",
              "ComparisonRef", "InsteadOf", "Goal", "Locus", "Whole", "PartPortion", "Beneficiary", "Purpose",
              "Cost", "Source", "Recipient", "Co-Theme", "Co-Agent", "OrgRole", "SocialRel", "Identity",
              "Approximator", "Path", "Direction", "Accompanier", "Time", "StartTime", "EndTime",
              "Frequency", "Extent", "Duration", "Stuff", "Quantity", "NAP", "A"]

if __name__ == '__main__':
    import os
    from watch_all_entities import get_one_xml
    from collections import defaultdict

    in_directory = r'data/UCCA_SNACS_wiki_sample_v1/xmls'
    out_directory = r'data/UCCA_SNACS_wiki_sample_v1/xmls'
    xmls = text_to_lists("data/UCCA_SNACS_wiki_sample_v1/annotated_data.txt")
    total_participants = 0

    categories_histogram = defaultdict(int)
    for x in xmls.keys():
        passage_participants = 0
        xml_name = os.path.join(in_directory, x)
        xml_tree = ET.parse(xml_name)
        original_xml = get_one_xml(xml_tree, xml_tree, "")
        participants = []
        for original, annotated in zip(original_xml, xmls[x]):
            annotation = annotated.strip().split(" ")[-1]
            type = ""
            m = re.search('type: (.+?) id:', original[0])
            if m:
                type = m.group(1)
            is_participant = type in categories
            if is_participant and not annotation:
                print "no annotation"
                print original[0]
                print annotated
                print annotation
            if is_participant and annotation:
                if annotation not in categories:
                    print "not in categories"
                    print original[0]
                    print annotated
                    print annotation
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
                if not has_edge:
                    print original[0]
                    print annotation
                    print annotated
        xml_name = os.path.join(out_directory, x)
        xml_tree.write(open(xml_name, 'wb'))
        #print passage_participants
        total_participants += passage_participants
    print total_participants
    for category in categories_histogram:
        print category + ": " + str(categories_histogram[category])


