#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import textree
from textree import TexTree, Node, NodeList, Path, RootNode, LineAnalizer
from collections import OrderedDict
class TestNode(unittest.TestCase):
    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            node = Node()
    def test_init_minimum(self):
        node = Node("A")
        def has_attr():
            self.assertTrue(hasattr(node, "Name"))
            self.assertTrue(hasattr(node, "Parent"))
            self.assertTrue(hasattr(node, "Children"))
        def is_type():
            self.assertTrue(isinstance(node.Name, str))
            self.assertTrue(isinstance(node.Children, NodeList))
            self.assertTrue(isinstance(node.Children, list))
        def is_value():
            self.assertEqual(0, len(node.Children))
            self.assertEqual("A", node.Name)
            self.assertEqual(None, node.Parent)
            self.assertEqual(0, len(node.Children))
        has_attr()
        is_type()
        is_value()
    def test_init_name_type_error(self):
        with self.assertRaises(Node.NameTypeError):
            node = Node("A", name=1)
    def test_init_name(self):
        node = Node("A", name="B")
        self.assertEqual("B", node.Name)
    def test_init_name_is_strip_of_line(self):
        node = Node("A ")
        self.assertEqual("A",  node.Name)
        node = Node("   A   ")
        self.assertEqual("A",       node.Name)
        node = Node("\t\tA\t\t")
        self.assertEqual("A",         node.Name)
    def test_init_parent_type_error(self):
        with self.assertRaises(Node.ParentTypeError):
            node = Node("A", parent="p")
    def test_init_parent(self):
        a  = Node("A")
        a1 = Node("A1", parent=a)
        self.assertEqual(None, a.Parent)
        self.assertEqual(a, a1.Parent)
    def test_init_children_type_error(self):
        with self.assertRaises(Node.ChildrenTypeError):
            node = Node("A", children="c")
        with self.assertRaises(Node.ChildrenTypeError):
            node = Node("A", children=1)
        with self.assertRaises(Node.ChildrenTypeError):
            node = Node("A", children="ABC")
        with self.assertRaises(Node.ChildrenTypeError):
            node = Node("A", children=Node('A1'))
    def test_init_child_type_error(self):
        with self.assertRaises(Node.ChildTypeError):
            node = Node("A", children=["c"])
        with self.assertRaises(Node.ChildTypeError):
            node = Node("A", children=[Node("c1"), "c2"])
        with self.assertRaises(Node.ChildTypeError):
            node = Node("A", children=["c1", Node("c2")])
        with self.assertRaises(Node.ChildTypeError):
            node = Node("A", children=[Node("c1"), 1])
    def test_init_children_list_zero(self):
        node = Node("A", children=[])
        self.assertTrue(isinstance(node.Children, list))
        self.assertEqual(0, len(node.Children))
    def test_init_children_list_one(self):
        node = Node("A", children=[Node('A')])
        self.assertTrue(isinstance(node.Children, list))
        self.assertEqual(1, len(node.Children))
        self.assertEqual('A', node.Children[0].Name)
    def test_init_children_list_two(self):
        node = Node("A", children=[Node('A'), Node('B')])
        self.assertTrue(isinstance(node.Children, list))
        self.assertEqual(2, len(node.Children))
        self.assertEqual('A', node.Children[0].Name)
        self.assertEqual('B', node.Children[1].Name)
    def test_init_children_node(self):
        node = Node("A", children=[Node("c1")])
        self.assertTrue(isinstance(node.Children, list))
        self.assertEqual(1, len(node.Children))
        self.assertEqual("c1", node.Children[0].Name)
    def test_init_children_NodeList(self):
        children = NodeList()
        children.append(Node("c1"))
        node = Node("A", children=children)
        self.assertTrue(isinstance(node.Children, list))
        self.assertEqual(1, len(node.Children))
        self.assertEqual("c1", node.Children[0].Name)
    def test_init_children_NodeList_from_list(self):
        children = NodeList([Node("c1")])
        node = Node("A", children=children)
        self.assertTrue(isinstance(node.Children, list))
        self.assertEqual(1, len(node.Children))
        self.assertEqual("c1", node.Children[0].Name)
    def test_init_children_NodeList_from_tuple(self):
        children = NodeList((Node("c1"),))
        node = Node("A", children=children)
        self.assertTrue(isinstance(node.Children, list))
        self.assertEqual(1, len(node.Children))
        self.assertEqual("c1", node.Children[0].Name)
    def test_init_children_NodeList_from_set(self):
        s = set(); s.add(Node("c1"))
        children = NodeList(s)
        node = Node("A", children=children)
        self.assertTrue(isinstance(node.Children, list))
        self.assertEqual(1, len(node.Children))
        self.assertEqual("c1", node.Children[0].Name)
    def test_init_children_NodeList_from_frozenset(self):
        s = set(); s.add(Node("c1")); fs = frozenset(s)
        children = NodeList(fs)
        node = Node("A", children=children)
        self.assertTrue(isinstance(node.Children, list))
        self.assertEqual(1, len(node.Children))
        self.assertEqual("c1", node.Children[0].Name)
    def test_init_children_NodeList_from_dict(self):
        children = NodeList({Node("c1"):'value'})
        node = Node("A", children=children)
        self.assertTrue(isinstance(node.Children, list))
        self.assertEqual(1, len(node.Children))
        self.assertEqual("c1", node.Children[0].Name)
    def test_init_children_NodeList_from_OrderedDict(self):
        od = OrderedDict(); od[Node("c1")] = 'value';
        children = NodeList(od)
        node = Node("A", children=children)
        self.assertTrue(isinstance(node.Children, list))
        self.assertEqual(1, len(node.Children))
        self.assertEqual("c1", node.Children[0].Name)
    def test_init_path(self):
        root = RootNode()
        A = Node('A', parent=root)
        A1 = Node('A1', parent=A)
        A11 = Node('A11', parent=A1)
        self.assertEqual('', root.Path)
        self.assertEqual('A', A.Path)
        self.assertEqual('A/A1', A1.Path)
        self.assertEqual('A/A1/A11', A11.Path)
    def test_init_attr(self):
        node = Node('A', attr='attr1')
        self.assertEqual('attr1', node.Attr)
    def test_init_index(self):
        root = RootNode()
        A = Node('A', parent=root)
        B = Node('B', parent=root)
        A1 = Node('A1', parent=A)
        A2 = Node('A2', parent=A)
        A11 = Node('A11', parent=A1)
        A12 = Node('A12', parent=A1)
        root.Children.append(A)
        root.Children.append(B)
        A.Children.append(A1)
        A.Children.append(A2)
        A1.Children.append(A11)
        A1.Children.append(A12)
        self.assertEqual(0, root.Index)
        self.assertEqual(0, A.Index)
        self.assertEqual(1, B.Index)
        self.assertEqual(0, A1.Index)
        self.assertEqual(1, A2.Index)
        self.assertEqual(0, A11.Index)
        self.assertEqual(1, A12.Index)

