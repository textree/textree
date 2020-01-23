#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a node object from the tree text."""
from collections import OrderedDict
class Node(object):
    """A node in the tree."""
    class NameTypeError(TypeError): pass
    class ParentTypeError(TypeError): pass
    class ChildrenTypeError(TypeError): pass
    class ChildTypeError(TypeError): pass
    def __init__(self, line, name=None, parent=None, children=None, attr=None):
        self.__set_name(name, line)
        self.Parent = parent
        self.Children = children
        self.__attr = attr
    def __set_name(self, name, line=None):
        self.__name = name
        if name is None and line is not None: self.__name = line.strip()
        if not isinstance(self.__name, str): raise Node.NameTypeError('Names should be of type str.')
    def __set_parent(self, parent):
        self.__parent = parent
        if self.__parent is None: return
        elif not isinstance(parent, Node): raise Node.ParentTypeError('Parent should be of type Node.')
        else: pass
    def __set_children(self, children):
        if children is None: self.__children = NodeList(children)
        elif isinstance(children, NodeList): self.__children = children
        elif hasattr(children, '__iter__'): self.__children = NodeList(children)
        else: raise Node.ChildrenTypeError('Children should be of type Node or list or NodeList.')
    @property
    def Name(self): return self.__name
    @property
    def Parent(self): return self.__parent
    @property
    def Children(self): return self.__children
    @Name.setter
    def Name(self, value): self.__set_name(value)
    @Parent.setter
    def Parent(self, value): self.__set_parent(value)
    @Children.setter
    def Children(self, value): self.__set_children(value)
    @property
    def Path(self): return Path.get_path(self)
    @property
    def Attr(self): return self.__attr
#    @Attr.setter
#    def Attr(self, value): self.__attr = value
    @property
    def Index(self): return Path.index(self)

    def to_first(self, path=None): self.to_index(0, path)
    def to_last(self, path=None):
        if not isinstance(self, RootNode):
            index = len(self.Parent.Children) if path is None else len(Path.select(self, path).Parent.Children)
            self.to_index(index, path)
    def to_prev(self, path=None):
        index = Path.index(self, path)-1
        # index-1: If you are at the same level as yourself
        # index  : If you are at a different level    
        if path is not None:
            if self.Parent != Path.select(self, path).Parent:
                index+=1
        if index < 0: index = 0
        self.to_index(index, path)
    def to_next(self, path=None):
        index = Path.index(self, path)+1
        self.to_index(index, path)
    def to_index(self, index, path=None):
        base = self if path is None else Path.select(self, path)
        self.Parent.Children.remove(self)
        base.Parent.Children.insert(index, self)
        
    def to_children_first(self, path=None):
        self.to_children_index(0, path)
    def to_children_last(self, path=None):
        base = self if path is None else Path.select(self, path)
        index = len(base.Children)
        self.to_children_index(index, path)
    def to_children_index(self, index, path=None):
        base = self if path is None else Path.select(self, path)
        if base == self: raise ValueError('You cannot make yourself your own child.')
        self.Parent.Children.remove(self)
        base.Children.insert(index, self)
 
    def to_ancestor_first(self, indent=1):
        self.to_ancestor_index(0, indent)
    def to_ancestor_last(self, indent=1):
        index = len(Path.get_ancestor(self, indent).Children)
        self.to_ancestor_index(index, indent)
    def to_ancestor_prev(self, indent=1):
        ancestor = Path.get_ancestor(self, indent)
        index = self.Parent.Children.index(self)-1 if 1 == abs(indent) else Path.index(ancestor)
        if index < 0: index = 0
        self.to_ancestor_index(index, indent)
    def to_ancestor_next(self, indent=1):
        ancestor = Path.get_ancestor(self, indent)
        index = self.Parent.Children.index(self)+1 if 1 == indent else Path.index(ancestor)+1
        self.to_ancestor_index(index, indent)
    def to_ancestor_index(self, index, indent=1):
        if 0 == indent: raise ValueError('You cannot make yourself your own child.')
        ancestor = Path.get_ancestor(self, indent)
        self.Parent.Children.remove(self)
        ancestor.Children.insert(index, self)

    def insert_first(self, node, path='./'):
        self.insert_index(node, path, 0)
    def insert_last(self, node, path='./'):
        base = Path.select(self, path)
        if isinstance(base, RootNode): raise ValueError('Cannot insert as sibling of root.')
        self.insert_index(node, path, len(base.Parent.Children))
    def insert_prev(self, node, path='./'):
        base = Path.select(self, path)
        index = Path.index(base)
        if index < 0: index = 0
        self.insert_index(node, path, index)
    def insert_next(self, node, path='./'):
        base = Path.select(self, path)
        index = Path.index(base)+1
        self.insert_index(node, path, index)
    def insert_index(self, node, path, index):
        base = Path.select(self, path)
        if isinstance(base, RootNode): raise ValueError('Cannot insert as sibling of root.')
        else: base = base.Parent
        base.Children.insert(index, node)

    def insert_children_first(self, node, path='./'):
        self.insert_children_index(node, path, 0)
    def insert_children_last(self, node, path='./'):
        base = Path.select(self, path)
        self.insert_children_index(node, path, len(base.Children))
    def insert_children_index(self, node, path, index):
        base = Path.select(self, path)
        base.Children.insert(index, node)

    def select(self, path): return Path.select(self, path)
    def delete(self, path=None):
        # 子孫を削除する
        def delete_descendants(node):
            for child in node.Children:
                delete_descendants(child)
            node.Parent.Children.remove(node)
        base = self if path is None else Path.select(self, path)
        if isinstance(base, RootNode): raise ValueError('Cannot delete root.')
        delete_descendants(base)

