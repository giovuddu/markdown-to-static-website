from textnode import TextNode, TextType


def split_node_delimiter(
    old_node: TextNode, delimiter: str, text_type: TextType
) -> list[TextNode]:
    sp = old_node.text.split(delimiter, 1)

    if len(sp) <= 1:
        return [old_node]

    left = TextNode(sp[0], TextType.TEXT)
    mid_right_rev_text = sp[1][::-1]

    if delimiter not in mid_right_rev_text:
        raise Exception(f"unmatched delimiter found in {old_node.text}")

    mid_right_rev_sp = mid_right_rev_text.split(delimiter, 1)

    right = TextNode(mid_right_rev_sp[0][::-1], TextType.TEXT)
    mid = TextNode(mid_right_rev_sp[1][::-1], text_type)

    return [left, mid, right]


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    res = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            res += split_node_delimiter(node, delimiter, text_type)
        else:
            res += [node]

    return res