class TestNodePath(unittest.TestCase):
    def get_brosers(self):
        root = RootNode(TexTree.ROOT_NAME)
        A = Node('A', parent=root)
        B = Node('B', parent=root)
        C = Node('C', parent=root)
        root.Children.append(A)
        root.Children.append(B)
        root.Children.append(C)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        return root, A, B, C
    def get_parents(self):
        root = RootNode(TexTree.ROOT_NAME)
        A = Node('A', parent=root)
        A1 = Node('A1', parent=A)
        B = Node('B', parent=root)
        B1 = Node('B1', parent=B)
        root.Children.append(A)
        root.Children.append(B)
        A.Children.append(A1)
        B.Children.append(B1)
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(1, len(root.Children[0].Children))
        self.assertEqual(1, len(root.Children[1].Children))
        self.assertEqual('A1', root.Children[0].Children[0].Name)
        self.assertEqual('B1', root.Children[1].Children[0].Name)
        return root, A, A1, B, B1
    def get_grand_parents(self):
        root = RootNode(TexTree.ROOT_NAME)
        A = Node('A', parent=root)
        A1 = Node('A1', parent=A)
        A11 = Node('A11', parent=A1)
        B = Node('B', parent=root)
        B1 = Node('B1', parent=B)
        B11 = Node('B11', parent=B1)
        B12 = Node('B12', parent=B1)
        root.Children.append(A)
        root.Children.append(B)
        A.Children.append(A1)
        B.Children.append(B1)
        A1.Children.append(A11)
        B1.Children.append(B11)
        B1.Children.append(B12)
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(1, len(root.Children[0].Children))
        self.assertEqual(1, len(root.Children[1].Children))
        self.assertEqual('A1', root.Children[0].Children[0].Name)              # A/A1
        self.assertEqual('B1', root.Children[1].Children[0].Name)              # B/B1
        self.assertEqual(1, len(root.Children[0].Children[0].Children))
        self.assertEqual(2, len(root.Children[1].Children[0].Children))
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name) # A/A1/A11
        self.assertEqual('B11', root.Children[1].Children[0].Children[0].Name) # B/B1/B11
        self.assertEqual('B12', root.Children[1].Children[0].Children[1].Name) # B/B1/B12
        return root, A, A1, A11, B, B1, B11, B12
    def get_grand_parents_brothers(self):
        root = RootNode(TexTree.ROOT_NAME)
        A = Node('A', parent=root)
        A1 = Node('A1', parent=A)
        A11 = Node('A11', parent=A1)
        A12 = Node('A12', parent=A1)
        A13 = Node('A13', parent=A1)
        A2 = Node('A2', parent=A)
        A21 = Node('A21', parent=A2)
        A22 = Node('A22', parent=A2)
        A23 = Node('A23', parent=A2)
        A3 = Node('A3', parent=A)
        A31 = Node('A31', parent=A3)
        A32 = Node('A32', parent=A3)
        A33 = Node('A33', parent=A3)
        B = Node('B', parent=root)
        B1 = Node('B1', parent=B)
        B11 = Node('B11', parent=B1)
        B12 = Node('B12', parent=B1)
        B13 = Node('B13', parent=B1)
        B2 = Node('B2', parent=B)
        B21 = Node('B21', parent=B2)
        B22 = Node('B22', parent=B2)
        B23 = Node('B23', parent=B2)
        B3 = Node('B3', parent=B)
        B31 = Node('B31', parent=B3)
        B32 = Node('B32', parent=B3)
        B33 = Node('B33', parent=B3)
        C = Node('C', parent=root)
        C1 = Node('C1', parent=C)
        C11 = Node('C11', parent=C1)
        C12 = Node('C12', parent=C1)
        C13 = Node('C13', parent=C1)
        C2 = Node('C2', parent=C)
        C21 = Node('C21', parent=C2)
        C22 = Node('C22', parent=C2)
        C23 = Node('C23', parent=C2)
        C3 = Node('C3', parent=C)
        C31 = Node('C31', parent=C3)
        C32 = Node('C32', parent=C3)
        C33 = Node('C33', parent=C3)
        root.Children.append(A)
        root.Children.append(B)
        root.Children.append(C)
        A.Children.append(A1)
        A.Children.append(A2)
        A.Children.append(A3)
        B.Children.append(B1)
        B.Children.append(B2)
        B.Children.append(B3)
        C.Children.append(C1)
        C.Children.append(C2)
        C.Children.append(C3)
        A1.Children.append(A11)
        A1.Children.append(A12)
        A1.Children.append(A13)
        A2.Children.append(A21)
        A2.Children.append(A22)
        A2.Children.append(A23)
        A3.Children.append(A31)
        A3.Children.append(A32)
        A3.Children.append(A33)

        B1.Children.append(B11)
        B1.Children.append(B12)
        B1.Children.append(B13)
        B2.Children.append(B21)
        B2.Children.append(B22)
        B2.Children.append(B23)
        B3.Children.append(B31)
        B3.Children.append(B32)
        B3.Children.append(B33)

        C1.Children.append(C11)
        C1.Children.append(C12)
        C1.Children.append(C13)
        C2.Children.append(C21)
        C2.Children.append(C22)
        C2.Children.append(C23)
        C3.Children.append(C31)
        C3.Children.append(C32)
        C3.Children.append(C33)

        self.assertEqual(3, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        self.assertEqual(3, len(root.Children[0].Children))
        self.assertEqual(3, len(root.Children[1].Children))
        self.assertEqual(3, len(root.Children[2].Children))
        self.assertEqual('A1', root.Children[0].Children[0].Name)              # A/A1
        self.assertEqual('B1', root.Children[1].Children[0].Name)              # B/B1
        self.assertEqual('C1', root.Children[2].Children[0].Name)              # B/B1
        self.assertEqual(3, len(root.Children[0].Children[0].Children))
        self.assertEqual(3, len(root.Children[1].Children[0].Children))
        self.assertEqual(3, len(root.Children[2].Children[0].Children))
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name) # A/A1/A11
        self.assertEqual('B11', root.Children[1].Children[0].Children[0].Name) # B/B1/B11
        self.assertEqual('C11', root.Children[2].Children[0].Children[0].Name) # C/C1/C11
        return root, A, A1, A11, A12, A13, A2, A21, A22, A23, A3, A31, A32, A33, B, B1, B11, B12, B2, B21, B22, B23, B3, B31, B32, B33, C, C1, C11, C12, C13, C2, C21, C22, C23, C3, C31, C32, C33

    def test_DELEMITER_read_only(self):
        with self.assertRaises(AttributeError):
            Path.DELIMITER = ':'

    def test_Path_select_type_error(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(TypeError):
            Path.select(root, None)
        with self.assertRaises(TypeError):
            Path.select(0, './')

    def test_Path_select_root_relative_this(self):
        root, A, B, C = self.get_brosers()
        self.assertEqual(root, Path.select(root, './'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(root, '../'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(root, '../../'))
        self.assertEqual(A, Path.select(root, 'A'))
        self.assertEqual(B, Path.select(root, 'B'))
        self.assertEqual(C, Path.select(root, 'C'))
        self.assertEqual(A, Path.select(root, './A'))
        self.assertEqual(B, Path.select(root, './B'))
        self.assertEqual(C, Path.select(root, './C'))
        self.assertEqual(root, Path.select(A, '../'))
        self.assertEqual(root, Path.select(B, '../'))
        self.assertEqual(root, Path.select(C, '../'))
        self.assertEqual(A, Path.select(A, '../A'))
        self.assertEqual(B, Path.select(A, '../B'))
        self.assertEqual(C, Path.select(A, '../C'))
        self.assertEqual(A, Path.select(B, '../A'))
        self.assertEqual(B, Path.select(B, '../B'))
        self.assertEqual(C, Path.select(B, '../C'))
        self.assertEqual(A, Path.select(C, '../A'))
        self.assertEqual(B, Path.select(C, '../B'))
        self.assertEqual(C, Path.select(C, '../C'))

    def test_Path_select_root_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        self.assertEqual(root, Path.select(root, './'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(root, '../'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(root, '../../'))
        self.assertEqual(A, Path.select(root, 'A'))
        self.assertEqual(B, Path.select(root, 'B'))
        with self.assertRaises(ValueError):
            self.assertEqual(None, Path.select(root, 'C'))
        self.assertEqual(A, Path.select(root, './A'))
        self.assertEqual(B, Path.select(root, './B'))
        self.assertEqual(A1, Path.select(A1, './'))
        self.assertEqual(B1, Path.select(B1, './'))
        self.assertEqual(A, Path.select(A1, '../'))
        self.assertEqual(B, Path.select(B1, '../'))
        self.assertEqual(root, Path.select(A1, '../../'))
        self.assertEqual(root, Path.select(B1, '../../'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(A1, '../../../'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(B1, '../../../'))

    def test_Path_select_root_relative_grand_parent(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        self.assertEqual(root, Path.select(root, './'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(root, '../'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(root, '../../'))
        self.assertEqual(A, Path.select(root, 'A'))
        self.assertEqual(B, Path.select(root, 'B'))
        with self.assertRaises(ValueError):
            self.assertEqual(None, Path.select(root, 'C'))
        self.assertEqual(A, Path.select(root, './A'))
        self.assertEqual(B, Path.select(root, './B'))

        self.assertEqual(A11, Path.select(A11, './'))
        self.assertEqual(B11, Path.select(B11, './'))
        self.assertEqual(B12, Path.select(B12, './'))
        self.assertEqual(A1, Path.select(A11, '../'))
        self.assertEqual(B1, Path.select(B11, '../'))
        self.assertEqual(B1, Path.select(B12, '../'))
        self.assertEqual(A, Path.select(A11, '../../'))
        self.assertEqual(B, Path.select(B11, '../../'))
        self.assertEqual(B, Path.select(B12, '../../'))
        self.assertEqual(root, Path.select(A11, '../../../'))
        self.assertEqual(root, Path.select(B11, '../../../'))
        self.assertEqual(root, Path.select(B12, '../../../'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(A11, '../../../../'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(B11, '../../../../'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(B12, '../../../../'))
        self.assertEqual(B11, Path.select(B12, '../B11'))
        self.assertEqual(A11, Path.select(B12, '../../../A/A1/A11'))

        self.assertEqual(A1, Path.select(A1, './'))
        self.assertEqual(B1, Path.select(B1, './'))
        self.assertEqual(A, Path.select(A1, '../'))
        self.assertEqual(B, Path.select(B1, '../'))
        self.assertEqual(root, Path.select(A1, '../../'))
        self.assertEqual(root, Path.select(B1, '../../'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(A1, '../../../'))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.select(B1, '../../../'))

    def test_Path_index_brosers(self):
        root, A, B, C = self.get_brosers()
        self.assertEqual(0, Path.index(root))
        self.assertEqual(0, Path.index(A))
        self.assertEqual(1, Path.index(B))
        self.assertEqual(2, Path.index(C))
    def test_Path_index_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        self.assertEqual(0, Path.index(root))
        self.assertEqual(0, Path.index(A))
        self.assertEqual(1, Path.index(B))
        self.assertEqual(0, Path.index(A1))
        self.assertEqual(0, Path.index(B1))
    def test_Path_index_grand_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        self.assertEqual(0, Path.index(root))
        self.assertEqual(0, Path.index(A))
        self.assertEqual(1, Path.index(B))
        self.assertEqual(0, Path.index(A1))
        self.assertEqual(0, Path.index(B1))
        self.assertEqual(0, Path.index(A11))
        self.assertEqual(0, Path.index(B11))
        self.assertEqual(1, Path.index(B12))
    def test_Path_index_path_brosers(self):
        root, A, B, C = self.get_brosers()
        self.assertEqual(0, Path.index(root, './'))
        self.assertEqual(0, Path.index(A, './'))
        self.assertEqual(1, Path.index(B, './'))
        self.assertEqual(2, Path.index(C, './'))
        with self.assertRaises(ValueError):
            self.assertEqual(0, Path.index(root, '../'))
        self.assertEqual(0, Path.index(A, '../'))
        self.assertEqual(0, Path.index(B, '../'))
        self.assertEqual(0, Path.index(C, '../'))
        self.assertEqual(0, Path.index(root, 'A'))
        self.assertEqual(1, Path.index(root, 'B'))
        self.assertEqual(2, Path.index(root, 'C'))
        self.assertEqual(0, Path.index(root, './A'))
        self.assertEqual(1, Path.index(root, './B'))
        self.assertEqual(2, Path.index(root, './C'))
        self.assertEqual(0, Path.index(A, '../A'))
        self.assertEqual(1, Path.index(A, '../B'))
        self.assertEqual(2, Path.index(A, '../C'))
        self.assertEqual(0, Path.index(B, '../A'))
        self.assertEqual(1, Path.index(B, '../B'))
        self.assertEqual(2, Path.index(B, '../C'))
        self.assertEqual(0, Path.index(C, '../A'))
        self.assertEqual(1, Path.index(C, '../B'))
        self.assertEqual(2, Path.index(C, '../C'))
        with self.assertRaises(ValueError):
            self.assertEqual(0, Path.index(A, '../../'))
    def test_Path_index_path_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        self.assertEqual(0, Path.index(root, './'))
        self.assertEqual(0, Path.index(A, './'))
        self.assertEqual(1, Path.index(B, './'))
        self.assertEqual(0, Path.index(A1, './'))
        self.assertEqual(0, Path.index(B1, './'))
        with self.assertRaises(ValueError):
            self.assertEqual(0, Path.index(root, '../'))
        self.assertEqual(0, Path.index(A, '../'))
        self.assertEqual(0, Path.index(B, '../'))
        self.assertEqual(0, Path.index(A1, '../../'))
        self.assertEqual(0, Path.index(B1, '../../'))
        self.assertEqual(0, Path.index(A1, '../'))
        self.assertEqual(1, Path.index(B1, '../'))
        self.assertEqual(0, Path.index(root, 'A'))
        self.assertEqual(1, Path.index(root, 'B'))
        self.assertEqual(0, Path.index(root, './A'))
        self.assertEqual(1, Path.index(root, './B'))
        self.assertEqual(0, Path.index(root, 'A/A1'))
        self.assertEqual(0, Path.index(root, 'B/B1'))
        self.assertEqual(0, Path.index(root, './A/A1'))
        self.assertEqual(0, Path.index(root, './B/B1'))

        self.assertEqual(0, Path.index(A, '../A'))
        self.assertEqual(1, Path.index(A, '../B'))
        self.assertEqual(0, Path.index(B, '../A'))
        self.assertEqual(1, Path.index(B, '../B'))
        self.assertEqual(0, Path.index(A, '../A/A1'))
        self.assertEqual(1, Path.index(A, '../B'))
        self.assertEqual(0, Path.index(A, '../B/B1'))
        self.assertEqual(0, Path.index(B, '../A'))
        self.assertEqual(0, Path.index(B, '../A/A1'))
        self.assertEqual(0, Path.index(B, '../B/B1'))
        with self.assertRaises(ValueError):
            self.assertEqual(0, Path.index(A, '../../'))
    def test_Path_index_path_grand_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        self.assertEqual(0, Path.index(root, './'))
        self.assertEqual(0, Path.index(A, './'))
        self.assertEqual(1, Path.index(B, './'))
        self.assertEqual(0, Path.index(A1, './'))
        self.assertEqual(0, Path.index(B1, './'))
        self.assertEqual(0, Path.index(A11, './'))
        self.assertEqual(0, Path.index(B11, './'))
        self.assertEqual(1, Path.index(B12, './'))
        with self.assertRaises(ValueError):
            self.assertEqual(0, Path.index(root, '../'))
        self.assertEqual(0, Path.index(A, '../'))
        self.assertEqual(0, Path.index(B, '../'))
        self.assertEqual(0, Path.index(A1, '../../'))
        self.assertEqual(0, Path.index(B1, '../../'))
        self.assertEqual(0, Path.index(A1, '../'))
        self.assertEqual(1, Path.index(B1, '../'))
        self.assertEqual(0, Path.index(root, 'A'))
        self.assertEqual(1, Path.index(root, 'B'))
        self.assertEqual(0, Path.index(root, './A'))
        self.assertEqual(1, Path.index(root, './B'))
        self.assertEqual(0, Path.index(root, 'A/A1'))
        self.assertEqual(0, Path.index(root, 'B/B1'))
        self.assertEqual(0, Path.index(root, './A/A1'))
        self.assertEqual(0, Path.index(root, './B/B1'))
        self.assertEqual(0, Path.index(root, './A/A1/A11'))
        self.assertEqual(0, Path.index(root, './B/B1/B11'))
        self.assertEqual(1, Path.index(root, './B/B1/B12'))

        self.assertEqual(0, Path.index(A, '../A'))
        self.assertEqual(1, Path.index(A, '../B'))
        self.assertEqual(0, Path.index(B, '../A'))
        self.assertEqual(1, Path.index(B, '../B'))
        self.assertEqual(0, Path.index(A, '../A/A1'))
        self.assertEqual(1, Path.index(A, '../B'))
        self.assertEqual(0, Path.index(A, '../B/B1'))
        self.assertEqual(0, Path.index(B, '../A'))
        self.assertEqual(0, Path.index(B, '../A/A1'))
        self.assertEqual(0, Path.index(B, '../B/B1'))
        self.assertEqual(0, Path.index(A, '../A/A1/A11'))
        self.assertEqual(0, Path.index(A, '../B/B1/B11'))
        self.assertEqual(1, Path.index(A, '../B/B1/B12'))
        self.assertEqual(0, Path.index(B, '../A/A1/A11'))
        self.assertEqual(0, Path.index(B, '../B/B1/B11'))
        self.assertEqual(1, Path.index(B, '../B/B1/B12'))

        with self.assertRaises(ValueError):
            self.assertEqual(0, Path.index(A, '../../'))
        with self.assertRaises(ValueError):
            self.assertEqual(0, Path.index(A1, '../../../'))
        with self.assertRaises(ValueError):
            self.assertEqual(0, Path.index(A11, '../../../../'))
   
    def test_Path_get_ancestor_brosers(self):
        root, A, B, C = self.get_brosers()
        self.assertEqual(root, Path.get_ancestor(root, 0))
        with self.assertRaises(ValueError):
            self.assertEqual(0, Path.get_ancestor(root, 1))
        with self.assertRaises(ValueError):
            self.assertEqual(0, Path.get_ancestor(root, -1))
        self.assertEqual(A, Path.get_ancestor(A, 0))
        self.assertEqual(B, Path.get_ancestor(B, 0))
        self.assertEqual(C, Path.get_ancestor(C, 0))
        self.assertEqual(root, Path.get_ancestor(A, 1))
        self.assertEqual(root, Path.get_ancestor(B, 1))
        self.assertEqual(root, Path.get_ancestor(C, 1))
        self.assertEqual(root, Path.get_ancestor(A, -1))
        self.assertEqual(root, Path.get_ancestor(B, -1))
        self.assertEqual(root, Path.get_ancestor(C, -1))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.get_ancestor(A, 2))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.get_ancestor(B, 2))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.get_ancestor(C, 2))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.get_ancestor(A, -2))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.get_ancestor(B, -2))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.get_ancestor(C, -2))

    def test_Path_get_ancestor_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        self.assertEqual(A1, Path.get_ancestor(A1, 0))
        self.assertEqual(B1, Path.get_ancestor(B1, 0))
        self.assertEqual(A, Path.get_ancestor(A1, 1))
        self.assertEqual(B, Path.get_ancestor(B1, 1))
        self.assertEqual(root, Path.get_ancestor(A1, 2))
        self.assertEqual(root, Path.get_ancestor(B1, 2))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.get_ancestor(A1, 3))
        with self.assertRaises(ValueError):
            self.assertEqual(root, Path.get_ancestor(B1, 3))
    def test_Path_get_ancestor_grand_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        self.assertEqual(A11, Path.get_ancestor(A11, 0))
        self.assertEqual(A1, Path.get_ancestor(A11, 1))
        self.assertEqual(A, Path.get_ancestor(A11, 2))
        self.assertEqual(root, Path.get_ancestor(A11, 3))
        with self.assertRaises(ValueError):
            self.assertEqual(None, Path.get_ancestor(A11, 4))
        self.assertEqual(B11, Path.get_ancestor(B11, 0))
        self.assertEqual(B1, Path.get_ancestor(B11, 1))
        self.assertEqual(B, Path.get_ancestor(B11, 2))
        self.assertEqual(root, Path.get_ancestor(B11, 3))
        with self.assertRaises(ValueError):
            self.assertEqual(None, Path.get_ancestor(B11, 4))
    def test_Path_get_path_brosers(self):
        root, A, B, C = self.get_brosers()
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual('', Path.get_path(root))
        self.assertEqual(Path.DELIMITER.join([A.Name]), Path.get_path(A))
        self.assertEqual(Path.DELIMITER.join([B.Name]), Path.get_path(B))
        self.assertEqual(Path.DELIMITER.join([C.Name]), Path.get_path(C))
        with self.assertRaises(ValueError):
            Path.get_path(None)
        with self.assertRaises(ValueError):
            Path.get_path(1)
        with self.assertRaises(ValueError):
            Path.get_path('A')
    def test_Path_get_ancestor_path_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        self.assertEqual('', Path.get_path(root))
        self.assertEqual(Path.DELIMITER.join([A.Name]), Path.get_path(A))
        self.assertEqual(Path.DELIMITER.join([B.Name]), Path.get_path(B))
        self.assertEqual(Path.DELIMITER.join([A.Name,A1.Name]), Path.get_path(A1))
        self.assertEqual(Path.DELIMITER.join([B.Name,B1.Name]), Path.get_path(B1))
    def test_Path_get_ancestor_path_grand_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        self.assertEqual('', Path.get_path(root))
        self.assertEqual(Path.DELIMITER.join([A.Name]), Path.get_path(A))
        self.assertEqual(Path.DELIMITER.join([B.Name]), Path.get_path(B))
        self.assertEqual(Path.DELIMITER.join([A.Name,A1.Name]), Path.get_path(A1))
        self.assertEqual(Path.DELIMITER.join([B.Name,B1.Name]), Path.get_path(B1))
        self.assertEqual(Path.DELIMITER.join([A.Name,A1.Name,A11.Name]), Path.get_path(A11))
        self.assertEqual(Path.DELIMITER.join([B.Name,B1.Name,B11.Name]), Path.get_path(B11))
        self.assertEqual(Path.DELIMITER.join([B.Name,B1.Name,B12.Name]), Path.get_path(B12))

    def test_to_first_none(self):
        root, A, B, C = self.get_brosers()
        C.to_first()
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        B.to_first()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_first()
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_first()
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
    def test_to_first_relative_this(self):
        root, A, B, C = self.get_brosers()
        C.to_first('./')
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        B.to_first('./')
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_first('./')
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_first('./')
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
    def test_to_first_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        B1.to_first('../../A')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('B1',root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual(0, len(root.Children[0].Children)) # B1
        self.assertEqual(1, len(root.Children[1].Children)) # A
        self.assertEqual(0, len(root.Children[2].Children)) # B
        self.assertEqual('A1', root.Children[1].Children[0].Name)
    def test_to_first_relative_grand_parent(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B11.to_first('../../../A/A1')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(2, len(root.Children[0].Children)) # A
        self.assertEqual(1, len(root.Children[1].Children)) # B
        self.assertEqual('B11',root.Children[0].Children[0].Name)              # A/B11
        self.assertEqual('A1', root.Children[0].Children[1].Name)              # A/A1
        self.assertEqual('B1', root.Children[1].Children[0].Name)              # B/B1
        self.assertEqual(0, len(root.Children[0].Children[0].Children)) # A/B11
        self.assertEqual(1, len(root.Children[0].Children[1].Children)) # A/A1
        self.assertEqual(1, len(root.Children[1].Children[0].Children)) # B/B1
        self.assertEqual('A11', root.Children[0].Children[1].Children[0].Name) # A/A1/A11
        self.assertEqual('B12', root.Children[1].Children[0].Children[0].Name) # B/B1/B12
    def test_to_first_over_ancestor(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_first('../../')
    def test_to_first_relative_grand_parent_brother(self):
        root, A, A1, A11, A12, A13, A2, A21, A22, A23, A3, A31, A32, A33, B, B1, B11, B12, B2, B21, B22, B23, B3, B31, B32, B33, C, C1, C11, C12, C13, C2, C21, C22, C23, C3, C31, C32, C33 = self.get_grand_parents_brothers()
        B11.to_first('../../../A/A1/A11')
        self.assertEqual(4, len(A1.Children))
        self.assertEqual('B11', A1.Children[0].Name)
        self.assertEqual('A11', A1.Children[1].Name)
        self.assertEqual('A12', A1.Children[2].Name)
        self.assertEqual('A13', A1.Children[3].Name)
        self.assertEqual(2, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        self.assertEqual('B13', B1.Children[1].Name)

    def test_to_last_none(self):
        root, A, B, C = self.get_brosers()
        A.to_last()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_last()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        C.to_last()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
    def test_to_last_relative_this(self):
        root, A, B, C = self.get_brosers()
        A.to_last('./')
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_last('./')
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        C.to_last('./')
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
    def test_to_last_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        B1.to_last('../../A')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('B1', root.Children[2].Name)
        self.assertEqual(1, len(root.Children[0].Children))
        self.assertEqual(0, len(root.Children[1].Children))
        self.assertEqual('A1', root.Children[0].Children[0].Name)
    def test_to_last_relative_grand_parent(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B11.to_last('../../../A/A1')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(2, len(root.Children[0].Children))
        self.assertEqual(1, len(root.Children[1].Children))
        self.assertEqual('A1', root.Children[0].Children[0].Name)              # A/A1
        self.assertEqual('B11',root.Children[0].Children[1].Name)              # A/B11
        self.assertEqual('B1', root.Children[1].Children[0].Name)              # B/B1
        self.assertEqual(1, len(root.Children[0].Children[0].Children)) # A/A1
        self.assertEqual(0, len(root.Children[0].Children[1].Children)) # A/B11
        self.assertEqual(1, len(root.Children[1].Children[0].Children)) # B/B1
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name) # A/A1/A11
        self.assertEqual('B12', root.Children[1].Children[0].Children[0].Name) # B/B1/B12
    def test_to_last_over_ancestor(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_last('../../')
    def test_to_last_relative_grand_parent_brother(self):
        root, A, A1, A11, A12, A13, A2, A21, A22, A23, A3, A31, A32, A33, B, B1, B11, B12, B2, B21, B22, B23, B3, B31, B32, B33, C, C1, C11, C12, C13, C2, C21, C22, C23, C3, C31, C32, C33 = self.get_grand_parents_brothers()
        B11.to_last('../../../A/A1/A11')
        self.assertEqual(4, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        self.assertEqual('A13', A1.Children[2].Name)
        self.assertEqual('B11', A1.Children[3].Name)
        self.assertEqual(2, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        self.assertEqual('B13', B1.Children[1].Name)

    def test_to_next_none(self):
        root, A, B, C = self.get_brosers()
        A.to_next()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        A.to_next()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        A.to_next()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
    def test_to_next_relative_this(self):
        root, A, B, C = self.get_brosers()
        A.to_next('./')
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        A.to_next('./')
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        A.to_next('./')
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
    def test_to_next_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        B1.to_next('../')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('B1', root.Children[2].Name)
        self.assertEqual(1, len(root.Children[0].Children))
        self.assertEqual(0, len(root.Children[1].Children))
        self.assertEqual(0, len(root.Children[0].Children[0].Children)) # A/A1
        self.assertEqual(0, len(root.Children[1].Children)) # B
        self.assertEqual(0, len(root.Children[2].Children)) # B1
    def test_to_next_relative_grand_parent(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B11.to_next('../../../A/A1')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(2, len(root.Children[0].Children)) # A
        self.assertEqual(1, len(root.Children[1].Children)) # B
        self.assertEqual('A1', root.Children[0].Children[0].Name)              # A/A1
        self.assertEqual('B11',root.Children[0].Children[1].Name)              # A/A1
        self.assertEqual('B1', root.Children[1].Children[0].Name)              # B/B1
        self.assertEqual(1, len(root.Children[0].Children[0].Children)) # A/A1
        self.assertEqual(0, len(root.Children[0].Children[1].Children)) # A/B11
        self.assertEqual(1, len(root.Children[0].Children[0].Children)) # B/B1
        self.assertEqual(1, len(root.Children[1].Children[0].Children))
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name) # A/A1/B11
        self.assertEqual('B12', root.Children[1].Children[0].Children[0].Name) # B/B1/B12
    def test_to_next_over_ancestor(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_next('../../')
    def test_to_next_relative_grand_parent_brother(self):
        root, A, A1, A11, A12, A13, A2, A21, A22, A23, A3, A31, A32, A33, B, B1, B11, B12, B2, B21, B22, B23, B3, B31, B32, B33, C, C1, C11, C12, C13, C2, C21, C22, C23, C3, C31, C32, C33 = self.get_grand_parents_brothers()
        B11.to_next('../../../A/A1/A11')
        self.assertEqual(4, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('B11', A1.Children[1].Name)
        self.assertEqual('A12', A1.Children[2].Name)
        self.assertEqual('A13', A1.Children[3].Name)
        self.assertEqual(2, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        self.assertEqual('B13', B1.Children[1].Name)

        root, A, A1, A11, A12, A13, A2, A21, A22, A23, A3, A31, A32, A33, B, B1, B11, B12, B2, B21, B22, B23, B3, B31, B32, B33, C, C1, C11, C12, C13, C2, C21, C22, C23, C3, C31, C32, C33 = self.get_grand_parents_brothers()
        B11.to_next('../../../A/A1/A12')
        self.assertEqual(4, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        self.assertEqual('B11', A1.Children[2].Name)
        self.assertEqual('A13', A1.Children[3].Name)
        self.assertEqual(2, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        self.assertEqual('B13', B1.Children[1].Name)

        root, A, A1, A11, A12, A13, A2, A21, A22, A23, A3, A31, A32, A33, B, B1, B11, B12, B2, B21, B22, B23, B3, B31, B32, B33, C, C1, C11, C12, C13, C2, C21, C22, C23, C3, C31, C32, C33 = self.get_grand_parents_brothers()
        B11.to_next('../../../A/A1/A13')
        self.assertEqual(4, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        self.assertEqual('A13', A1.Children[2].Name)
        self.assertEqual('B11', A1.Children[3].Name)
        self.assertEqual(2, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        self.assertEqual('B13', B1.Children[1].Name)



    def test_to_prev_none(self):
        root, A, B, C = self.get_brosers()
        C.to_prev()
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        C.to_prev()
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        C.to_prev()
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
    def test_to_prev_relative_this(self):
        root, A, B, C = self.get_brosers()
        C.to_prev('./')
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        C.to_prev('./')
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        C.to_prev('./')
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
    def test_to_prev_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        B1.to_prev('../')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B1', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual(1, len(root.Children[0].Children))
        self.assertEqual(0, len(root.Children[1].Children))
        self.assertEqual(0, len(root.Children[2].Children))
        self.assertEqual(0, len(root.Children[0].Children[0].Children)) # A/A1
    def test_to_prev_relative_grand_parent(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B11.to_prev('../../../A/A1')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(2, len(root.Children[0].Children)) # A
        self.assertEqual(1, len(root.Children[1].Children)) # B
        self.assertEqual('B11',root.Children[0].Children[0].Name)              # A/B11
        self.assertEqual('A1', root.Children[0].Children[1].Name)              # A/A1
        self.assertEqual('B1', root.Children[1].Children[0].Name)              # B/B1
        self.assertEqual(0, len(root.Children[0].Children[0].Children)) # A/B11
        self.assertEqual(1, len(root.Children[0].Children[1].Children)) # A/A1
        self.assertEqual(1, len(root.Children[1].Children[0].Children))
        self.assertEqual('A11', root.Children[0].Children[1].Children[0].Name) # A/A1/B11
        self.assertEqual('B12', root.Children[1].Children[0].Children[0].Name) # B/B1/B12
    def test_to_prev_over_ancestor(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_prev('../../')
    def test_to_prev_relative_grand_parent_brother(self):
        root, A, A1, A11, A12, A13, A2, A21, A22, A23, A3, A31, A32, A33, B, B1, B11, B12, B2, B21, B22, B23, B3, B31, B32, B33, C, C1, C11, C12, C13, C2, C21, C22, C23, C3, C31, C32, C33 = self.get_grand_parents_brothers()
        B11.to_prev('../../../A/A1/A11')
        self.assertEqual(4, len(A1.Children))
        self.assertEqual('B11', A1.Children[0].Name)              # A/B11
        self.assertEqual('A11', A1.Children[1].Name)
        self.assertEqual('A12', A1.Children[2].Name)
        self.assertEqual('A13', A1.Children[3].Name)
        self.assertEqual(2, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        self.assertEqual('B13', B1.Children[1].Name)

        root, A, A1, A11, A12, A13, A2, A21, A22, A23, A3, A31, A32, A33, B, B1, B11, B12, B2, B21, B22, B23, B3, B31, B32, B33, C, C1, C11, C12, C13, C2, C21, C22, C23, C3, C31, C32, C33 = self.get_grand_parents_brothers()
        B11.to_prev('../../../A/A1/A12')
        self.assertEqual(4, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('B11', A1.Children[1].Name)
        self.assertEqual('A12', A1.Children[2].Name)
        self.assertEqual('A13', A1.Children[3].Name)
        self.assertEqual(2, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        self.assertEqual('B13', B1.Children[1].Name)

        root, A, A1, A11, A12, A13, A2, A21, A22, A23, A3, A31, A32, A33, B, B1, B11, B12, B2, B21, B22, B23, B3, B31, B32, B33, C, C1, C11, C12, C13, C2, C21, C22, C23, C3, C31, C32, C33 = self.get_grand_parents_brothers()
        B11.to_prev('../../../A/A1/A13')
        self.assertEqual(4, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        self.assertEqual('B11', A1.Children[2].Name)
        self.assertEqual('A13', A1.Children[3].Name)
        self.assertEqual(2, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        self.assertEqual('B13', B1.Children[1].Name)

    def test_to_children_first_none(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_children_first()
        with self.assertRaises(ValueError):
            B.to_children_first()
        with self.assertRaises(ValueError):
            A.to_children_first()
        with self.assertRaises(ValueError):
            root.to_children_first()
    def test_to_children_first_relative_this(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_children_first('./')
        with self.assertRaises(ValueError):
            B.to_children_first('./')
        with self.assertRaises(ValueError):
            A.to_children_first('./')
        with self.assertRaises(ValueError):
            root.to_children_first('./')
        with self.assertRaises(ValueError):
            root.to_children_first('../')
    def test_to_children_first_relative_parent(self):
        root, A, B, C = self.get_brosers()
        C.to_children_first('../')
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        B.to_children_first('../')
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_children_first('../')
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_children_first('../')
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
    def test_to_children_first_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        B1.to_children_first('../../A')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(2, len(root.Children[0].Children))
        self.assertEqual(0, len(root.Children[1].Children))
        self.assertEqual('B1', root.Children[0].Children[0].Name)
        self.assertEqual('A1', root.Children[0].Children[1].Name)
    def test_to_children_first_relative_grand_parent(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B11.to_children_first('../../../A/A1')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(1, len(root.Children[0].Children))
        self.assertEqual(1, len(root.Children[1].Children))
        self.assertEqual('A1', root.Children[0].Children[0].Name)              # A/A1
        self.assertEqual('B1', root.Children[1].Children[0].Name)              # B/B1
        self.assertEqual(2, len(root.Children[0].Children[0].Children))
        self.assertEqual(1, len(root.Children[1].Children[0].Children))
        self.assertEqual('B11', root.Children[0].Children[0].Children[0].Name) # A/A1/B11
        self.assertEqual('A11', root.Children[0].Children[0].Children[1].Name) # A/A1/A11
        self.assertEqual('B12', root.Children[1].Children[0].Children[0].Name) # B/B1/B12
    def test_to_children_first_over_ancestor(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_children_first('../../')

    def test_to_children_last_none(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            A.to_children_last()
        with self.assertRaises(ValueError):
            B.to_children_last()
        with self.assertRaises(ValueError):
            C.to_children_last()
        with self.assertRaises(ValueError):
            root.to_children_last()
    def test_to_children_last_relative_this(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            A.to_children_last('./')
        with self.assertRaises(ValueError):
            B.to_children_last('./')
        with self.assertRaises(ValueError):
            C.to_children_last('./')
        with self.assertRaises(ValueError):
            root.to_children_last()
    def test_to_children_last_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        B1.to_children_last('../')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(1, len(root.Children[0].Children))
        self.assertEqual(1, len(root.Children[1].Children))
        self.assertEqual('A1', root.Children[0].Children[0].Name)
        self.assertEqual('B1', root.Children[1].Children[0].Name)
    def test_to_children_last_relative_parent_1(self):
        root, A, A1, B, B1 = self.get_parents()
        B1.to_children_last('../../')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('B1',root.Children[2].Name)
        self.assertEqual(1, len(root.Children[0].Children))
        self.assertEqual(0, len(root.Children[1].Children))
        self.assertEqual('A1', root.Children[0].Children[0].Name)
    def test_to_children_last_relative_parent_2(self):
        root, A, A1, B, B1 = self.get_parents()
        B1.to_children_last('../../A')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(2, len(root.Children[0].Children))
        self.assertEqual(0, len(root.Children[1].Children))
        self.assertEqual('A1', root.Children[0].Children[0].Name)
        self.assertEqual('B1', root.Children[0].Children[1].Name)
    def test_to_children_last_relative_grand_parent(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B11.to_children_last('../../../A/A1')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(1, len(root.Children[0].Children))
        self.assertEqual(1, len(root.Children[1].Children))
        self.assertEqual('A1', root.Children[0].Children[0].Name)              # A/A1
        self.assertEqual('B1', root.Children[1].Children[0].Name)              # B/B1
        self.assertEqual(2, len(root.Children[0].Children[0].Children))
        self.assertEqual(1, len(root.Children[1].Children[0].Children))
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name) # A/A1/A11
        self.assertEqual('B11', root.Children[0].Children[0].Children[1].Name) # A/A1/B11
        self.assertEqual('B12', root.Children[1].Children[0].Children[0].Name) # B/B1/B12
    def test_to_children_last_over_ancestor(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_children_last('../../')

    def test_to_ancestor_first_none(self):
        root, A, B, C = self.get_brosers()
        C.to_ancestor_first()
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        B.to_ancestor_first()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_ancestor_first()
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_ancestor_first()
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        with self.assertRaises(ValueError):
            root.to_ancestor_first()

    def test_to_ancestor_first_0(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_ancestor_first(0)
        with self.assertRaises(ValueError):
            B.to_ancestor_first(0)
        with self.assertRaises(ValueError):
            A.to_ancestor_first(0)
        with self.assertRaises(ValueError):
            root.to_ancestor_first(0)
        with self.assertRaises(ValueError):
            root.to_ancestor_first(0)

    def test_to_ancestor_first_1(self):
        root, A, B, C = self.get_brosers()
        C.to_ancestor_first(1)
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        B.to_ancestor_first(1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_ancestor_first(1)
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_ancestor_first(1)
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        with self.assertRaises(ValueError):
            root.to_ancestor_first(1)

    def test_to_ancestor_first_1_minus(self):
        root, A, B, C = self.get_brosers()
        C.to_ancestor_first(-1)
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        B.to_ancestor_first(-1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_ancestor_first(-1)
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_ancestor_first(-1)
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        with self.assertRaises(ValueError):
            root.to_ancestor_first(-1)

    def test_to_ancestor_first_2(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_ancestor_first(2)
        with self.assertRaises(ValueError):
            C.to_ancestor_first(-2)

    def test_to_ancestor_last_none(self):
        root, A, B, C = self.get_brosers()
        A.to_ancestor_last()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_ancestor_last()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        C.to_ancestor_last()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)

    def test_to_ancestor_last_0(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_ancestor_last(0)
        with self.assertRaises(ValueError):
            B.to_ancestor_last(0)
        with self.assertRaises(ValueError):
            A.to_ancestor_last(0)
        with self.assertRaises(ValueError):
            root.to_ancestor_last(0)

    def test_to_ancestor_last_1(self):
        root, A, B, C = self.get_brosers()
        A.to_ancestor_last(1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_ancestor_last(1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        C.to_ancestor_last(1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)

    def test_to_ancestor_last_1_minus(self):
        root, A, B, C = self.get_brosers()
        A.to_ancestor_last(-1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_ancestor_last(-1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        C.to_ancestor_last(-1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)

    def test_to_ancestor_last_2(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_ancestor_last(2)
        with self.assertRaises(ValueError):
            C.to_ancestor_last(-2)

    def test_to_ancestor_next_none(self):
        root, A, B, C = self.get_brosers()
        A.to_ancestor_next()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        A.to_ancestor_next()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        A.to_ancestor_next()
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)

    def test_to_ancestor_next_0(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_ancestor_next(0)
        with self.assertRaises(ValueError):
            B.to_ancestor_next(0)
        with self.assertRaises(ValueError):
            A.to_ancestor_next(0)
        with self.assertRaises(ValueError):
            root.to_ancestor_next(0)

    def test_to_ancestor_next_1(self):
        root, A, B, C = self.get_brosers()
        A.to_ancestor_next(1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        A.to_ancestor_next(1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        A.to_ancestor_next(1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)

    def test_to_ancestor_next_1_minus(self):
        root, A, B, C = self.get_brosers()
        A.to_ancestor_next(-1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        C.to_ancestor_next(-1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)
        C.to_ancestor_next(-1)
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('A', root.Children[2].Name)

    def test_to_ancestor_next_2(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_ancestor_next(2)
        with self.assertRaises(ValueError):
            C.to_ancestor_next(-2)

    def test_to_ancestor_prev_none(self):
        root, A, B, C = self.get_brosers()
        C.to_ancestor_prev()
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        C.to_ancestor_prev()
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        C.to_ancestor_prev()
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)

    def test_to_ancestor_prev_0(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_ancestor_prev(0)
        with self.assertRaises(ValueError):
            B.to_ancestor_prev(0)
        with self.assertRaises(ValueError):
            A.to_ancestor_prev(0)
        with self.assertRaises(ValueError):
            root.to_ancestor_prev(0)

    def test_to_ancestor_prev_1(self):
        root, A, B, C = self.get_brosers()
        C.to_ancestor_prev(1)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        C.to_ancestor_prev(1)
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        C.to_ancestor_prev(1)
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)

    def test_to_ancestor_prev_1_minus(self):
        root, A, B, C = self.get_brosers()
        C.to_ancestor_prev(-1)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        C.to_ancestor_prev(-1)
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        C.to_ancestor_prev(-1)
        self.assertEqual('C', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)

    def test_to_ancestor_prev_2(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            C.to_ancestor_prev(2)
        with self.assertRaises(ValueError):
            C.to_ancestor_prev(-2)

    def test_insert_first_none(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        A.insert_first(D)
        self.assertEqual(4, len(root.Children))
        self.assertEqual('D', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('C', root.Children[3].Name)
    def test_insert_first_relative_this(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        A.insert_first(D, './')
        self.assertEqual(4, len(root.Children))
        self.assertEqual('D', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('C', root.Children[3].Name)
    def test_insert_first_relative_parent(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            A.insert_first(D, '../')
    def test_insert_first_relative_this_root(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            root.insert_first(D)
        with self.assertRaises(ValueError):
            root.insert_first(D, './')
    def test_insert_first_none_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        A.insert_first(C)
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        A0 = Node('A0', parent=A)
        A1.insert_first(A0)
        self.assertEqual('A0', A.Children[0].Name)
        B0 = Node('B0', parent=B)
        B1.insert_first(B0)
        self.assertEqual('B0', B.Children[0].Name)
    def test_insert_first_relative_this(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        A.insert_first(C, './')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        A0 = Node('A0', parent=A)
        A1.insert_first(A0, './')
        self.assertEqual('A0', A.Children[0].Name)
        B0 = Node('B0', parent=B)
        B1.insert_first(B0, './')
        self.assertEqual('B0', B.Children[0].Name)
    def test_insert_first_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        with self.assertRaises(ValueError):
            A.insert_first(C, '../')
        A0 = Node('A0', parent=A)
        with self.assertRaises(ValueError):
            A1.insert_first(A0, '../../')
        B0 = Node('B0', parent=B)
        with self.assertRaises(ValueError):
            B1.insert_first(B0, '../../')
        A1.insert_first(A0, '../')
        self.assertEqual('A0', root.Children[0].Name)
        B1.insert_first(B0, '../')
        self.assertEqual('B0', root.Children[0].Name)
    def test_insert_first_grand_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        A12 = Node('A12', parent=A1)
        A11.insert_first(A12)
        self.assertEqual(2, len(A1.Children))
        self.assertEqual('A12', A1.Children[0].Name)
        self.assertEqual('A11', A1.Children[1].Name)
        A13 = Node('A13', parent=A1)
        root.insert_first(A13, 'A/A1/A12')
        self.assertEqual(3, len(A1.Children))
        self.assertEqual('A13', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        self.assertEqual('A11', A1.Children[2].Name)

    def test_insert_last_none(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        A.insert_last(D)
        self.assertEqual(4, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        self.assertEqual('D', root.Children[3].Name)
    def test_insert_last_relative_this(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        A.insert_last(D, './')
        self.assertEqual(4, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        self.assertEqual('D', root.Children[3].Name)
    def test_insert_last_relative_parent(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            A.insert_last(D, '../')
    def test_insert_last_relative_this_root(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            root.insert_last(D, './')
    def test_insert_last_none_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        A.insert_last(C)
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[2].Name)
        A0 = Node('A0', parent=A)
        A1.insert_last(A0)
        self.assertEqual('A0', A.Children[1].Name)
        B0 = Node('B0', parent=B)
        B1.insert_last(B0)
        self.assertEqual('B0', B.Children[1].Name)
    def test_insert_last_relative_this(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        A.insert_last(C, './')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[2].Name)
        A0 = Node('A0', parent=A)
        A1.insert_last(A0, './')
        self.assertEqual('A0', A.Children[1].Name)
        B0 = Node('B0', parent=B)
        B1.insert_last(B0, './')
        self.assertEqual('B0', B.Children[1].Name)
    def test_insert_last_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        with self.assertRaises(ValueError):
            A.insert_last(C, '../')
        A0 = Node('A0', parent=A)
        with self.assertRaises(ValueError):
            A1.insert_last(A0, '../../')
        B0 = Node('B0', parent=B)
        with self.assertRaises(ValueError):
            B1.insert_last(B0, '../../')
        A1.insert_last(A0, '../')
        self.assertEqual('A0', root.Children[2].Name)
        B1.insert_last(B0, '../')
        self.assertEqual('B0', root.Children[3].Name)
    def test_insert_last_grand_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        A12 = Node('A12', parent=A1)
        A11.insert_last(A12)
        self.assertEqual(2, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        A13 = Node('A13', parent=A1)
        root.insert_last(A13, 'A/A1/A12')
        self.assertEqual(3, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        self.assertEqual('A13', A1.Children[2].Name)

    def test_insert_prev_none(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        A.insert_prev(D)
        self.assertEqual(4, len(root.Children))
        self.assertEqual('D', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('C', root.Children[3].Name)
        E = Node('E', parent=root)
        C.insert_prev(E)
        self.assertEqual(5, len(root.Children))
        self.assertEqual('D', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('E', root.Children[3].Name)
        self.assertEqual('C', root.Children[4].Name)
    def test_insert_prev_relative_this(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        A.insert_prev(D, './')
        self.assertEqual(4, len(root.Children))
        self.assertEqual('D', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('C', root.Children[3].Name)
        E = Node('E', parent=root)
        C.insert_prev(E, './')
        self.assertEqual(5, len(root.Children))
        self.assertEqual('D', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('E', root.Children[3].Name)
        self.assertEqual('C', root.Children[4].Name)

    def test_insert_prev_relative_parent(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            A.insert_prev(D, '../')
    def test_insert_prev_relative_this_root(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            root.insert_prev(D, './')
    def test_insert_prev_none_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        A.insert_prev(C)
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        A0 = Node('A0', parent=A)
        A1.insert_prev(A0)
        self.assertEqual('A0', A.Children[0].Name)
        B0 = Node('B0', parent=B)
        B1.insert_prev(B0)
        self.assertEqual('B0', B.Children[0].Name)
    def test_insert_prev_relative_this(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        A.insert_prev(C, './')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        A0 = Node('A0', parent=A)
        A1.insert_prev(A0, './')
        self.assertEqual('A0', A.Children[0].Name)
        B0 = Node('B0', parent=B)
        B1.insert_prev(B0, './')
        self.assertEqual('B0', B.Children[0].Name)
    def test_insert_prev_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        with self.assertRaises(ValueError):
            A.insert_prev(C, '../')
        A0 = Node('A0', parent=A)
        with self.assertRaises(ValueError):
            A1.insert_prev(A0, '../../')
        B0 = Node('B0', parent=B)
        with self.assertRaises(ValueError):
            B1.insert_prev(B0, '../../')
        A1.insert_prev(A0, '../')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('A0', root.Children[0].Name)
        B1.insert_prev(B0, '../')
        self.assertEqual('B0', root.Children[2].Name)

        self.assertEqual('A0',root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B0',root.Children[2].Name)
        self.assertEqual('B', root.Children[3].Name)
    def test_insert_prev_grand_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        A12 = Node('A12', parent=A1)
        A11.insert_prev(A12)
        self.assertEqual(2, len(A1.Children))
        self.assertEqual('A12', A1.Children[0].Name)
        self.assertEqual('A11', A1.Children[1].Name)
        A13 = Node('A13', parent=A1)
        root.insert_prev(A13, 'A/A1/A12')
        self.assertEqual(3, len(A1.Children))
        self.assertEqual('A13', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        self.assertEqual('A11', A1.Children[2].Name)

    def test_insert_next_none(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        A.insert_next(D)
        self.assertEqual(4, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('D', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('C', root.Children[3].Name)
        E = Node('E', parent=root)
        C.insert_next(E)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('D', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('C', root.Children[3].Name)
        self.assertEqual('E', root.Children[4].Name)
    def test_insert_next_relative_this(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        A.insert_next(D, './')
        self.assertEqual(4, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('D', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('C', root.Children[3].Name)
        E = Node('E', parent=root)
        C.insert_next(E, './')
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('D', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('C', root.Children[3].Name)
        self.assertEqual('E', root.Children[4].Name)

    def test_insert_next_relative_parent(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            A.insert_next(D, '../')
    def test_insert_next_relative_this_root(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            root.insert_next(D, './')
    def test_insert_next_none_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        A.insert_next(C)
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[1].Name)
        A0 = Node('A0', parent=A)
        A1.insert_next(A0)
        self.assertEqual('A0', A.Children[1].Name)
        B0 = Node('B0', parent=B)
        B1.insert_next(B0)
        self.assertEqual('B0', B.Children[1].Name)
    def test_insert_next_relative_this(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        A.insert_next(C, './')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[1].Name)
        A0 = Node('A0', parent=A)
        A1.insert_next(A0, './')
        self.assertEqual('A0', A.Children[1].Name)
        B0 = Node('B0', parent=B)
        B1.insert_next(B0, './')
        self.assertEqual('B0', B.Children[1].Name)
    def test_insert_next_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        with self.assertRaises(ValueError):
            A.insert_next(C, '../')
        A0 = Node('A0', parent=A)
        with self.assertRaises(ValueError):
            A1.insert_next(A0, '../../')
        B0 = Node('B0', parent=B)
        with self.assertRaises(ValueError):
            B1.insert_next(B0, '../../')
        A1.insert_next(A0, '../')
        self.assertEqual('A0', root.Children[1].Name)
        B1.insert_next(B0, '../')
        self.assertEqual('B0', root.Children[3].Name)
    def test_insert_next_grand_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        A12 = Node('A12', parent=A1)
        A11.insert_next(A12)
        self.assertEqual(2, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        A13 = Node('A13', parent=A1)
        root.insert_next(A13, 'A/A1/A12')
        self.assertEqual(3, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        self.assertEqual('A13', A1.Children[2].Name)

    def test_insert_children_first_none(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        root.insert_children_first(D)
        self.assertEqual(4, len(root.Children))
        self.assertEqual('D', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('C', root.Children[3].Name)
        A1 = Node('A1', parent=root)
        A.insert_children_first(A1)
        self.assertEqual(4, len(root.Children))
        self.assertEqual(1, len(A.Children))
        self.assertEqual('A1', A.Children[0].Name)
        A2 = Node('A2', parent=root)
        A.insert_children_first(A2)
        self.assertEqual(2, len(A.Children))
        self.assertEqual('A2', A.Children[0].Name)
        self.assertEqual('A1', A.Children[1].Name)
    def test_insert_children_first_relative_this(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        root.insert_children_first(D, './')
        self.assertEqual(4, len(root.Children))
        self.assertEqual('D', root.Children[0].Name)
        self.assertEqual('A', root.Children[1].Name)
        self.assertEqual('B', root.Children[2].Name)
        self.assertEqual('C', root.Children[3].Name)
        A1 = Node('A1', parent=root)
        A.insert_children_first(A1, './')
        self.assertEqual(4, len(root.Children))
        self.assertEqual(1, len(A.Children))
        self.assertEqual('A1', A.Children[0].Name)
        A2 = Node('A2', parent=root)
        A.insert_children_first(A2, './')
        self.assertEqual(2, len(A.Children))
        self.assertEqual('A2', A.Children[0].Name)
        self.assertEqual('A1', A.Children[1].Name)
    def test_insert_children_first_relative_parent(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            root.insert_children_first(D, '../')
    def test_insert_children_first_relative_grand_parent(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            root.insert_children_first(D, '../../')
    def test_insert_children_first_none_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        root.insert_children_first(C)
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        A0 = Node('A0', parent=A)
        A.insert_children_first(A0)
        self.assertEqual('A0', A.Children[0].Name)
        B0 = Node('B0', parent=B)
        B.insert_children_first(B0)
        self.assertEqual('B0', B.Children[0].Name)
    def test_insert_children_first_relative_this(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        root.insert_children_first(C, './')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        A0 = Node('A0', parent=A)
        A.insert_children_first(A0, './')
        self.assertEqual('A0', A.Children[0].Name)
        B0 = Node('B0', parent=B)
        B.insert_children_first(B0, './')
        self.assertEqual('B0', B.Children[0].Name)
    def test_insert_children_first_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        with self.assertRaises(ValueError):
            root.insert_children_first(C, '../')
        A0 = Node('A0', parent=A)
        with self.assertRaises(ValueError):
            A.insert_children_first(A0, '../../')
        B0 = Node('B0', parent=B)
        with self.assertRaises(ValueError):
            B.insert_children_first(B0, '../../')
        A.insert_children_first(A0, '../')
        self.assertEqual('A0', root.Children[0].Name)
        B.insert_children_first(B0, '../')
        self.assertEqual('B0', root.Children[0].Name)
    def test_insert_children_first_grand_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        A12 = Node('A12', parent=A1)
        A1.insert_children_first(A12)
        self.assertEqual(2, len(A1.Children))
        self.assertEqual('A12', A1.Children[0].Name)
        self.assertEqual('A11', A1.Children[1].Name)
        A13 = Node('A13', parent=A1)
        root.insert_children_first(A13, 'A/A1')
        self.assertEqual(3, len(A1.Children))
        self.assertEqual('A13', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        self.assertEqual('A11', A1.Children[2].Name)
        A14 = Node('A14', parent=A1)
        A.insert_children_first(A14, 'A1')
        self.assertEqual(4, len(A1.Children))
        self.assertEqual('A14', A1.Children[0].Name)
        self.assertEqual('A13', A1.Children[1].Name)
        self.assertEqual('A12', A1.Children[2].Name)
        self.assertEqual('A11', A1.Children[3].Name)

    def test_insert_children_last_none(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        root.insert_children_last(D)
        self.assertEqual(4, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        self.assertEqual('D', root.Children[3].Name)
    def test_insert_children_last_relative_this(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        root.insert_children_last(D, './')
        self.assertEqual(4, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('C', root.Children[2].Name)
        self.assertEqual('D', root.Children[3].Name)
    def test_insert_children_last_relative_parent(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            root.insert_children_last(D, '../')
    def test_insert_children_last_relative_grand_parent(self):
        root, A, B, C = self.get_brosers()
        D = Node('D', parent=root)
        with self.assertRaises(ValueError):
            root.insert_children_last(D, '../../')
    def test_insert_children_last_none_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        root.insert_children_last(C)
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[2].Name)
        A0 = Node('A0', parent=A)
        A.insert_children_last(A0)
        self.assertEqual('A0', A.Children[1].Name)
        B0 = Node('B0', parent=B)
        B.insert_children_last(B0)
        self.assertEqual('B0', B.Children[1].Name)
    def test_insert_children_last_relative_this(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        root.insert_children_last(C, './')
        self.assertEqual(3, len(root.Children))
        self.assertEqual('C', root.Children[2].Name)
        A0 = Node('A0', parent=A)
        A.insert_children_last(A0, './')
        self.assertEqual('A0', A.Children[1].Name)
        B0 = Node('B0', parent=B)
        B.insert_children_last(B0, './')
        self.assertEqual('B0', B.Children[1].Name)
    def test_insert_children_last_relative_parent(self):
        root, A, A1, B, B1 = self.get_parents()
        C = Node('C', parent=root)
        with self.assertRaises(ValueError):
            root.insert_children_last(C, '../')
        A0 = Node('A0', parent=A)
        with self.assertRaises(ValueError):
            A.insert_children_last(A0, '../../')
        B0 = Node('B0', parent=B)
        with self.assertRaises(ValueError):
            B.insert_children_last(B0, '../../')
        A.insert_children_last(A0, '../')
        self.assertEqual('A0', root.Children[2].Name)
        B.insert_children_last(B0, '../')
        self.assertEqual('B0', root.Children[3].Name)
    def test_insert_children_last_grand_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        A12 = Node('A12', parent=A1)
        A1.insert_children_last(A12)
        self.assertEqual(2, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        A13 = Node('A13', parent=A1)
        root.insert_children_last(A13, 'A/A1')
        self.assertEqual(3, len(A1.Children))
        self.assertEqual('A11', A1.Children[0].Name)
        self.assertEqual('A12', A1.Children[1].Name)
        self.assertEqual('A13', A1.Children[2].Name)

    def test_select_path_TypeError(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(TypeError):
            root.select()
    def test_select_relative_this(self):
        root, A, B, C = self.get_brosers()
        self.assertEqual(A, root.select('A'))
        self.assertEqual(B, root.select('B'))
        self.assertEqual(C, root.select('C'))
        self.assertEqual(root, A.select('../'))
        self.assertEqual(root, B.select('../'))
        self.assertEqual(root, C.select('../'))
        self.assertEqual(A, A.select('../A'))
        self.assertEqual(B, A.select('../B'))
        self.assertEqual(C, A.select('../C'))
        self.assertEqual(A, B.select('../A'))
        self.assertEqual(B, B.select('../B'))
        self.assertEqual(C, B.select('../C'))
        self.assertEqual(A, C.select('../A'))
        self.assertEqual(B, C.select('../B'))
        self.assertEqual(C, C.select('../C'))
    def test_select_brothers_root_over(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            root.select('../')
        with self.assertRaises(ValueError):
            A.select('../../')
        with self.assertRaises(ValueError):
            B.select('../../')
        with self.assertRaises(ValueError):
            C.select('../../')
    def test_select_relative_this(self):
        root, A, B, C = self.get_brosers()
        self.assertEqual(root, root.select('./'))
        self.assertEqual(A, A.select('./'))
        self.assertEqual(B, B.select('./'))
        self.assertEqual(C, C.select('./'))
    def test_select_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        self.assertEqual(A, root.select('A'))
        self.assertEqual(B, root.select('B'))
        self.assertEqual(A1, root.select('A/A1'))
        self.assertEqual(B1, root.select('B/B1'))
        self.assertEqual(A1, A.select('A1'))
        self.assertEqual(B1, B.select('B1'))
        self.assertEqual(A1, A1.select('./'))
        self.assertEqual(B1, B1.select('./'))
        self.assertEqual(A, A1.select('../'))
        self.assertEqual(B, B1.select('../'))
        self.assertEqual(root, A1.select('../../'))
        self.assertEqual(root, B1.select('../../'))
        self.assertEqual(B, A1.select('../../B'))
        self.assertEqual(B1, A1.select('../../B/B1'))
        self.assertEqual(A, B1.select('../../A'))
        self.assertEqual(A1, B1.select('../../A/A1'))
        self.assertEqual(root, A.select('../'))
        self.assertEqual(root, B.select('../'))
        self.assertEqual(A, A.select('../A'))
        self.assertEqual(B, A.select('../B'))
        self.assertEqual(A, B.select('../A'))
        self.assertEqual(B, B.select('../B'))
        self.assertEqual(A1, A.select('../A/A1'))
        self.assertEqual(B1, A.select('../B/B1'))
        self.assertEqual(A1, B.select('../A/A1'))
        self.assertEqual(B1, B.select('../B/B1'))
    def test_select_grand_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        self.assertEqual(A, root.select('A'))
        self.assertEqual(B, root.select('B'))
        self.assertEqual(A1, root.select('A/A1'))
        self.assertEqual(B1, root.select('B/B1'))
        self.assertEqual(A11, root.select('A/A1/A11'))
        self.assertEqual(B11, root.select('B/B1/B11'))
        self.assertEqual(B12, root.select('B/B1/B12'))
        self.assertEqual(A1, A.select('A1'))
        self.assertEqual(B1, B.select('B1'))
        self.assertEqual(A11, A.select('A1/A11'))
        self.assertEqual(B11, B.select('B1/B11'))
        self.assertEqual(B12, B.select('B1/B12'))
        self.assertEqual(A11, A1.select('A11'))
        self.assertEqual(B11, B1.select('B11'))
        self.assertEqual(B12, B1.select('B12'))
        self.assertEqual(A11, A11.select('./'))
        self.assertEqual(B11, B11.select('./'))
        self.assertEqual(B12, B12.select('./'))
        self.assertEqual(A1, A11.select('../'))
        self.assertEqual(B1, B11.select('../'))
        self.assertEqual(B1, B12.select('../'))
        self.assertEqual(A, A11.select('../../'))
        self.assertEqual(B, B11.select('../../'))
        self.assertEqual(B, B12.select('../../'))
        self.assertEqual(root, A11.select('../../../'))
        self.assertEqual(root, B11.select('../../../'))
        self.assertEqual(root, B12.select('../../../'))
        self.assertEqual(A, A11.select('../../../A'))
        self.assertEqual(A, B11.select('../../../A'))
        self.assertEqual(A, B12.select('../../../A'))
        self.assertEqual(A1, A11.select('../../../A/A1'))
        self.assertEqual(A1, B11.select('../../../A/A1'))
        self.assertEqual(A1, B12.select('../../../A/A1'))
        self.assertEqual(A11, A11.select('../../../A/A1/A11'))
        self.assertEqual(A11, B11.select('../../../A/A1/A11'))
        self.assertEqual(A11, B12.select('../../../A/A1/A11'))
        self.assertEqual(B, A11.select('../../../B'))
        self.assertEqual(B, B11.select('../../../B'))
        self.assertEqual(B, B12.select('../../../B'))
        self.assertEqual(B1, A11.select('../../../B/B1'))
        self.assertEqual(B1, B11.select('../../../B/B1'))
        self.assertEqual(B1, B12.select('../../../B/B1'))
        self.assertEqual(B11, A11.select('../../../B/B1/B11'))
        self.assertEqual(B11, B11.select('../../../B/B1/B11'))
        self.assertEqual(B11, B12.select('../../../B/B1/B11'))
        self.assertEqual(B12, A11.select('../../../B/B1/B12'))
        self.assertEqual(B12, B11.select('../../../B/B1/B12'))
        self.assertEqual(B12, B12.select('../../../B/B1/B12'))

    def test_delete_brothers(self):
        root, A, B, C = self.get_brosers()
        A.delete()
        self.assertEqual(2, len(root.Children))
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        B.delete()
        self.assertEqual(1, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        C.delete()
        self.assertEqual(0, len(root.Children))
        
        root, A, B, C = self.get_brosers()
        C.delete()
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        B.delete()
        self.assertEqual(1, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        A.delete()
        self.assertEqual(0, len(root.Children))
 
        root, A, B, C = self.get_brosers()
        B.delete()
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        A.delete()
        self.assertEqual(1, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        C.delete()
        self.assertEqual(0, len(root.Children))
    def test_delete_root(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            root.delete()

    def test_delete_brothers_relative_this(self):
        root, A, B, C = self.get_brosers()
        A.delete('./')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        B.delete('./')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        C.delete('./')
        self.assertEqual(0, len(root.Children))
        
        root, A, B, C = self.get_brosers()
        C.delete('./')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        B.delete('./')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        A.delete('./')
        self.assertEqual(0, len(root.Children))
 
        root, A, B, C = self.get_brosers()
        B.delete('./')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        A.delete('./')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        C.delete('./')
        self.assertEqual(0, len(root.Children))
    def test_delete_root_relative_this(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            root.delete('./')
    def test_delete_brothers_relative_self(self):
        root, A, B, C = self.get_brosers()
        A.delete('../A')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        B.delete('../B')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        C.delete('../C')
        self.assertEqual(0, len(root.Children))
        
        root, A, B, C = self.get_brosers()
        C.delete('../C')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        B.delete('../B')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        A.delete('../A')
        self.assertEqual(0, len(root.Children))
 
        root, A, B, C = self.get_brosers()
        B.delete('../B')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        A.delete('../A')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        C.delete('../C')
        self.assertEqual(0, len(root.Children))
    def test_delete_root_relative_self(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            root.delete('../root')
    def test_delete_brothers_relative_not_self(self):
        root, A, B, C = self.get_brosers()
        A.delete('../B')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        C.delete('../A')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
        
        root, A, B, C = self.get_brosers()
        A.delete('../C')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        B.delete('../A')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('B', root.Children[0].Name)
 
        root, A, B, C = self.get_brosers()
        B.delete('../C')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('B', root.Children[1].Name)
        B.delete('../A')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('B', root.Children[0].Name)

        root, A, B, C = self.get_brosers()
        C.delete('../A')
        self.assertEqual(2, len(root.Children))
        self.assertEqual('B', root.Children[0].Name)
        self.assertEqual('C', root.Children[1].Name)
        C.delete('../B')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('C', root.Children[0].Name)
    def test_delete_root_relative_self(self):
        root, A, B, C = self.get_brosers()
        with self.assertRaises(ValueError):
            A.delete('../root')
    def test_delete_parents(self):
        root, A, A1, B, B1 = self.get_parents()
        root.delete('A/A1')
        self.assertEqual(0, len(A.Children))
        root.delete('B/B1')
        self.assertEqual(0, len(B.Children))

        root, A, A1, B, B1 = self.get_parents()
        root.delete('A')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('B', root.Children[0].Name)
#        self.assertEqual(None, A)
#        self.assertEqual(None, A1)

        root, A, A1, B, B1 = self.get_parents()
        root.delete('B')
        self.assertEqual(1, len(root.Children))
        self.assertEqual('A', root.Children[0].Name)
    def test_delete_parents(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        root.delete('A/A1/A11')
        self.assertEqual(0, len(A1.Children))
        root.delete('B/B1/B11')
        self.assertEqual(1, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        root.delete('B/B1/B12')
        self.assertEqual(0, len(B1.Children))

        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        A.delete('A1')
        self.assertEqual(0, len(A.Children))
        B.delete('B1')
        self.assertEqual(0, len(B.Children))

        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        A.delete('A1/A11')
        self.assertEqual(0, len(A1.Children))
        B.delete('B1/B11')
        self.assertEqual(1, len(B.Children))
        self.assertEqual('B12', B1.Children[0].Name)

        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B1.delete('B11')
        self.assertEqual(1, len(B.Children))
        self.assertEqual('B12', B1.Children[0].Name)

        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B11.delete()
        self.assertEqual(1, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B11.delete('./')
        self.assertEqual(1, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B11.delete('../')
        self.assertEqual(0, len(B.Children))
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B11.delete('../B11')
        self.assertEqual(1, len(B1.Children))
        self.assertEqual('B12', B1.Children[0].Name)
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        B11.delete('../B12')
        self.assertEqual(1, len(B1.Children))
        self.assertEqual('B11', B1.Children[0].Name)

    def test_update(self):
        root, A, A1, A11, B, B1, B11, B12 = self.get_grand_parents()
        a = Path.select(root, 'A')
        a.Name = 'A_change'
        a = Path.select(root, 'A_change')
        self.assertEqual('A_change', a.Name)

        self.assertEqual(None, a.Attr)
        a.some= 'A_some'
        self.assertEqual('A_some', a.some)

class TestNodeList(unittest.TestCase):
    def test_init_blank(self):
        nl = NodeList()
        self.assertEqual(NodeList, type(nl))
    def test_init_type_error_int(self):
        with self.assertRaises(Node.ChildTypeError):
            nl = NodeList(1)
    def test_init_type_error_str(self):
        with self.assertRaises(Node.ChildTypeError):
            nl = NodeList('A')

    def test_init_type_error_list(self):
        with self.assertRaises(Node.ChildTypeError):
            nl = NodeList(['A'])
    def test_init_type_error_tuple(self):
        with self.assertRaises(Node.ChildTypeError):
            nl = NodeList(('A',))
    def test_init_type_error_set(self):
        s = set(); s.add('A');
        with self.assertRaises(Node.ChildTypeError):
            nl = NodeList(s)
    def test_init_type_error_frozenset(self):
        s = set(); s.add('A'); fs = frozenset(s); 
        with self.assertRaises(Node.ChildTypeError):
            nl = NodeList(fs)
    def test_init_type_error_dict(self):
        with self.assertRaises(Node.ChildTypeError):
            nl = NodeList({'key':'value'})
    def test_init_OrderedDict(self):
        od = OrderedDict(); od['key'] = 'value';
        with self.assertRaises(Node.ChildTypeError):
            nl = NodeList(od)
    def test_init_type_error_int(self):
        with self.assertRaises(Node.ChildTypeError):
            nl = NodeList(1)
    def test_init_type_error_str(self):
        with self.assertRaises(Node.ChildTypeError):
            nl = NodeList('A')
    def test_init_type_error_Node(self):
        with self.assertRaises(Node.ChildTypeError):
            nl = NodeList(Node('A'))

    def test_init_list(self):
        nl = NodeList([Node('A')])
        self.assertEqual(NodeList, type(nl))
        self.assertEqual(1, len(nl))
        self.assertEqual(Node, type(nl[0]))
        self.assertEqual('A', nl[0].Name)
    def test_init_tuple(self):
        nl = NodeList((Node('A'),))
        self.assertEqual(NodeList, type(nl))
        self.assertEqual(1, len(nl))
        self.assertEqual(Node, type(nl[0]))
        self.assertEqual('A', nl[0].Name)
    def test_init_set(self):
        s = set(); s.add(Node('A'));
        nl = NodeList(s)
        self.assertEqual(NodeList, type(nl))
        self.assertEqual(1, len(nl))
        self.assertEqual(Node, type(nl[0]))
        self.assertEqual('A', nl[0].Name)
    def test_init_frozenset(self):
        s = set(); s.add(Node('A')); fs = frozenset(s);
        nl = NodeList(fs)
        self.assertEqual(NodeList, type(nl))
        self.assertEqual(1, len(nl))
        self.assertEqual(Node, type(nl[0]))
        self.assertEqual('A', nl[0].Name)
    def test_init_dict(self):
        nl = NodeList({Node('key'):'value'})
        self.assertEqual(NodeList, type(nl))
        self.assertEqual(1, len(nl))
        self.assertEqual(Node, type(nl[0]))
        self.assertEqual('key', nl[0].Name)
    def test_init_OrderedDict(self):
        od = OrderedDict()
        od[Node('key')] = 'value'
        nl = NodeList(od)
        self.assertEqual(NodeList, type(nl))
        self.assertEqual(1, len(nl))
        self.assertEqual(Node, type(nl[0]))
        self.assertEqual('key', nl[0].Name)

    def test_append(self):
        nl = NodeList()
        node = Node('A')
        nl.append(node)
        self.assertEqual(1, len(nl))
        self.assertEqual(Node, type(nl[0]))
        self.assertEqual('A', nl[0].Name)
    def test_extend(self):
        nl = NodeList()
        nodes = [Node('A'), Node('B')]
        nl.extend(nodes)
        self.assertEqual(2, len(nl))
        self.assertEqual('A', nl[0].Name)
        self.assertEqual('B', nl[1].Name)
    def test_insert(self):
        nl = NodeList()
        node = Node('A')
        nl.insert(0, node)
        self.assertEqual(1, len(nl))
        self.assertEqual(Node, type(nl[0]))
        self.assertEqual('A', nl[0].Name)
    def test_append_type_error(self):
        nl = NodeList()
        with self.assertRaises(TypeError):
            nl.append(1)
        with self.assertRaises(TypeError):
            nl.append('')
        with self.assertRaises(TypeError):
            nl.append([])
    def test_extend_type_error(self):
        nl = NodeList()
        with self.assertRaises(TypeError):
            nl.extend([1])
        with self.assertRaises(TypeError):
            nl.extend([''])
    def test_insert_type_error(self):
        nl = NodeList()
        with self.assertRaises(TypeError):
            nl.insert(1)
        with self.assertRaises(TypeError):
            nl.insert('')
        with self.assertRaises(TypeError):
            nl.insert([])

class TestRootNode(unittest.TestCase):
    def test_init(self):
        root = textree.RootNode(TexTree.ROOT_NAME)
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual(None, root.Attr)

class TestRootSerializer(unittest.TestCase):
    def test_serialize(self):
        root = RootNode()
        ser = textree.RootSerializer()
        self.assertEqual(TexTree.ROOT_NAME, ser.serialize(root))
    def test_serialize_name(self):
        root = RootNode(line='<root>')
        ser = textree.RootSerializer()
        self.assertEqual('<root>', ser.serialize(root))
    def test_serialize_attr(self):
        root = RootNode(attr='root_attr1')
        ser = textree.RootSerializer()
        self.assertEqual(TexTree.ROOT_NAME + TexTree.INDENT + 'root_attr1', ser.serialize(root))

class TestNodeSerializer(unittest.TestCase):
    def test_serialize(self):
        root = RootNode()
        A = Node('A', parent=root)
        ser = textree.NodeSerializer()
        self.assertEqual('A', ser.serialize(A, []))
    def test_serialize_attr(self):
        root = RootNode()
        A = Node('A', parent=root, attr='A_attr1')
        ser = textree.NodeSerializer()
        self.assertEqual('A\tA_attr1', ser.serialize(A, []))
    def test_serialize_2(self):
        root = RootNode()
        A = Node('A', parent=root, attr='A_attr1')
        A1 = Node('A1', parent=root, attr='A1_attr1')
        ser = textree.NodeSerializer()
        self.assertEqual('A\tA_attr1', ser.serialize(A, []))
        self.assertEqual('\tA1\tA1_attr1', ser.serialize(A1, [A]))

class TestRootDeserializer(unittest.TestCase):
    def test_is_root_only_first_line(self):
        tree_text = '<ROOT>\nA\n\tA1\nB'
        des = textree.RootDeserializer()
        ana = LineAnalizer(tree_text.split('\n'))

        self.assertEqual('<ROOT>', ana.RootName)
        self.assertEqual('<ROOT>', TexTree.ROOT_NAME)
        self.assertEqual(None, ana.RootAttr)
        for i, (name, attr) in enumerate(ana.analize_nodes()):
            if 0 == i:
                self.assertEqual('A', name)
                self.assertEqual(None, attr)
            if 1 == i:
                self.assertEqual('A1', name)
                self.assertEqual(None, attr)
            if 2 == i:
                self.assertEqual('B', name)
                self.assertEqual(None, attr)
    def test_is_root_first_line_name_is_not_ROOT_NAME(self):
        tree_text = 'A\n\tA1\nB'
        des = textree.RootDeserializer()
        ana = LineAnalizer(tree_text.split('\n'))

        self.assertEqual(None, ana.RootName)
        self.assertEqual(None, ana.RootAttr)
        for i, (name, attr) in enumerate(ana.analize_nodes()):
            if 0 == i:
                self.assertEqual('A', name)
                self.assertEqual(None, attr)
            if 1 == i:
                self.assertEqual('A1', name)
                self.assertEqual(None, attr)
            if 2 == i:
                self.assertEqual('B', name)
                self.assertEqual(None, attr)
    def test_is_root_only_first_line_has_attr(self):
        tree_text = '<ROOT>\tattr1 attr2 key=val\nA\tattr1\n\tA1\nB'
        des = textree.RootDeserializer()
        ana = LineAnalizer(tree_text.split('\n'))
        self.assertEqual('<ROOT>', ana.RootName)
        self.assertEqual('<ROOT>', TexTree.ROOT_NAME)
        self.assertEqual('attr1 attr2 key=val', ana.RootAttr)
        for i, (name, attr) in enumerate(ana.analize_nodes()):
            if 0 == i:
                self.assertEqual('A', name)
                self.assertEqual('attr1', attr)
            if 1 == i:
                self.assertEqual('A1', name)
                self.assertEqual(None, attr)
            if 2 == i:
                self.assertEqual('B', name)
                self.assertEqual(None, attr)
    def test_deserialize(self):
        tree_text = '<ROOT>\nA\n\tA1\nB'
        des = textree.RootDeserializer()
        ana = LineAnalizer(tree_text.split('\n'))

        self.assertEqual('<ROOT>', ana.RootName)
        self.assertEqual('<ROOT>', TexTree.ROOT_NAME)
        self.assertEqual(None, ana.RootAttr)

        nodes = list(ana.analize_nodes())
        self.assertEqual(3, len(nodes))

        self.assertEqual(('A', None), nodes[0])
        self.assertEqual(('A1', None), nodes[1])
        self.assertEqual(('B', None), nodes[2])
    def test_deserialize_pos(self):
        tree_text = '<ROOT>\tattr1 attr2 attr3'
        des = textree.RootDeserializer()
        ana = LineAnalizer(tree_text.split('\n'))
        self.assertEqual('<ROOT>', ana.RootName)
        self.assertEqual('<ROOT>', TexTree.ROOT_NAME)
        self.assertEqual('attr1 attr2 attr3', ana.RootAttr)
        self.assertEqual(0, len(list(ana.analize_nodes())))
    def test_deserialize_named(self):
        tree_text = '<ROOT>\tkey1=attr1 key2=attr2 key3=attr3'
        des = textree.RootDeserializer()
        ana = LineAnalizer(tree_text.split('\n'))
        self.assertEqual('<ROOT>', ana.RootName)
        self.assertEqual('<ROOT>', TexTree.ROOT_NAME)
        self.assertEqual('key1=attr1 key2=attr2 key3=attr3', ana.RootAttr)
        self.assertEqual(0, len(list(ana.analize_nodes())))
    def test_deserialize_pos_single_quote(self):
        tree_text = "<ROOT>\t'attr 1' 'attr 2' 'attr 3'"
        des = textree.RootDeserializer()
        ana = LineAnalizer(tree_text.split('\n'))
        self.assertEqual('<ROOT>', ana.RootName)
        self.assertEqual('<ROOT>', TexTree.ROOT_NAME)
        self.assertEqual("'attr 1' 'attr 2' 'attr 3'", ana.RootAttr)
        self.assertEqual(0, len(list(ana.analize_nodes())))
    def test_deserialize_pos_double_quote(self):
        tree_text = '<ROOT>\t"attr 1" "attr 2" "attr 3"'
        des = textree.RootDeserializer()
        ana = LineAnalizer(tree_text.split('\n'))
        self.assertEqual('<ROOT>', ana.RootName)
        self.assertEqual('<ROOT>', TexTree.ROOT_NAME)
        self.assertEqual('"attr 1" "attr 2" "attr 3"', ana.RootAttr)
        self.assertEqual(0, len(list(ana.analize_nodes())))
    def test_deserialize_named_single_quote(self):
        tree_text = "<ROOT>\tkey1='attr1' key2='attr2' key3='attr3'"
        des = textree.RootDeserializer()
        ana = LineAnalizer(tree_text.split('\n'))
        self.assertEqual('<ROOT>', ana.RootName)
        self.assertEqual('<ROOT>', TexTree.ROOT_NAME)
        self.assertEqual("key1='attr1' key2='attr2' key3='attr3'", ana.RootAttr)
        self.assertEqual(0, len(list(ana.analize_nodes())))
    def test_deserialize_named_double_quote(self):
        tree_text = '<ROOT>\tkey1="attr1" key2="attr2" key3="attr3"'
        des = textree.RootDeserializer()
        ana = LineAnalizer(tree_text.split('\n'))
        self.assertEqual('<ROOT>', ana.RootName)
        self.assertEqual('<ROOT>', TexTree.ROOT_NAME)
        self.assertEqual('key1="attr1" key2="attr2" key3="attr3"', ana.RootAttr)
        self.assertEqual(0, len(list(ana.analize_nodes())))
    def test_is_root(self):
        tree_text = '<ROOT>\nA\n\tA1\nB'
        des = textree.RootDeserializer()
        ana = LineAnalizer(tree_text.split('\n'))
        self.assertEqual('<ROOT>', ana.RootName)
        self.assertEqual('<ROOT>', TexTree.ROOT_NAME)
        self.assertEqual(None, ana.RootAttr)
        for i, (name, attr) in enumerate(ana.analize_nodes()):
            if 0 == i:
                self.assertEqual('A', name)
                self.assertEqual(None, attr)
            if 1 == i:
                self.assertEqual('A1', name)
                self.assertEqual(None, attr)
            if 2 == i:
                self.assertEqual('B', name)
                self.assertEqual(None, attr)

class TestDeserializer(unittest.TestCase):
    def test_set_attr(self):
        class CustomRootDeserializer(textree.RootDeserializer):
            def deserialize(self, line_analizer, attr=None):
                root = textree.RootNode('<ROOT>')
                root.ROOT_data = '<custom data of ROOT>: ' + root.Name
                return root
        class CustomNodeDeserializer(textree.NodeDeserializer):
            def deserialize(self, line_analizer, parent, parents=None):
                node = Node(line_analizer.Line, parent=parent)
                node.node_data = '<custom data of node>: ' + node.Name
                return node
        tree = TexTree(root_deserializer=CustomRootDeserializer(), node_deserializer=CustomNodeDeserializer())
        root = tree.to_node("A")
        def test_setup_root():
            self.assertEqual(False, hasattr(root,             "node_data"))
            self.assertEqual(True,  hasattr(root,             "ROOT_data"))
            self.assertEqual('<custom data of ROOT>: <ROOT>', root.ROOT_data)
        def test_setup_node():
            self.assertEqual(True,  hasattr(root.Children[0], "node_data"))
            self.assertEqual(False, hasattr(root.Children[0], "ROOT_data"))
            self.assertEqual('<custom data of node>: A', root.Children[0].node_data)
        test_setup_root()
        test_setup_node()
    def test_set_attr_node_only(self):
        class CustomNodeDeserializer(textree.NodeDeserializer):
            def deserialize(self, line_analizer, parent, parents=None):
                node = Node(line_analizer.Line, parent=parent)
                node.node_data = '<custom data of node>: ' + node.Name
                return node
        tree = TexTree(node_deserializer=CustomNodeDeserializer())
        root = tree.to_node("A")
        def test_setup_node():
            self.assertEqual(True,  hasattr(root.Children[0], "node_data"))
            self.assertEqual(False, hasattr(root.Children[0], "ROOT_data"))
            self.assertEqual('<custom data of node>: A', root.Children[0].node_data)
        test_setup_node()
    def test_set_attr_root_only(self):
        class CustomRootDeserializer(textree.RootDeserializer):
            def deserialize(self, line_analizer, attr=None):
                root = textree.RootNode('<ROOT>')
                root.ROOT_data = '<custom data of ROOT>: ' + root.Name
                return root
        tree = TexTree(root_deserializer=CustomRootDeserializer())
        root = tree.to_node("A")
        def test_setup_root():
            self.assertEqual(False, hasattr(root,             "node_data"))
            self.assertEqual(True,  hasattr(root,             "ROOT_data"))
            self.assertEqual('<custom data of ROOT>: <ROOT>', root.ROOT_data)
        test_setup_root()

class TestLineAnalizer(unittest.TestCase):
    def test_lines_type_error(self):
        with self.assertRaises(ValueError):
            ana = LineAnalizer(None)
    def test_line_type_error_one_line(self):
        with self.assertRaises(TypeError):
            ana = LineAnalizer([1])
    def test_line_type_error_two_line(self):
        with self.assertRaises(TypeError):
            ana = LineAnalizer([1, 2])
    def test_one_line_last_line(self):
        lines = ["last_line"]
        ana = LineAnalizer(lines)
        self.assertEqual(None, ana.RootName)
        self.assertEqual(None, ana.RootAttr)
        for i, (name, attr) in enumerate(ana.analize_nodes()):
            if 0 == i:
                self.assertEqual('last_line', name)
                self.assertEqual(None, attr)
                self.assertEqual(True, ana.IsLast)
                self.assertEqual(True,  ana.IsFirst)
                self.assertEqual(False,  ana.IsParent)
                self.assertEqual(True, ana.IsLeaf)
                self.assertEqual("last_line", ana.Line)
                self.assertEqual(0, ana.Indent)
                self.assertEqual(0, ana.Index)
                self.assertEqual("last_line",  ana.Name)
                self.assertEqual(None,  ana.Attr)
                self.assertEqual(0, ana.IndentationDiff)
    def test_two_line_brosers(self):
        lines = ["A", "B"]
        ana = LineAnalizer(lines)

        self.assertEqual(None, ana.RootName)
        self.assertEqual(None, ana.RootAttr)
        for i, (name, attr) in enumerate(ana.analize_nodes()):
            if 0 == i:
                self.assertEqual('A', name)
                self.assertEqual(None, attr)
                self.assertEqual(False, ana.IsLast)
                self.assertEqual(True,  ana.IsFirst)
                self.assertEqual(False,  ana.IsParent)
                self.assertEqual(True, ana.IsLeaf)
                self.assertEqual("A", ana.Line)
                self.assertEqual(0, ana.Indent)
                self.assertEqual(0, ana.Index)
                self.assertEqual("A",  ana.Name)
                self.assertEqual(None,  ana.Attr)
                self.assertEqual(0, ana.IndentationDiff)
            elif 1 == i:
                self.assertEqual('B', name)
                self.assertEqual(None, attr)
                self.assertEqual(True,  ana.IsLast)
                self.assertEqual(False, ana.IsFirst)
                self.assertEqual(False, ana.IsParent)
                self.assertEqual(True,  ana.IsLeaf)
                self.assertEqual("B", ana.Line)
                self.assertEqual(0, ana.Indent)
                self.assertEqual(1, ana.Index)
                self.assertEqual("B",  ana.Name)
                self.assertEqual(None,  ana.Attr)
                self.assertEqual(0, ana.IndentationDiff)
    def test_two_line_parent(self):
        lines = ["A", "\tA1"]
        ana = LineAnalizer(lines)

        self.assertEqual(None, ana.RootName)
        self.assertEqual(None, ana.RootAttr)
        for i, (name, attr) in enumerate(ana.analize_nodes()):
            if 0 == i:
                self.assertEqual('A', name)
                self.assertEqual(None, attr)
                self.assertEqual(False, ana.IsLast)
                self.assertEqual(True,  ana.IsFirst)
                self.assertEqual(True,  ana.IsParent)
                self.assertEqual(False, ana.IsLeaf)
                self.assertEqual("A", ana.Line)
                self.assertEqual(0, ana.Indent)
                self.assertEqual(0, ana.Index)
                self.assertEqual("A",  ana.Name)
                self.assertEqual(None,  ana.Attr)
                self.assertEqual(1, ana.IndentationDiff)
            elif 1 == i:
                self.assertEqual('A1', name)
                self.assertEqual(None, attr)
                self.assertEqual(True,  ana.IsLast)
                self.assertEqual(False, ana.IsFirst)
                self.assertEqual(False, ana.IsParent)
                self.assertEqual(True,  ana.IsLeaf)
                self.assertEqual("\tA1", ana.Line)
                self.assertEqual(1, ana.Indent)
                self.assertEqual(1, ana.Index)
                self.assertEqual("A1",  ana.Name)
                self.assertEqual(None,  ana.Attr)
                self.assertEqual(1, ana.IndentationDiff)
    def test_relative_indent_error(self):
        lines = ["A", "\t\tA11"]
        ana = LineAnalizer(lines)
        with self.assertRaises(LineAnalizer.RelativeIndentError):
            for _, _ in ana.analize_nodes(): pass

class TestTexTree(unittest.TestCase):
    def test_init(self):
        tree = TexTree()
        self.assertEqual(tree.Root, None)
    def test_INDENT_read_only(self):
        with self.assertRaises(AttributeError):
            TexTree.INDENT = '    '
    def test_ROOT_NAME_read_only(self):
        with self.assertRaises(AttributeError):
            TexTree.ROOT_NAME= 'root_name'
    def test_to_node_type_error(self):
        tree = TexTree()
        with self.assertRaises(TypeError):
            tree.to_node()
        with self.assertRaises(TexTree.TreeTextTypeError):
            tree.to_node(None)
        with self.assertRaises(TexTree.TreeTextTypeError):
            tree.to_node(1)
        with self.assertRaises(TexTree.TreeTextTypeError):
            tree.to_node([])
    def test_to_node_empty_error(self):
        tree = TexTree()
        with self.assertRaises(TexTree.TreeTextEmptyError):
            tree.to_node("")
        with self.assertRaises(TexTree.TreeTextEmptyError):
            tree.to_node("\n")
        with self.assertRaises(TexTree.TreeTextEmptyError):
            tree.to_node("\t")
        with self.assertRaises(TexTree.TreeTextEmptyError):
            tree.to_node(" ")
        with self.assertRaises(TexTree.TreeTextEmptyError):
            tree.to_node("\n\t ")
    def test_to_node_first_indent_error(self):
        tree = TexTree()
        with self.assertRaises(TexTree.FirstNodeIndentError):
            tree.to_node("	A")
    def test_to_node_relative_indent_error(self):
        tree = TexTree()
        with self.assertRaises(LineAnalizer.RelativeIndentError):
            tree.to_node("A\n\t\tA11")
    def test_to_node_root_only(self):
        tree = TexTree()
        root = tree.to_node(TexTree.ROOT_NAME)
        self.assertEqual(root, tree.Root)
        self.assertEqual(RootNode, type(root))
    def test_to_node_root_and_nodes(self):
        tree = TexTree()
        root = tree.to_node(TexTree.ROOT_NAME + '\nA\n\tA1')
        self.assertEqual(root, tree.Root)
        self.assertEqual(RootNode, type(root))
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('A1', root.Children[0].Children[0].Name)
    def test_to_node_one(self):
        tree = TexTree()
        root = tree.to_node("A")
        def test_root():
            self.assertEqual(root, tree.Root)
            self.assertEqual("A", tree.Root.Nodes[0].Name)
        def test_nodes():
            self.assertEqual(1, len(root.Nodes))
            self.assertEqual("A", root.Nodes[0].Name)
        def test_parent():
            self.assertEqual(None, root.Parent)
            self.assertEqual(root, root.Nodes[0].Parent)
        def test_children():
            self.assertEqual(1, len(root.Children))
            self.assertEqual(0, len(root.Nodes[0].Children))
        test_root()             
        test_nodes()             
        test_parent()
        test_children()
    def test_to_node_list(self):
        tree = TexTree()
        root = tree.to_node("A\nB\nC")
        def test_root():
            self.assertEqual(root, tree.Root)
            self.assertEqual("A", tree.Root.Nodes[0].Name)
            self.assertEqual("B", tree.Root.Nodes[1].Name)
            self.assertEqual("C", tree.Root.Nodes[2].Name)
        def test_nodes():
            self.assertEqual(3, len(root.Nodes))
            self.assertEqual("A", root.Nodes[0].Name)
            self.assertEqual("B", root.Nodes[1].Name)
            self.assertEqual("C", root.Nodes[2].Name)
        def test_parent():
            self.assertEqual(None, root.Parent)
            for node in root.Nodes:
                self.assertEqual(root,  node.Parent)
        def test_children():
            self.assertEqual(3, len(root.Children))
            for node in root.Nodes:
                self.assertEqual(0, len(node.Children))
        test_root()             
        test_nodes()             
        test_parent()
        test_children()
    def test_to_node_nest(self):
        tree = TexTree()
        root = tree.to_node("A\n\tA1\n\t\tA11")
        def test_root():
            self.assertEqual(root, tree.Root)
            self.assertEqual("A",   tree.Root.Nodes[0].Name)
            self.assertEqual("A1",  tree.Root.Nodes[0].Children[0].Name)
            self.assertEqual("A11",  tree.Root.Nodes[0].Children[0].Children[0].Name)
        def test_nodes():
            self.assertEqual(3, len(root.Nodes))
            self.assertEqual("A",   root.Nodes[0].Name)
            self.assertEqual("A1",  root.Nodes[1].Name)
            self.assertEqual("A11", root.Nodes[2].Name)
        def test_parent():
            self.assertEqual(None,  root.Parent)
            self.assertEqual(root,  root.Children[0].Parent)
            self.assertEqual("A",    root.Children[0].Children[0].Parent.Name)
            self.assertEqual("A1",   root.Children[0].Children[0].Children[0].Parent.Name)
            self.assertEqual(0,  len(root.Children[0].Children[0].Children[0].Children))
        def test_children():
            self.assertEqual(1, len(root.Children))
            self.assertEqual("A", root.Children[0].Name)
            self.assertEqual(1, len(root.Children[0].Children))
            self.assertEqual("A1", root.Children[0].Children[0].Name)
            self.assertEqual(1, len(root.Children[0].Children[0].Children))
            self.assertEqual("A11", root.Children[0].Children[0].Children[0].Name)
        test_root()
        test_nodes()             
        test_parent()
        test_children()
    def test_to_node_nest_diff_2(self):
        tree = TexTree()
        root = tree.to_node("A\n\tA1\n\t\tA11\nB")
        def test_root():
            self.assertEqual(root, tree.Root)
            self.assertEqual("A",   tree.Root.Nodes[0].Name)
            self.assertEqual("A1",  tree.Root.Nodes[0].Children[0].Name)
            self.assertEqual("A11", tree.Root.Nodes[0].Children[0].Children[0].Name)
            self.assertEqual("A",   tree.Root.Children[0].Name)
            self.assertEqual("A1",  tree.Root.Children[0].Children[0].Name)
            self.assertEqual("A11", tree.Root.Children[0].Children[0].Children[0].Name)
            self.assertEqual("B",   tree.Root.Children[1].Name)
        def test_nodes():
            self.assertEqual(4, len(root.Nodes))
            self.assertEqual("A",   root.Nodes[0].Name)
            self.assertEqual("A1",  root.Nodes[1].Name)
            self.assertEqual("A11", root.Nodes[2].Name)
            self.assertEqual("B",   root.Nodes[3].Name)
        def test_parent():
            self.assertEqual(None,  root.Parent)
            self.assertEqual(root,  root.Children[0].Parent)
            self.assertEqual("A",   root.Children[0].Children[0].Parent.Name)
            self.assertEqual("A1",  root.Children[0].Children[0].Children[0].Parent.Name)
            self.assertEqual(root,  root.Children[1].Parent)
            self.assertEqual(0, len(root.Children[0].Children[0].Children[0].Children))
        def test_children():
            self.assertEqual(2, len(root.Children))
            self.assertEqual("A", root.Children[0].Name)
            self.assertEqual("B", root.Children[1].Name)
            self.assertEqual(1, len(root.Children[0].Children))
            self.assertEqual("A1",  root.Children[0].Children[0].Name)
            self.assertEqual(1, len(root.Children[0].Children[0].Children))
            self.assertEqual("A11", root.Children[0].Children[0].Children[0].Name)
            self.assertEqual(0, len(root.Children[1].Children))
        test_root()
        test_nodes()             
        test_parent()
        test_children()
    def test_to_node_tree_text_in_blank_line(self):
        tree = TexTree()
        root = tree.to_node("\n\n\nA\n\n\n\n\tA1\n\n\n\n\t\tA11\n\n\n\nB\n\n\n")
        def test_root():
            self.assertEqual(root, tree.Root)
            self.assertEqual("A",   tree.Root.Nodes[0].Name)
            self.assertEqual("A1",  tree.Root.Nodes[0].Children[0].Name)
            self.assertEqual("A11", tree.Root.Nodes[0].Children[0].Children[0].Name)
            self.assertEqual("A",   tree.Root.Children[0].Name)
            self.assertEqual("A1",  tree.Root.Children[0].Children[0].Name)
            self.assertEqual("A11", tree.Root.Children[0].Children[0].Children[0].Name)
            self.assertEqual("B",   tree.Root.Children[1].Name)
        def test_nodes():
            self.assertEqual(4, len(root.Nodes))
            self.assertEqual("A",   root.Nodes[0].Name)
            self.assertEqual("A1",  root.Nodes[1].Name)
            self.assertEqual("A11", root.Nodes[2].Name)
            self.assertEqual("B",   root.Nodes[3].Name)
        def test_parent():
            self.assertEqual(None,  root.Parent)
            self.assertEqual(root, root.Children[0].Parent)
            self.assertEqual("A",   root.Children[0].Children[0].Parent.Name)
            self.assertEqual("A1",  root.Children[0].Children[0].Children[0].Parent.Name)
            self.assertEqual(root, root.Children[1].Parent)
            self.assertEqual(0, len(root.Children[0].Children[0].Children[0].Children))
        def test_children():
            self.assertEqual(2, len(root.Children))
            self.assertEqual("A", root.Children[0].Name)
            self.assertEqual("B", root.Children[1].Name)
            self.assertEqual(1, len(root.Children[0].Children))
            self.assertEqual("A1",  root.Children[0].Children[0].Name)
            self.assertEqual(1, len(root.Children[0].Children[0].Children))
            self.assertEqual("A11", root.Children[0].Children[0].Children[0].Name)
            self.assertEqual(0, len(root.Children[1].Children))
        test_root()
        test_nodes()             
        test_parent()
        test_children()
    def test_to_node_INDENT_multiple_space(self):
        indent = '    '
        root_text = TexTree.ROOT_NAME + indent + 'root_attr1' + '\n'
        node_text = ('A' + indent + 'a' + '\n'
                + (indent * 1) + 'A1'   + indent + 'a1' + '\n'
                + (indent * 2) + 'A11'  + indent + 'a11' + '\n'
                + (indent * 3) + 'A111' + indent + 'a111' + '\n'
                + (indent * 3) + 'A112' + indent + 'a112' + '\n'
                + (indent * 1) + 'A2'   + indent + 'a2' + '\n'
                + 'B' + indent + 'b')
        tree_text = root_text + node_text 
        tree = TexTree(indent=indent)
        root = tree.to_node(tree_text)
        self.assertEqual(tree_text, tree.to_text())
        self.assertEqual(tree_text, tree.to_text(root))
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual('root_attr1', root.Attr)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('a', root.Children[0].Attr)
        self.assertEqual('A1', root.Children[0].Children[0].Name)
        self.assertEqual('a1', root.Children[0].Children[0].Attr)
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name)
        self.assertEqual('a11', root.Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A111', root.Children[0].Children[0].Children[0].Children[0].Name)
        self.assertEqual('a111', root.Children[0].Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A112', root.Children[0].Children[0].Children[0].Children[1].Name)
        self.assertEqual('a112', root.Children[0].Children[0].Children[0].Children[1].Attr)
        self.assertEqual('A2', root.Children[0].Children[1].Name)
        self.assertEqual('a2', root.Children[0].Children[1].Attr)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('b', root.Children[1].Attr)

    def test_to_text_root_name_only(self):
        tree_text = TexTree.ROOT_NAME
        tree = TexTree()
        root = tree.to_node(tree_text)
        self.assertEqual('', tree.to_text())
        self.assertEqual('', tree.to_text(root))
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual(None, root.Attr)
    def test_to_text_root_name_and_attr_only(self):
        tree_text = TexTree.ROOT_NAME + TexTree.INDENT + 'root_attr1'
        tree = TexTree()
        root = tree.to_node(tree_text)
        self.assertEqual(tree_text, tree.to_text())
        self.assertEqual(tree_text, tree.to_text(root))
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual('root_attr1', root.Attr)
    def test_to_text_root_and_node_name_only(self):
        root_text = TexTree.ROOT_NAME + '\n'
        node_text = '''A
\tA1
\t\tA11
\t\t\tA111
\t\t\tA112
\tA2
B'''
        tree_text = root_text + node_text 
        tree = TexTree()
        root = tree.to_node(tree_text)
        self.assertEqual(node_text, tree.to_text())
        self.assertEqual(node_text, tree.to_text(root))
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual(None, root.Attr)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual(None, root.Children[0].Attr)
        self.assertEqual('A1', root.Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Attr)
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A111', root.Children[0].Children[0].Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A112', root.Children[0].Children[0].Children[0].Children[1].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Children[1].Attr)
        self.assertEqual('A2', root.Children[0].Children[1].Name)
        self.assertEqual(None, root.Children[0].Children[1].Attr)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(None, root.Children[1].Attr)
    def test_to_text_root_attr_and_node_name(self):
        root_text = TexTree.ROOT_NAME + TexTree.INDENT + 'root_attr1' + '\n'
        node_text = '''A
\tA1
\t\tA11
\t\t\tA111
\t\t\tA112
\tA2
B'''
        tree_text = root_text + node_text 
        tree = TexTree()
        root = tree.to_node(tree_text)
        self.assertEqual(tree_text, tree.to_text())
        self.assertEqual(tree_text, tree.to_text(root))
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual('root_attr1', root.Attr)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('a', root.Children[0].Attr)
        self.assertEqual('A1', root.Children[0].Children[0].Name)
        self.assertEqual('a1', root.Children[0].Children[0].Attr)
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name)
        self.assertEqual('a11', root.Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A111', root.Children[0].Children[0].Children[0].Children[0].Name)
        self.assertEqual('a111', root.Children[0].Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A112', root.Children[0].Children[0].Children[0].Children[1].Name)
        self.assertEqual('a112', root.Children[0].Children[0].Children[0].Children[1].Attr)
        self.assertEqual('A2', root.Children[0].Children[1].Name)
        self.assertEqual('a2', root.Children[0].Children[1].Attr)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('b', root.Children[1].Attr)
    def test_to_text_node_name(self):
        tree_text = '''A
\tA1
\t\tA11
\t\t\tA111
\t\t\tA112
\tA2
B'''
        tree = TexTree()
        root = tree.to_node(tree_text)
        self.assertEqual(tree_text, tree.to_text())
        self.assertEqual(tree_text, tree.to_text(root))
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual(None, root.Attr)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual(None, root.Children[0].Attr)
        self.assertEqual('A1', root.Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Attr)
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A111', root.Children[0].Children[0].Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A112', root.Children[0].Children[0].Children[0].Children[1].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Children[1].Attr)
        self.assertEqual('A2', root.Children[0].Children[1].Name)
        self.assertEqual(None, root.Children[0].Children[1].Attr)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(None, root.Children[1].Attr)
    def test_to_text_root_name_and_node_name(self):
        root_text = TexTree.ROOT_NAME + '\n'
        node_text = '''A
\tA1
\t\tA11
\t\t\tA111
\t\t\tA112
\tA2
B'''
        tree_text = root_text + node_text 
        tree = TexTree()
        root = tree.to_node(tree_text)
        self.assertEqual(node_text, tree.to_text())
        self.assertEqual(node_text, tree.to_text(root))
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual(None, root.Attr)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual(None, root.Children[0].Attr)
        self.assertEqual('A1', root.Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Attr)
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A111', root.Children[0].Children[0].Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A112', root.Children[0].Children[0].Children[0].Children[1].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Children[1].Attr)
        self.assertEqual('A2', root.Children[0].Children[1].Name)
        self.assertEqual(None, root.Children[0].Children[1].Attr)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(None, root.Children[1].Attr)
    def test_to_text_root_attr_and_node_name(self):
        root_text = TexTree.ROOT_NAME + TexTree.INDENT + 'root_attr1' + '\n'
        node_text = '''A
\tA1
\t\tA11
\t\t\tA111
\t\t\tA112
\tA2
B'''
        tree_text = root_text + node_text 
        tree = TexTree()
        root = tree.to_node(tree_text)
        self.assertEqual(tree_text, tree.to_text())
        self.assertEqual(tree_text, tree.to_text(root))
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual('root_attr1', root.Attr)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual(None, root.Children[0].Attr)
        self.assertEqual('A1', root.Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Attr)
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A111', root.Children[0].Children[0].Children[0].Children[0].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A112', root.Children[0].Children[0].Children[0].Children[1].Name)
        self.assertEqual(None, root.Children[0].Children[0].Children[0].Children[1].Attr)
        self.assertEqual('A2', root.Children[0].Children[1].Name)
        self.assertEqual(None, root.Children[0].Children[1].Attr)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual(None, root.Children[1].Attr)
    def test_to_text_node_attr(self):
        tree_text = '''A\ta
\tA1\ta1
\t\tA11\ta11
\t\t\tA111\ta111
\t\t\tA112\ta112
\tA2\ta2
B\tb'''
        tree = TexTree()
        root = tree.to_node(tree_text)
        self.assertEqual(tree_text, tree.to_text())
        self.assertEqual(tree_text, tree.to_text(root))
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual(None, root.Attr)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('a', root.Children[0].Attr)
        self.assertEqual('A1', root.Children[0].Children[0].Name)
        self.assertEqual('a1', root.Children[0].Children[0].Attr)
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name)
        self.assertEqual('a11', root.Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A111', root.Children[0].Children[0].Children[0].Children[0].Name)
        self.assertEqual('a111', root.Children[0].Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A112', root.Children[0].Children[0].Children[0].Children[1].Name)
        self.assertEqual('a112', root.Children[0].Children[0].Children[0].Children[1].Attr)
        self.assertEqual('A2', root.Children[0].Children[1].Name)
        self.assertEqual('a2', root.Children[0].Children[1].Attr)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('b', root.Children[1].Attr)
    def test_to_text_root_attr_and_node_attr(self):
        root_text = TexTree.ROOT_NAME + TexTree.INDENT + 'root_attr1' + '\n'
        node_text = '''A\ta
\tA1\ta1
\t\tA11\ta11
\t\t\tA111\ta111
\t\t\tA112\ta112
\tA2\ta2
B\tb'''
        tree_text = root_text + node_text 
        tree = TexTree()
        root = tree.to_node(tree_text)
        self.assertEqual(tree_text, tree.to_text())
        self.assertEqual(tree_text, tree.to_text(root))
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual('root_attr1', root.Attr)
        self.assertEqual('A', root.Children[0].Name)
        self.assertEqual('a', root.Children[0].Attr)
        self.assertEqual('A1', root.Children[0].Children[0].Name)
        self.assertEqual('a1', root.Children[0].Children[0].Attr)
        self.assertEqual('A11', root.Children[0].Children[0].Children[0].Name)
        self.assertEqual('a11', root.Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A111', root.Children[0].Children[0].Children[0].Children[0].Name)
        self.assertEqual('a111', root.Children[0].Children[0].Children[0].Children[0].Attr)
        self.assertEqual('A112', root.Children[0].Children[0].Children[0].Children[1].Name)
        self.assertEqual('a112', root.Children[0].Children[0].Children[0].Children[1].Attr)
        self.assertEqual('A2', root.Children[0].Children[1].Name)
        self.assertEqual('a2', root.Children[0].Children[1].Attr)
        self.assertEqual('B', root.Children[1].Name)
        self.assertEqual('b', root.Children[1].Attr)

class TestAttribute(unittest.TestCase):
    def test(self):
        tree_text = 'A\tsome_attr'
        tree = TexTree()
        root = tree.to_node(tree_text)
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertTrue(hasattr(root.Children[0], "Attr"))
        self.assertEqual(property, type(type(root.Children[0]).Attr))
        self.assertEqual(None, root.Attr)

import shlex, argparse
class TestRootAttributeDeserializer(unittest.TestCase):
    def test_argparse(self):
        class MyRootAttributeDeserializer(textree.RootAttributeDeserializer):
            def deserialize(self, line_attr):
                if line_attr is None: line_attr = ''
                parser = argparse.ArgumentParser(add_help=False)
                parser.add_argument('-w', '--width', type=int, nargs='?', default=640, help='image width.')
                parser.add_argument('-h', '--height', type=int, nargs='?', default=480, help='image height.')
                parser.add_argument('-n', '--name', type=str, nargs='?', default='new.xcf', help='output of Xcf file name.')
                return parser.parse_args(shlex.split(line_attr))
        class MyRootAttributeSerializer(textree.RootAttributeSerializer):
            def serialize(self, node):
                line_attr = ''
                if hasattr(node.Attr, 'width')  and node.Attr.width  != 640: line_attr+="-w {} ".format(node.Attr.width)
                if hasattr(node.Attr, 'height') and node.Attr.height != 480: line_attr+="-h {} ".format(node.Attr.width)
                if hasattr(node.Attr, 'name')   and node.Attr.name   != 'new.xcf': line_attr+='-n "{}" '.format(node.Attr.name)
                return line_attr.strip()
        tree_text = '<ROOT>\nA'
        tree = TexTree(root_deserializer=textree.RootDeserializer(MyRootAttributeDeserializer()), root_serializer=textree.RootSerializer(MyRootAttributeSerializer()))
        root = tree.to_node(tree_text)
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual(argparse.Namespace, type(root.Attr))
        self.assertEqual(640, root.Attr.width)
        self.assertEqual(480, root.Attr.height)
        self.assertEqual('new.xcf', root.Attr.name)
        self.assertEqual(1, len(root.Nodes))
        self.assertEqual('A', root.Nodes[0].Name)
        self.assertEqual(None, root.Nodes[0].Attr)

        tree_text = '<ROOT>\t-w666 -h 444 --name " \\" NAME \\" "\nA'
        root = tree.to_node(tree_text)
        self.assertEqual(argparse.Namespace, type(root.Attr))
        self.assertEqual(666, root.Attr.width)
        self.assertEqual(444, root.Attr.height)
        self.assertEqual(' " NAME " ', root.Attr.name)

        tree_text = '<ROOT>\t-h 444 --name " \\" NAME \\" "\nA'
        root = tree.to_node(tree_text)
        self.assertEqual(640, root.Attr.width)
        self.assertEqual(444, root.Attr.height)
        self.assertEqual(' " NAME " ', root.Attr.name)

    def test_json(self):
        import json, collections
        class MyRootAttributeDeserializer(textree.RootAttributeDeserializer):
            def deserialize(self, line_attr):
                decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
                attr = decoder.decode('{"width":640, "height":480, "name":"new.xcf"}') # default value
                if line_attr is None: return attr
                inpt = decoder.decode(line_attr)
                attr.update(inpt)
                return attr
        class MyRootAttributeSerializer(textree.RootAttributeSerializer):
            def serialize(self, node):
                return json.dumps(node.Attr)
        tree_text = '<ROOT>\nA'
        tree = TexTree(root_deserializer=textree.RootDeserializer(MyRootAttributeDeserializer()), root_serializer=textree.RootSerializer(MyRootAttributeSerializer()))
        root = tree.to_node(tree_text)
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual(collections.OrderedDict, type(root.Attr))
        self.assertEqual(640, root.Attr['width'])
        self.assertEqual(480, root.Attr['height'])
        self.assertEqual('new.xcf', root.Attr['name'])
        self.assertEqual(1, len(root.Nodes))
        self.assertEqual('A', root.Nodes[0].Name)
        self.assertEqual(None, root.Nodes[0].Attr)

        tree_text = '<ROOT>\t{"width": 666, "height": 444, "name": " \\" NAME \\" "}\nA'
        root = tree.to_node(tree_text)
        self.assertEqual(collections.OrderedDict, type(root.Attr))
        self.assertEqual(666, root.Attr['width'])
        self.assertEqual(444, root.Attr['height'])
        self.assertEqual(' " NAME " ', root.Attr['name'])

        tree_text = '<ROOT>\t{"height": 444, "name": " \\" NAME \\" "}\nA'
        root = tree.to_node(tree_text)
        self.assertEqual(640, root.Attr['width'])
        self.assertEqual(444, root.Attr['height'])
        self.assertEqual(' " NAME " ', root.Attr['name'])

    def test_json_customize(self):
        import json, collections
        class MyRootAttributeDeserializer(textree.RootAttributeDeserializer):
            def deserialize(self, line_attr):
                def parse_kv_pairs(text, item_sep=" ", value_sep="="):
                    lexer = shlex.shlex(text, posix=True)
                    lexer.whitespace = item_sep
                    lexer.wordchars += value_sep
                    return dict(word.split(value_sep) for word in lexer)
                decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
                attr = decoder.decode('{"width":640, "height":480, "name":"new.xcf"}') # default value
                if line_attr is None: return attr
                inpt = parse_kv_pairs(line_attr)
                attr.update(inpt)
                attr['width'] = int(attr['width'])
                attr['height'] = int(attr['height'])
                return attr

        class MyRootAttributeSerializer(textree.RootAttributeSerializer):
            def serialize(self, attr):
                def delete_braces(attr_str):
                    if '{' == attr_str[0]: attr_str = attr_str[1:]
                    if '}' == attr_str[-1]: attr_str = attr_str[:-1]
                    return attr_str
                def delete_key_quotes(attr_str):
                    rmidxs = []
                    idxs = [i for i, x in enumerate(attr_str) if '=' == x]
                    for idx in idxs:
                        if '"' == attr_str[idx-1]:
                            start_quote_idx = idx-1-1
                            while -1 < start_quote_idx:
                                if '"' == attr_str[start_quote_idx]: break
                                else: start_quote_idx-=1
                            if -1 < start_quote_idx:
                                rmidxs.append(start_quote_idx)
                                rmidxs.append(idx-1)
                    res = str(attr_str)
                    diff = 0
                    for rmidx in rmidxs:
                        if   0 == rmidx: res = res[rmidx+1-diff:]
                        elif rmidx == len(attr_str)-1: res = res[:rmidx-diff]
                        else: res = res[:rmidx-diff] + res[rmidx+1-diff:]
                        diff+=1
                    return res
#  https://stackoverflow.com/questions/11716687/why-does-str-split-not-take-keyword-arguments/11716792#11716792
#                attr_str = json.dumps(attr, separators=(' ','='))
#                attr_str = json.dumps(attr, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding="utf-8", default=None, sort_keys=False, **kw)
#                attr_str = json.dumps(attr, False, True, True, True, None, None, (' ','='))
                attr_str = json.dumps(attr, False, True, True, True, None, None, (' ','='), "utf-8", None, False)
                attr_str = delete_key_quotes(delete_braces(attr_str))
                attr_str = attr_str.replace('width=640', '')
                attr_str = attr_str.replace('height=480', '')
                attr_str = attr_str.replace('name="new.xcf"', '')
                return None if attr_str is None else attr_str.strip()
        tree_text = '<ROOT>\nA'
        tree = TexTree(root_deserializer=textree.RootDeserializer(attr_des=MyRootAttributeDeserializer()), root_serializer=textree.RootSerializer(attr_ser=MyRootAttributeSerializer()))
        root = tree.to_node(tree_text)
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual(collections.OrderedDict, type(root.Attr))
        self.assertEqual(640, root.Attr['width'])
        self.assertEqual(480, root.Attr['height'])
        self.assertEqual('new.xcf', root.Attr['name'])
        self.assertEqual(1, len(root.Nodes))
        self.assertEqual('A', root.Nodes[0].Name)
        self.assertEqual(None, root.Nodes[0].Attr)

        tree_text = '<ROOT>\twidth=666 height=444 name=" \\" NAME \\" "\nA'
        root = tree.to_node(tree_text)
        self.assertEqual(collections.OrderedDict, type(root.Attr))
        self.assertEqual(666, root.Attr['width'])
        self.assertEqual(444, root.Attr['height'])
        self.assertEqual(' " NAME " ', root.Attr['name'])

        tree_text = '<ROOT>\theight=444 name=" \\" NAME \\" "\nA'
        root = tree.to_node(tree_text)
        self.assertEqual(640, root.Attr['width'])
        self.assertEqual(444, root.Attr['height'])
        self.assertEqual(' " NAME " ', root.Attr['name'])
        self.assertEqual(tree_text, tree.to_text())

class TestNodeAttributeDeserializer(unittest.TestCase):
    def test_argparse(self):
        class MyNodeAttributeDeserializer(textree.NodeAttributeDeserializer):
            def deserialize(self, line_attr):
                if line_attr is None: line_attr = ''
                parser = argparse.ArgumentParser(add_help=False)
                parser.add_argument('width', type=int, nargs='?', default=640, help='Layer width.')
                parser.add_argument('height', type=int, nargs='?', default=480, help='Layer height.')
                return parser.parse_args(shlex.split(line_attr))
        class MyNodeAttributeSerializer(textree.NodeAttributeSerializer):
            def serialize(self, node):
                line_attr = ''
                if hasattr(node.Attr, 'width') : line_attr+="{} ".format(node.Attr.width)
                if hasattr(node.Attr, 'height'): line_attr+="{} ".format(node.Attr.width)
                return line_attr.strip()
        tree_text = '<ROOT>\nA'
        tree = TexTree(node_deserializer=textree.NodeDeserializer(MyNodeAttributeDeserializer()), node_serializer=textree.NodeSerializer(MyNodeAttributeSerializer()))
        root = tree.to_node(tree_text)
        self.assertEqual(argparse.Namespace, type(root.Nodes[0].Attr))
        self.assertEqual(640, root.Nodes[0].Attr.width)
        self.assertEqual(480, root.Nodes[0].Attr.height)

        tree_text = '<ROOT>\t-w666 -h 444 --name " \\" NAME \\" "\nA\t66 44'
        root = tree.to_node(tree_text)
        self.assertEqual(argparse.Namespace, type(root.Nodes[0].Attr))
        self.assertEqual(66, root.Nodes[0].Attr.width)
        self.assertEqual(44, root.Nodes[0].Attr.height)

        tree_text = '<ROOT>\t-h 444 --name " \\" NAME \\" "\nA\t66'
        root = tree.to_node(tree_text)
        self.assertEqual(argparse.Namespace, type(root.Nodes[0].Attr))
        self.assertEqual(66, root.Nodes[0].Attr.width)
        self.assertEqual(480, root.Nodes[0].Attr.height)

    def test_json(self):
        import json, collections
        class MyNodeAttributeDeserializer(textree.NodeAttributeDeserializer):
            def deserialize(self, line_attr):
                decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
                attr = decoder.decode('{"width":640, "height":480, "name":"new.xcf"}') # default value
                if line_attr is None: return attr
                inpt = decoder.decode(line_attr)
                attr.update(inpt)
                return attr
        class MyNodeAttributeSerializer(textree.NodeAttributeSerializer):
            def serialize(self, node):
                return json.dumps(node.Attr)
        tree_text = '<ROOT>\nA'
        tree = TexTree(node_deserializer=textree.NodeDeserializer(MyNodeAttributeDeserializer()), node_serializer=textree.NodeSerializer(MyNodeAttributeSerializer()))
        root = tree.to_node(tree_text)
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual(collections.OrderedDict, type(root.Nodes[0].Attr))
        self.assertEqual(640, root.Nodes[0].Attr['width'])
        self.assertEqual(480, root.Nodes[0].Attr['height'])
        self.assertEqual('new.xcf', root.Nodes[0].Attr['name'])

        tree_text = '<ROOT>\nA\t{"width": 666, "height": 444, "name": " \\" NAME \\" "}'
        root = tree.to_node(tree_text)
        self.assertEqual(collections.OrderedDict, type(root.Nodes[0].Attr))
        self.assertEqual(666, root.Nodes[0].Attr['width'])
        self.assertEqual(444, root.Nodes[0].Attr['height'])
        self.assertEqual(' " NAME " ', root.Nodes[0].Attr['name'])

        tree_text = '<ROOT>\nA\t{"height": 444, "name": " \\" NAME \\" "}'
        root = tree.to_node(tree_text)
        self.assertEqual(collections.OrderedDict, type(root.Nodes[0].Attr))
        self.assertEqual(640, root.Nodes[0].Attr['width'])
        self.assertEqual(444, root.Nodes[0].Attr['height'])
        self.assertEqual(' " NAME " ', root.Nodes[0].Attr['name'])

    def test_json_customize(self):
        import json, collections
        class MyNodeAttributeDeserializer(textree.NodeAttributeDeserializer):
            def deserialize(self, line_attr):
                def parse_kv_pairs(text, item_sep=" ", value_sep="="):
                    lexer = shlex.shlex(text, posix=True)
                    lexer.whitespace = item_sep
                    lexer.wordchars += value_sep
                    return dict(word.split(value_sep) for word in lexer)
                decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
                attr = decoder.decode('{"width":640, "height":480, "name":"new.xcf"}') # default value
                if line_attr is None: return attr
                inpt = parse_kv_pairs(line_attr)
                attr.update(inpt)
                attr['width'] = int(attr['width'])
                attr['height'] = int(attr['height'])
                return attr

        class MyNodeAttributeSerializer(textree.NodeAttributeSerializer):
            def serialize(self, attr):
                def delete_braces(attr_str):
                    if '{' == attr_str[0]: attr_str = attr_str[1:]
                    if '}' == attr_str[-1]: attr_str = attr_str[:-1]
                    return attr_str
                def delete_key_quotes(attr_str):
                    rmidxs = []
                    idxs = [i for i, x in enumerate(attr_str) if '=' == x]
                    for idx in idxs:
                        if '"' == attr_str[idx-1]:
                            start_quote_idx = idx-1-1
                            while -1 < start_quote_idx:
                                if '"' == attr_str[start_quote_idx]: break
                                else: start_quote_idx-=1
                            if -1 < start_quote_idx:
                                rmidxs.append(start_quote_idx)
                                rmidxs.append(idx-1)
                    res = str(attr_str)
                    diff = 0
                    for rmidx in rmidxs:
                        if   0 == rmidx: res = res[rmidx+1-diff:]
                        elif rmidx == len(attr_str)-1: res = res[:rmidx-diff]
                        else: res = res[:rmidx-diff] + res[rmidx+1-diff:]
                        diff+=1
#                        print(rmidx, res)
                    return res
#  https://stackoverflow.com/questions/11716687/why-does-str-split-not-take-keyword-arguments/11716792#11716792
#                attr_str = json.dumps(attr, separators=(' ','='))
#                attr_str = json.dumps(attr, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding="utf-8", default=None, sort_keys=False, **kw)
#                attr_str = json.dumps(attr, False, True, True, True, None, None, (' ','='))
                attr_str = json.dumps(attr, False, True, True, True, None, None, (' ','='), "utf-8", None, False)
                attr_str = delete_key_quotes(delete_braces(attr_str))
                attr_str = attr_str.replace('width=640', '')
                attr_str = attr_str.replace('height=480', '')
                attr_str = attr_str.replace('name="new.xcf"', '')
                return None if attr_str is None else attr_str.strip()
        tree_text = '<ROOT>\nA'
        tree = TexTree(node_deserializer=textree.NodeDeserializer(MyNodeAttributeDeserializer()), node_serializer=textree.NodeSerializer(MyNodeAttributeSerializer()))
        root = tree.to_node(tree_text)
        self.assertEqual(TexTree.ROOT_NAME, root.Name)
        self.assertEqual(None, root.Attr)
        self.assertEqual(1, len(root.Nodes))
        self.assertEqual('A', root.Nodes[0].Name)
        self.assertEqual(collections.OrderedDict, type(root.Nodes[0].Attr))
        self.assertEqual(640, root.Nodes[0].Attr['width'])
        self.assertEqual(480, root.Nodes[0].Attr['height'])

        tree_text = '<ROOT>\nA\twidth=66 height=44'
        root = tree.to_node(tree_text)
        self.assertEqual(collections.OrderedDict, type(root.Nodes[0].Attr))
        self.assertEqual(66, root.Nodes[0].Attr['width'])
        self.assertEqual(44, root.Nodes[0].Attr['height'])

        tree_text = 'A\theight=44'
#        tree_text = '<ROOT>\nA\theight=44'
        root = tree.to_node(tree_text)
        self.assertEqual(640, root.Nodes[0].Attr['width'])
        self.assertEqual(44, root.Nodes[0].Attr['height'])
        self.assertEqual(tree_text, tree.to_text())



if __name__ == '__main__':
    unittest.main()