class NodeList(list):
    """A list with only node type elements."""
    def __init__(self, arg=None):
        if   arg is None: super(NodeList, self).__init__()
        elif hasattr(arg, "__iter__"):
            for item in arg:
                if not isinstance(item, Node): 
                    raise Node.ChildTypeError('The argument element is invalid. If the argument is a collection, its elements should be of type Node.')
            super(NodeList, self).__init__(arg)
        else: 
            raise Node.ChildTypeError('Argument type is invalid. Should be a None or collection containing Node.')
    def append(self, value):
        self.__is_node(value)
        list.append(self, value)
    def extend(self, values):
        for value in values:
            self.__is_node(value)
        list.extend(self, values)
    def insert(self, index, value):
        self.__is_node(value)
        list.insert(self, index, value)
    def __is_node(self, value):
        if not isinstance(value, Node):
            raise Node.ChildTypeError('Elements of children should be of type Node. {}'.format(type(value)))
        return True

class Path(object):
    class ReadOnlyClass(type):
        @property
        def DELIMITER(cls): return cls._DELIMITER
    __metaclass__ = ReadOnlyClass
    _DELIMITER = '/'
    @staticmethod
    def select(base_node, path):
        if not isinstance(base_node, Node): raise TypeError('base_node should be of type Node.: {}'.format(type(base_node)))
        if not isinstance(path, str): raise TypeError('path should be of type str.: {}'.format(type(path)))
        paths = path.split(Path.DELIMITER)
        if '' == paths[-1]: paths = paths[:-1]
        base = base_node
        base_idx = 0
        if path.startswith('./'): base_idx+=1
        else:
            for i, path in enumerate(paths):
                if '..' == path:
                    if base is None: raise ValueError('You cannot go back to your ancestors than the root.: "{}", "{}"'.format(path, paths[:i+1]))
                    base = base.Parent
                    base_idx+=1
                    if base is None: raise ValueError('You cannot go back to your ancestors than the root.: "{}", "{}"'.format(path, paths[:i+1]))
        paths = paths[base_idx:]
        for i, path in enumerate(paths):
            child = filter(lambda c: c.Name == path, base.Children)
            if len(child) < 1: raise ValueError('The node at the specified path was not found. : "{}", {}'.format(path, paths[:i+1]))
            base = child[0]
        if base is None: raise ValueError('You cannot go back to your ancestors than the root.: "{}", "{}"'.format(path, paths[base_idx:]))
        return base
    
    @staticmethod
    def index(base_node, path=None):
        if path is None:
            if isinstance(base_node, RootNode): return 0
            else: return base_node.Parent.Children.index(base_node)
        else:
            base = Path.select(base_node, path)
            if isinstance(base, RootNode): return 0
            else: return base.Parent.Children.index(base)

    @staticmethod
    def get_ancestor(base_node, indent):
        res = base_node
        for i in range(abs(indent)):
            res = res.Parent
            if res is None: raise ValueError('You cannot go back beyond root.')
        return res
        
    @staticmethod
    def get_path(node):
        if not isinstance(node, Node): raise ValueError('The first argument node should be of type Node.')
        ancestors = []
        base = node
        while (not isinstance(base, RootNode)):
            ancestors.append(base.Name)
            base = base.Parent
        ancestors.reverse()
        return Path.DELIMITER.join(ancestors)

