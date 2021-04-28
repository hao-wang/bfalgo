import math
import json


def predicate(name, first, second):
    """ Determine whether a condition is satisfied.

    Args:
        first: string or number
        second: string or number
        name: predicate name 
    Returns:
        A boolean. Examples:
        predicate(">=", 3, 3) # True
        predicate("==", 'hello', 'world') # False
    """
    if name == '==':
        return first == second
    elif name == '>=':
        return first >= second
    else:
        print("error!")
        return


def count_attr(data, attr):
    """ Count occurances of an attribute.

    Args:
    Returns:
        A dict.

    """
    counter = {}
    for d in data:
        counter[d[attr]] = counter.get(d[attr], 0) + 1

    return counter


def most_frequent_category(data, category_attr):
    counter = count_attr(data, category_attr)
    sorted_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    return sorted_counter[0][0]


def split(data, attr, predicateName, pivot):
    """Split data into matched and unmatched subgroup.

    Args:
    Returns:
        A dict. Example usage:
        >>> data = [{'color':red, 'size':3}, {'color':green, 'size':10}]
        >>> split(data, 'color', '==', 'red') 
        {'matched': {'color':red, 'size':3}, 'unmatched': {'color':green, 'size':10}}
    """
    matched = []
    unmatched = []

    for d in data:
        if predicate(predicateName, d[attr], pivot):
            matched.append(d)
        else:
            unmatched.append(d)
    return {"matched": matched, "unmatched": unmatched}


def entropy(data, category_attr):
    """ Get entropy of data based on category attribute.
    """
    counter = count_attr(data, category_attr)
    N = len(data)
    ent = 0
    for k in counter:
        c = counter[k]
        ent += -(c/N)*math.log(c/N)

    return ent


def build_decision_tree(data, category_attr):
    if (len(data) < min_leaf_size):
        return({"label": most_frequent_category(data, category_attr)})

    best_split = {
        "best_gain": 0,
    }
    for attr in data[0]:
        already_checked = set()

        if(attr == category_attr):
            continue

        if(isinstance(data[0][attr], str)):
            predicateName = '=='
        else:
            predicateName = '>='

        for d in data:
            pivot = d[attr]
            checking_id = attr+predicateName+str(pivot)
            if (checking_id in already_checked):
                continue
            else:
                already_checked.add(checking_id)

            new_split = split(data, attr, predicateName, pivot)
            current_entropy = entropy(data, category_attr)
            ratio_match = len(new_split['matched'])/len(data)
            new_entropy = \
                entropy(new_split['matched'], category_attr
                        )*ratio_match + \
                entropy(new_split['unmatched'], category_attr +
                        )*(1-ratio_match)
            new_gain = current_entropy - new_entropy

            if new_gain > best_split['best_gain']:
                best_split['best_gain'] = new_gain
                best_split['predicateName'] = predicateName
                best_split['pivot'] = pivot
                best_split['attribute'] = attr
                best_split['matched'] = new_split['matched']
                best_split['unmatched'] = new_split['unmatched']

    if(best_split['best_gain'] == 0):
        return {'label': most_frequent_category(data, category_attr)}

    matched = best_split['matched']
    matched_tree = build_decision_tree(matched, category_attr)

    unmatched = best_split['unmatched']
    unmatched_tree = build_decision_tree(unmatched, category_attr)

    return {
        'attribute': best_split['attribute'],
        'predicateName': best_split['predicateName'],
        'pivot': best_split['pivot'],
        'matched': matched_tree,
        'unmatched': unmatched_tree
    }
    

if __name__ == "__main__":
    # mock data
    data = [
       {'length': 10, 'keyword': 'post', 'last_height': 3, 'label': 'api'},
       {'length': 10, 'keyword': 'post', 'last_height': 3, 'label': 'api'},
       {'length': 10, 'keyword': 'post', 'last_height': 5, 'label': 'params'},
       {'length': 20, 'keyword': 'post', 'last_height': 5, 'label': 'params'},
       {'length': 30, 'keyword': 'post', 'last_height': 5, 'label': 'params'},
       {'length': 10, 'keyword': '200', 'last_height': 5, 'label': 'response'},
       {'length': 30, 'keyword': '300', 'last_height': 5, 'label': 'response'},
       {'length': 40, 'keyword': '404', 'last_height': 5, 'label': 'response'},
    ]

    min_leaf_size = 2

    model = build_decision_tree(data, 'label')
    print(json.dumps(model))
