#!/usr/bin/env python
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    from textree import TexTree, Node, NodeDeserializer, NodeSerializer
    tree_text = """
A
	A1
		A11
			A111
			A112
	A2
B
"""
    tree = TexTree()
    root = tree.to_node(tree_text)
    print(root, root.Name)
    for node in tree.Nodes:
        print(node.Name)
    for node in root.Nodes:
        print(node.Name)

    print('==============')
    class MyNodeDeserializer(NodeDeserializer):
        def deserialize(self, ana, parent, parents=Node):
            node = Node(ana.Line, parent=parent)
            node.my_name = 'My name is ' + node.Name
            return node
    tree = TexTree(node_deserializer=MyNodeDeserializer())
    root = tree.to_node(tree_text)
    for node in tree.Nodes:
        print(node.my_name)
    print(tree.to_text())

    class MyNodeSerializer(NodeSerializer):
        def serialize(self, node, parents=Node):
            indent_level = len(parents)
            indent_str = '' if 0 == len(parents) else TexTree.INDENT * indent_level
            return indent_str + '[' + node.Name + ']' + ('' if node.Attr is None else TexTree.INDENT + self.AttrSerializer.serialize(node.Attr))
    tree = TexTree(node_serializer=MyNodeSerializer())
    print(tree.to_text(tree.to_node(tree_text)))