class TexTree(object):
    class ReadOnlyClass(type):
        @property
        def INDENT(cls): return cls._INDENT
        @property
        def ROOT_NAME(cls): return cls._ROOT_NAME
    __metaclass__ = ReadOnlyClass
    _INDENT = '\t'
    _ROOT_NAME = '<ROOT>'
    """Generate a node from the tree text."""
    class TreeTextTypeError(Exception):
        """Tree text should be of type string."""
        pass
    class TreeTextEmptyError(Exception):
        """Tree text is empty."""
        pass
    class FirstNodeIndentError(Exception):
        """Indent is invalid. The first element must not be indented."""
        pass
    def __init__(self, indent='\t', root_name='<ROOT>', node_deserializer=None, node_serializer=None, root_deserializer=None, root_serializer=None):
        self.__indent = indent if isinstance(indent , str) and 0 < len(indent) else TexTree.INDENT
        self.__root_name = root_name if isinstance(root_name, str) and 0 < len(root_name) else TexTree.ROOT_NAME
        self.__root = None
        self.__set_root_deserializer(root_deserializer)
        self.__set_root_serializer(root_serializer)
        self.__set_node_deserializer(node_deserializer)
        self.__set_node_serializer(node_serializer)
    def __set_node_deserializer(self, node_deserializer): self.__set_lizer("__node_deserializer", node_deserializer, NodeDeserializer)
    def __set_node_serializer(self, node_serializer):     self.__set_lizer("__node_serializer",   node_serializer,   NodeSerializer)
    def __set_root_deserializer(self, root_deserializer): self.__set_lizer("__root_deserializer", root_deserializer, RootDeserializer)
    def __set_root_serializer(self, root_serializer):     self.__set_lizer("__root_serializer",   root_serializer,   RootSerializer)
    def __set_lizer(self, name, value, typ):
        name = '_' + self.__class__.__name__  + name
        setattr(self, name, value)
        target = getattr(self, name)
        if target is None: setattr(self, name, typ()); target = getattr(self, name);
        if not isinstance(target, typ): raise TypeError('{} should be of type {}. : {}'.format(name, typ, type(value)));
        indent_name = '_' + target.__class__.__name__  + '__indent'
        if hasattr(target, indent_name):
            setattr(target, indent_name, self.Indent)
    def to_text_lines(self, base=None):
        if base is None: base = self.Root
        parents = []
        def get_line(node, lines, parents):
            line = self.__node_serializer.serialize(node, parents)
            if line is not None and 0 < len(line): lines.append(line)
            parents.append(node)
            for child in node.Children:
                get_line(child, lines, parents)
            parents.pop()
        lines = []
        if isinstance(base, RootNode):
            if base.Attr is not None and 0 < len(base.Attr):
                lines.append(self.__root_serializer.serialize(base))
            for top in base.Children:
                get_line(top, lines, parents)
        else: get_line(base, lines, parents)
        return lines
    def to_text(self, base=None):
        return '\n'.join(self.to_text_lines(self.Root if base is None else base))
    def to_node(self, tree_text):
        """Generate a node from the tree text. Returns the root node."""
        def is_tree_text_invalid_type():
            if tree_text is None or not isinstance(tree_text, str): raise TexTree.TreeTextTypeError('Tree text should be of type string.')
        is_tree_text_invalid_type()
        lines = tree_text.split("\n")
        lines = filter(lambda line: '' != line.strip(), lines)
        def is_tree_text_not_empty():
            if 0 == len(lines): raise TexTree.TreeTextEmptyError("Tree text is empty. Please enter at least one line of tree text.")
        def is_zero_indent_first_line():
            if self.Indent == lines[0][0]: raise TexTree.FirstNodeIndentError("Indent is invalid. The first element must not be indented.")
        is_tree_text_not_empty()
        is_zero_indent_first_line()
        return self.__to_node(lines)
    def __to_node(self, lines):
        def get_latest_node(parents):
            return parents[-1].Children[-1] if 0 < len(parents[-1].Children) else parents[-1]
        def get_root(ana):
            return self.__root_deserializer.deserialize(ana)
        def add_node(ana, parents):
            node = self.__node_deserializer.deserialize(ana, parents[-1], parents=parents)
            parents[-1].Children.append(node)
            if not ana.IsLast:
                if   ana.IsParent: parents.append(get_latest_node(parents))
                else: [parents.pop() for i in range(ana.IndentationDiff)]
        ana = LineAnalizer(lines, INDENT=self.Indent, ROOT_NAME=self.RootName)
        root = get_root(ana)
        parents = [root]
        for name, attr in ana.analize_nodes():
            add_node(ana, parents)
        self.__root = root
        root.Nodes = self.Nodes
        return root
    @property
    def Indent(self): return self.__indent
    @property
    def RootName(self): return self.__root_name 
    @property
    def Root(self): return self.__root
    @property
    def Nodes(self):
        def nodes(node, _list):
            _list.append(node)
            for i, child in enumerate(node.Children):
                nodes(child, _list)
        _list = []
        for i, child in enumerate(self.__root.Children):
            nodes(child, _list)
        return _list

