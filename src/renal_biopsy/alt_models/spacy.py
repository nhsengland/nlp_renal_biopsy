import spacy
from spacy.language import Language
import re


def number_word_to_int(text):
    text = text.lower().strip()

    # Basic number dictionary
    ones = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    tens = [
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
    ]
    teens = [
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
    ]

    number_map = {word: num for num, word in enumerate(ones)}  # 0-9
    number_map.update({word: num + 10 for num, word in enumerate(teens)})  # 10-19
    number_map.update(
        {word: (num + 2) * 10 for num, word in enumerate(tens)}
    )  # 20,30,40,...

    # Handle hyphenated numbers (e.g., 'twenty-one')
    if "-" in text:
        tens_word, ones_word = text.split("-")
        if tens_word in tens and ones_word in ones:
            return number_map[tens_word] + number_map[ones_word]

    # Handle direct word matches (single words like 'fifteen' or 'twenty')
    if text in number_map:
        return number_map[text]

    # Handle compound numbers (e.g., "twenty five")
    words = text.split()
    if len(words) == 2:
        if words[0] in tens and words[1] in ones:
            return number_map[words[0]] + number_map[words[1]]

    return None


def extract_number(text):
    # First try to find a digit
    digit_match = re.search(r"(\d+)", text)
    if digit_match:
        return int(digit_match.group(1))

    # Then try to find a word number
    for word in text.lower().split():
        number = number_word_to_int(word)
        if number is not None:
            return number
    return None


@Language.component("custom_entity_ruler")
def custom_entity_ruler(doc):
    patterns = {
        # Basic structure patterns
        "cortex": r"""(?ix)
        cortex
        (?!\s+
            (?:absent|
                missing|
                not\s+(?:present|identified|seen))
        )
        """,
        "medulla": r"""(?ix)
        medulla
        (?!\s+
            (?:absent|
                missing|
                not\s+(?:present|identified|seen))
        )
        """,
        "cortex_absent": r"""(?ix)
        cortex
        \s+
        (?:absent|
            missing|
            not\s+(?:present|identified|seen))
        """,
        "medulla_absent": r"""(?ix)
        medulla
        \s+
        (?:absent|
            missing|
            not\s+(?:present|identified|seen))
        """,
        # Glomeruli counts - with comprehensive fuzzy matching
        "n_total": r"""(?ix)                    # Case insensitive and verbose mode
            (?:contain(?:ing?|g|en|ng)|         # Variations of contain
               includ(?:ing?|es|ed)|
               consists?\s+of|with|shows?|
               having|composed\s+of|has|
               present|identified|seen|noted)    # Additional verbs
            \s+
            (?:(?:approximately|about|around|    # Optional approximation
                roughly|~)\s+)?
            (?:(\d+)|                           # Digits
               (?:(?:twenty|thirty|forty|fifty|sixty|
                  seventy|eighty|ninety)
                  (?:[- ](?:one|two|three|four|five|
                         six|seven|eight|nine))?|
                  ten|eleven|twelve|thirteen|fourteen|
                  fifteen|sixteen|seventeen|eighteen|
                  nineteen|one|two|three|four|five|
                  six|seven|eight|nine))         # Word numbers
            \s*
            (?:gl(?:o|a|e|ea|eo|u|oa)?m        # Very flexible glom prefix
               (?:e|a|o|u|ur|eru|aru|ora|ere)?  # Middle variations
               (?:r|rr)?                        # Optional double r
               (?:u|o|e|a|i)?                   # Vowel variations
               l(?:i|us|um|ae|e|ii|ous|ar|er)?  # Various endings
               s?)                              # Optional plural s""",
        "n_global": r"""(?ix)
            (?:(\d+)|one|two|three|four|five|six|seven|eight|nine|ten)
            \s*
            (?:globally|complete(?:ly)?)
            \s*
            sclerosed
            \s*
            glomerul[ius]
        """,
        "n_global_relative": r"""(?ix)
            (?:(\d+)|one|two|three|four|five|six|seven|eight|nine|ten)
            \s+
            (?:of\s+
                (?:these|which|the|these\s+glomeruli)
                \s+
                (?:(?:are|is|were|was|show(?:ed)?|display(?:ed)?|appear(?:ed)?)\s+)?
            )?
            (?:globally|complete(?:ly)?)
            \s+
            sclerosed
        """,
        "n_segmental": r"""(?ix)
            (?:(\d+)|one|two|three|four|five|six|seven|eight|nine|ten)
            \s*
            (?:segment(?:al(?:ly)?)|partial(?:ly)?)
            \s*
            sclerosed
            \s*
            glomerul[ius]
        """,
        "n_segmental_relative": r"""(?ix)
            (?:(\d+)|one|two|three|four|five|six|seven|eight|nine|ten)
            \s+
            (?:of\s+
                (?:these|which|the|these\s+glomeruli)
                \s+
                (?:(?:are|is|were|was|show(?:ed)?|display(?:ed)?|appear(?:ed)?)\s+)?
            )?
            (?:segment(?:al(?:ly)?)|partial(?:ly)?)
            \s+
            (?:sclerosed|sclerosis)
        """,
        # Chronic changes
        "chronic_change_adj": r"""(?ix)
            (minimal|mild|moderate|severe|marked|extensive|florid)
            (?:\s+(?:irreversible|reversible))?
            \s+
            (?:tubular\s+atrophy|
            interstitial\s+fibrosis|
            chronic\s+changes?|
            chronic\s+allograft\s+nephropathy)
        """,
        "chronic_change_percentage": r"""(?ix)
            (?:affecting|involves?|involving|present\s+in)
            \s+
            (?:approximately\s+)?
            (\d+(?:\.\d+)?)
            \s*%\s*
            (?:of\s*)?
            (?:the\s+)?
            (?:cortex|parenchyma|tissue|sample|biopsy)
        """,
        # Rejection patterns
        "rejection_grade": r"""(?ix)
            (?:grade|type|classification)?
            \s*
            (?:1[abc]|2[abc]|3|4|5|6)
            \s*
            (?:rejection)?
        """,
        "rejection_type": r"""(?ix)
            (?:acute|chronic)
            \s+
            (?:T-cell[- ]mediated|
            cellular|
            humoral|
            antibody[- ]mediated)
            \s+
            rejection
        """,
        # Glomerular abnormalities
        "abnormal_glomeruli": r"""(?ix)
            (?:glomerul(?:ar|i))?
            \s*
            (?:(?P<count>\d+)\s+)?
            (?:scarring|
            isch(?:a)?emic\s+changes|
            thickening\s+of\s+bowman(?:'s)?\s+capsule|
            thickening\s+of\s+(?:capillary\s+)?basement\s+membrane|
            mesangial\s+(?:expansion|thickening)|
            changes?\s+in\s+(?:size|shape)|
            irregular\s+(?:size|shape))
        """,
        # Other patterns
        "transplant": r"(?i)(transplant(?:ation)?|infiltrate[sd]?|infection)",
        "diagnosis": r"(?i)(?:final\s*)?diagnosis\s*[:;]\s*(.*?)(?:\.|$)",
    }

    entities = []
    for ent_type, pattern in patterns.items():
        for match in re.finditer(pattern, doc.text):
            start, end = match.span()
            if not any(start < e.end_char and end > e.start_char for e in entities):
                span = doc.char_span(start, end, label=ent_type)
                if span is not None:
                    entities.append(span)

    doc.ents = entities
    return doc


