from memi.categories import CATEGORIES


def build_menu():
    """Build a nested menu structure from CATEGORIES keys.

    Returns (top_level, subcategories) where:
    - top_level: sorted list of {"label": ..., "key": ... or "has_submenu": True}
    - subcategories: dict of parent -> list of children
    """
    top_level_keys = set()
    subs = {}

    for key in CATEGORIES:
        parts = key.split(":")
        if len(parts) == 1:
            top_level_keys.add(key)
        elif len(parts) == 2:
            parent, label = parts
            top_level_keys.add(parent)
            subs.setdefault(parent, []).append({"key": key, "label": label})
        elif len(parts) == 3:
            parent, group, label = parts
            top_level_keys.add(parent)
            parent_list = subs.setdefault(parent, [])
            sub_group = None
            for item in parent_list:
                if item.get("label") == group and "children" in item:
                    sub_group = item
                    break
            if not sub_group:
                sub_group = {"label": group, "children": []}
                parent_list.append(sub_group)
            sub_group["children"].append({"key": key, "label": label})

    top_level = []
    for name in sorted(top_level_keys):
        if name in subs:
            top_level.append({"label": name, "has_submenu": True})
        else:
            top_level.append({"label": name, "key": name})

    for cat in subs:
        for item in subs[cat]:
            if "children" in item:
                item["children"].sort(key=lambda s: (s["label"] != "all", s["label"]))
        subs[cat].sort(key=lambda s: (s.get("label", "") != "all", s.get("label", "")))

    return top_level, subs