class LineAnalizer(object):
    """Analyze a line of tree text."""
    class RelativeIndentError(Exception):
        """The relative indent value is invalid. The indentation difference between the lines before and after is only 0, +1 or less than -1."""
        pass
    def __init__(self, lines, INDENT=TexTree.INDENT, ROOT_NAME=TexTree.ROOT_NAME):
        if lines is None: raise ValueError('lines should be of type list with elements of type str.')
        if 0 == len(lines): raise ValueError('lines should be a list type with one or more str elements.')
        for line in lines:
            if not isinstance(line, str): raise TypeError('lines should be of type list with elements of type str.')
        self.__lines = lines
        self.__INDENT = INDENT
        self.__ROOT_NAME = ROOT_NAME
        self.__index = 0
        self.__indent = 0
        self.__next_indent = None
        self.__prev_indent = None
        self.__name = None
        self.__attr = None
        self.__root_line = None
        _, self.__root_name, self.__root_attr = self.__get_triple()
        if self.__root_name == self.__ROOT_NAME:
            self.__root_line = lines[0]
            self.__lines = lines[1:]
        else:
            self.__root_name = None
            self.__root_attr = None
    @property
    def RootName(self): return self.__root_name
    @property
    def RootAttr(self): return self.__root_attr
    def analize_nodes(self):
        for i, line in enumerate(self.__lines):
            self.__calc_indents(i)
            self.__raise_indent_error()
            self.__indent, self.__name, self.__attr = self.__get_triple()
            yield self.__name, self.__attr
            self.__index+=1
    def __calc_indents(self, i):
        if   self.IsLast:
            self.__prev_indent = self.__get_indent_num(i-1)
            self.__next_indent = None
        elif self.IsFirst: 
            self.__prev_indent = None
            self.__next_indent = self.__get_indent_num(i+1)
        else:
            self.__prev_indent = self.__get_indent_num(i-1)
            self.__next_indent = self.__get_indent_num(i+1)
        self.__indent = self.__get_indent_num()
    @property
    def IsLast(self): return len(self.__lines) <= self.__index+1 
    @property
    def IsFirst(self): return 0 == self.Index
    @property
    def IsLeaf(self): return not self.IsParent
    @property
    def IsParent(self): return self.__indent+1 == self.__next_indent
    @property
    def Line(self): return self.__lines[self.__index]
    @property
    def Indent(self): return self.__indent
    @property
    def Index(self): return self.__index
    @property
    def IndentStr(self):
        if 0 == self.__indent: return ''
        else: self.__INDENT * self.__indent
    @property
    def Name(self): return self.__name
    @property
    def Attr(self): return self.__attr
    @property
    def IndentationDiff(self):
        if self.IsLast: return abs(self.__indent - self.__prev_indent)
        else:           return abs(self.__indent - self.__next_indent)
    def __get_indent_num(self, line_index=-1):
        line = self.Line if line_index < 0 else self.__lines[line_index]
        char_index = 0
        while self.__INDENT == line[char_index:char_index+len(self.__INDENT)]: char_index+=len(self.__INDENT)
        return char_index / len(self.__INDENT)
    # 階層タブ＋行の名前＋タブ＋属性
    # (indent_level, line_name, line_attr)
    def __get_triple(self):
        indent = self.__get_indent_num()
        line = self.Line[(len(self.__INDENT) * indent):]
        pos = line.find(self.__INDENT)
        if -1 == pos: return (indent, line, None)
        else: return (indent, line[:pos], line[pos+len(self.__INDENT):])
    def __is_indent_error(self):
        if self.IsLast: return self.__prev_indent+1 < self.__indent
        else: return self.__indent+1 < self.__next_indent
    def __raise_indent_error(self):
        if self.__is_indent_error():
            raise LineAnalizer.RelativeIndentError("The relative indent value is invalid. The indentation difference between the lines before and after is only 0, +1 or less than -1.")

