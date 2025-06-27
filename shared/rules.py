# Translate rules to human-readable
def parse_rule_line(rule_line, lbl):
    rule_depth = rule_line.count('|   ')
    content = rule_line.strip().replace('|--- ', '').replace('|   ', '')

    if 'class:' in content:
        label = content.split(':')[-1].strip()
        return rule_depth, f"THEN → {lbl if label == '1' else f'Not {lbl}'}"
    else:
        parts = content.split(' ')
        feature = parts[0].replace('_', ' ')
        op = parts[1]
        value = parts[2] if parts[2] != "" else parts[3]
        if op == '<=':
            condition = f"{feature} is **No**" if value == "0.50" else f"{feature} ≤ {value}"
        else:
            condition = f"{feature} is **Yes**" if value == "0.50" else f"{feature} > {value}"
        return rule_depth, f"IF {condition}"

def explain_tree(rules, clf, predictors, lbl):
    parsed_lines = rules.split('\n')
    translated = []
    current_path = []
    for line in parsed_lines:
        if not line.strip():
            continue
        depth, sentence = parse_rule_line(line, lbl)
        current_path = current_path[:depth]
        current_path.append(sentence)
        if sentence.startswith("THEN"):
            translated.append(" → ".join(current_path))
    leaf_ids = clf.apply(predictors)
    return leaf_ids, translated