def process_reports(reports, n_prototype=2):
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("custom_entity_ruler")

    all_results = []
    all_docs = []

    for i, r in enumerate(reports):
        if i == n_prototype:
            break

        doc = nlp(r)

        results = {
            "cortex_present": True,
            "medulla_present": False,
            "n_total": 0,
            "n_segmental": 0,
            "n_global": 0,
            "abnormal_glomeruli": False,
            "chronic_change": None,
            "chronic_change_percentage": None,
            "chronic_change_adj": None,
            # "tubulitis": None,
            # "infiltrate": None,
            "rejection_type": None,
            "rejection_grade": None,
            "transplant": False,
            "diagnosis": None,
        }

        # has_cortex_mention = False
        # has_medulla_mention = False
        chronic_change_perc = None
        chronic_change_adj = None

        for ent in doc.ents:
            if ent.label_ == "cortex":
                results["cortex_present"] = True
                # has_cortex_mention = True
            elif ent.label_ == "cortex_absent":
                results["cortex_present"] = False
                # has_cortex_mention = True
            elif ent.label_ == "medulla":
                results["medulla_present"] = True
                # has_medulla_mention = True
            elif ent.label_ == "medulla_absent":
                results["medulla_present"] = False
                # has_medulla_mention = True
            elif ent.label_ == "transplant":
                results["transplant"] = True
            elif ent.label_ == "abnormal_glomeruli":
                results["abnormal_glomeruli"] = True
            elif ent.label_ == "chronic_change_percentage":
                chronic_change_perc = float(
                    re.search(r"(\d+(?:\.\d+)?)", ent.text).group(1)
                )
                results["chronic_change_percentage"] = chronic_change_perc
            elif ent.label_ == "chronic_change_adj":
                chronic_change_adj = (
                    re.search(
                        r"(minimal|mild|moderate|severe|marked|extensive|florid)",
                        ent.text,
                        re.I,
                    )
                    .group(1)
                    .lower()
                )
                results["chronic_change_adj"] = chronic_change_adj
            # elif ent.label_ == "tubulitis":
            #    results["tubulitis"] = re.search(
            #           r"(minimal|mild|moderate|severe|marked|extensive|florid)",
            #                                ent.text, re.I).group(1).lower()
            # elif ent.label_ == "infiltrate":
            #    results["infiltrate"] = ent.text
            elif ent.label_ == "rejection_type":
                results["rejection_type"] = ent.text
            elif ent.label_ == "rejection_grade":
                results["rejection_grade"] = re.search(
                    r"(?:1[abc]|2[abc]|3|4|5|6)", ent.text, re.I
                ).group()
            elif ent.label_ == "n_total":
                number = extract_number(ent.text)
                if number is not None:
                    results["n_total"] = number
            elif ent.label_ in ["n_segmental", "n_segmental_relative"]:
                number = extract_number(ent.text)
                if number is not None:
                    results["n_segmental"] = number
            elif ent.label_ in ["n_global", "n_global_relative"]:
                number = extract_number(ent.text)
                if number is not None:
                    results["n_global"] = number
            elif ent.label_ == "diagnosis":
                results["diagnosis"] = ent.text.split(":", 1)[-1].strip()

        results["chronic_change"] = (
            chronic_change_perc
            if chronic_change_perc is not None
            else chronic_change_adj
        )

        all_results.append(results)
        all_docs.append(doc)

    return all_results, all_docs