class RootNode(Node):# pass
    def __init__(self, line=None, name=None, parent=None, children=None, attr=None):
        if line is None: line = TexTree.ROOT_NAME
        super(RootNode, self).__init__(line, name, parent, children, attr)

class RootDeserializer(object):
    """Convert a Node to a line of tree text."""
    def __init__(self, attr_des=None):
        self.__attr_des = RootAttributeDeserializer() if attr_des is None else attr_des
        if not isinstance(self.__attr_des, RootAttributeDeserializer):
            raise TypeError('attr_des should be of type RootAttributeDeserializer.')
    def deserialize(self, line_analizer):
        return RootNode(line_analizer.RootName, attr=self.__attr_des.deserialize(line_analizer.RootAttr))
class RootSerializer(object):
    """Convert a line of tree text to Node."""
    def __init__(self, attr_ser=None, indent=TexTree.INDENT):
        self.__attr_ser = RootAttributeSerializer() if attr_ser is None else attr_ser
        if not isinstance(self.__attr_ser, RootAttributeSerializer):
            raise TypeError('attr_ser should be of type RootAttributeSerializer.')
        self.__indent = indent if isinstance(indent, str) and 0 < len(indent) else TexTree.INDENT
    @property
    def Indent(self): return self.__indent
    @property
    def AttrSerializer(self): return self.__attr_ser
    def serialize(self, node):
        return node.Name + ('' if node.Attr is None else self.Indent + self.__attr_ser.serialize(node.Attr))

class NodeDeserializer(object):
    """Convert a Node to a line of tree text."""
    def __init__(self, attr_des=None):
        self.__attr_des = NodeAttributeDeserializer() if attr_des is None else attr_des
        if not isinstance(self.__attr_des, NodeAttributeDeserializer):
            raise TypeError('attr_des should be of type NodeAttributeDeserializer.')
    def deserialize(self, line_analizer, parent, parents=None):
        return Node(line_analizer.Line, name=line_analizer.Name, parent=parent, attr=self.__attr_des.deserialize(line_analizer.Attr))
class NodeSerializer(object):
    """Convert a line of tree text to Node."""
    def __init__(self, attr_ser=None, indent=TexTree.INDENT):
        self.__attr_ser = NodeAttributeSerializer() if attr_ser is None else attr_ser
        if not isinstance(self.__attr_ser, NodeAttributeSerializer):
            raise TypeError('attr_ser should be of type NodeAttributeSerializer.')
        self.__indent = indent if isinstance(indent, str) and 0 < len(indent) else TexTree.INDENT
    @property
    def Indent(self): return self.__indent
    @property
    def AttrSerializer(self): return self.__attr_ser
    def serialize(self, node, parents=None):
        indent_level = len(parents)
        indent_str = '' if 0 == len(parents) else self.Indent * indent_level
        return indent_str + node.Name + ('' if node.Attr is None else self.Indent + self.__attr_ser.serialize(node.Attr))

import shlex, argparse
from collections import OrderedDict
class RootAttributeDeserializer(object):
    def deserialize(self, line_attr): return line_attr

import pipes
class RootAttributeSerializer(object):
    def serialize(self, attr): return attr

import shlex, argparse
from collections import OrderedDict
class NodeAttributeDeserializer(object):
    def deserialize(self, line_attr): return line_attr

import pipes
class NodeAttributeSerializer(object):
    def serialize(self, attr): return attr

