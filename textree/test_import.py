#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import textree

tree = textree.TexTree()
root = tree.to_node('A\n\tA1')
for node in root.Nodes:
    print(node.Name)

from textree import TexTree
tree = TexTree()
root = tree.to_node('A\n\tA1')
for node in root.Nodes:
    print(node.Name)

