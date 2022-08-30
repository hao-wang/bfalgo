import collections
import numpy as np
import numbers
from typing import Any, List, Dict, Union, NamedTuple


def most_frequent_value(elements: Any) -> Any:
    counts = collections.Counter(elements)
    return sorted(counts.items(), key=lambda d: d[1], reverse=True)[0][0]


def entropy(data: List[numbers.Number]) -> float:
    counts = np.array(list(collections.Counter(data).values()))
    total = len(data)
    return sum(-(counts / total) * np.log2(counts / total))


def predicate(predicate_name, value, pivot):
    if predicate_name == "==":
        return value == pivot
    else:
        return value >= pivot


class DecisionTree:
    class Split(NamedTuple):
        subtree: Dict
        feature: str
        pivot: Any
        predicate: str

    class Leaf(NamedTuple):
        category: str

    Tree = Union[Split, Leaf]

    def __init__(self, label_col: str, max_depth: int = 3):
        self.max_depth = max_depth
        self.min_leaf = 1
        self.label_col = label_col
        self.min_entropy_gain = 1e-1

    def most_frequent_label(self, data: List[Dict]):
        labels = [d[self.label_col] for d in data]
        return most_frequent_value(labels)

    def count_labels(self, data: List[Dict]):
        labels = [d[self.label_col] for d in data]
        return collections.Counter(labels)

    def get_entropy(self, data: List[Dict]):
        data_list = [d[self.label_col] for d in data]
        return entropy(data_list)

    def split(self, data: List[Dict], feature: str, pivot: Any) -> Dict:
        predicate_name = ">=" if isinstance(data[0][feature], numbers.Number) else "=="
        matched = []
        unmatched = []
        for d in data:
            if predicate(predicate_name, d[feature], pivot):
                matched.append(d)
            else:
                unmatched.append(d)

        return {"matched": matched, "unmatched": unmatched, "predicate": predicate_name}

    def build_tree(self, data: List[Dict]) -> Tree:
        if len(data) <= self.min_leaf:
            return self.Leaf(self.most_frequent_label(data))

        features = [f for f in data[0].keys() if f != self.label_col]

        checked_combo = set()
        old_entropy = self.get_entropy(data)
        maximum_entropy_gain = 0
        best_split = {}
        for ft in features:
            for dt in data:
                combo = "_".join([ft, str(dt[ft])])
                if combo not in checked_combo:
                    checked_combo.add(combo)
                    pivot = dt[ft]
                    new_split = self.split(data, ft, pivot)
                    new_entropy = (
                        len(new_split["matched"]) * self.get_entropy(new_split["matched"])
                        + len(new_split["unmatched"])
                        * self.get_entropy(new_split["unmatched"])
                    ) / len(data)
                    entropy_gain = old_entropy - new_entropy
                    if entropy_gain > maximum_entropy_gain:
                        maximum_entropy_gain = entropy_gain
                        print(new_split)
                        best_split = self.Split(
                            {
                                "matched": new_split["matched"],
                                "unmatched": new_split["unmatched"],
                            },
                            ft,
                            pivot,
                            new_split["predicate"],
                        )

        if maximum_entropy_gain < self.min_entropy_gain:
            prediction = self.most_frequent_label(data)
            return self.Leaf(prediction)

        matched_tree = self.build_tree(best_split.subtree["matched"])
        unmatched_tree = self.build_tree(best_split.subtree["unmatched"])
        return self.Split(
            {"matched": matched_tree, "unmatched": unmatched_tree},
            best_split.feature,
            best_split.pivot,
            best_split.predicate,
        )

    def fit(self, data: List[Dict]) -> None:
        self.tree = self.build_tree(data)

    def traverse_tree(self, tree: Tree, datapoint: Dict) -> str:
        print("current tree: {}".format(repr(tree)))
        try:
            feature = tree.feature
        except AttributeError:
            return tree.category
        else:
            pivot = tree.pivot
            if predicate(tree.predicate, datapoint[feature], pivot):
                return self.traverse_tree(tree.subtree["matched"], datapoint)
            else:
                return self.traverse_tree(tree.subtree["unmatched"], datapoint)

    def predict(self, datapoint: Dict) -> str:
        return self.traverse_tree(self.tree, datapoint)


if __name__ == "__main__":
    # mock data
    data = [
        {"length": 10, "keyword": "post", "last_height": 3, "label": "api"},
        {"length": 10, "keyword": "post", "last_height": 3, "label": "api"},
        {"length": 10, "keyword": "post", "last_height": 5, "label": "params"},
        {"length": 20, "keyword": "post", "last_height": 5, "label": "params"},
        {"length": 30, "keyword": "post", "last_height": 5, "label": "params"},
        {"length": 10, "keyword": "200", "last_height": 5, "label": "response"},
        {"length": 30, "keyword": "300", "last_height": 5, "label": "response"},
        {"length": 40, "keyword": "404", "last_height": 5, "label": "response"},
    ]

    model = DecisionTree(label_col="label")
    model.fit(data)

    print(model.tree)
    print(model.predict(data[0]))
    print(model.predict(data[2]))
    print(model.predict(data[5]))
