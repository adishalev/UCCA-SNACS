UCCA-SNACS
============================

UCCA is a semantic multi-layered framework for semantic representation that aims to accommodate the semantic distinctions 
expressed through linguistic utterances. [Universal Conceptual Cognitive Annotation (UCCA)][1].
SNACS (Semantic Network of Adposition and Case Supersenses) is a new annotation scheme for the disambiguation of prepositions 
and possessives in English. SNACS annotations are comprehensive with respect to types and tokens of these markers and use 
broadly applicable supersense classes. [Comprehensive Supersense Disambiguation of
English Prepositions and Possessives][2].
Here we use SNACS supersense classes (also known as scene roles) as a refinement layer for UCCA Participants, which in 
correspondence to the Process/State from the Foundational layer they serve as a Semantic Role layer.

This repository contains:
  1. Sample of ~30% of the UCCA Wiki corpus with a refinement layer for participants where each participants is annotated 
     according to its Semantic Role.
  2. Code to review the data and get more information about the Roles distribution i.e. a full histogram, roles distributions 
     in Static vs. Dynamic scenes and more.

### Statistics

To know more about the Semantic Roles distribution in the corpora run:
  python -m statistics.py


Author
------
* Adi Shalev: adi.bitan@mail.huji.ac.il

License
-------
This package is licensed under the GPLv3 or later license (see [`LICENSE.txt`](LICENSE.txt)).

[1]: http://aclweb.org/anthology/P13-1023
[2]: http://aclweb.org/anthology/P18-1018
