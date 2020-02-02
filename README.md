[ja](./README.ja.md)

# TexTree

Create nodes as specified in the tree text.

![demo](doc/demo/demo.svg)

# Features

* Compatible with python2,3
* Data can be assigned to nodes
* Convert between text and node objects

# Requirement

* <time datetime="2019-12-26T10:00:00+0900">2019-12-26</time>
* [Raspbierry Pi](https://ja.wikipedia.org/wiki/Raspberry_Pi) 4 Model B Rev 1.2
* [Raspbian](https://ja.wikipedia.org/wiki/Raspbian) buster 10.0 2019-09-26 <small>[setup](http://ytyaru.hatenablog.com/entry/2019/12/25/222222)</small>
* bash 5.0.3(1)-release
* Python 2.7.16
* Python 3.7.3

# Installation

```sh
pip install textree
```

# Usage

## Foundations

Convert from text to node object.

```python
import textree
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
    print(node.Line)
print(tree.to_text())
```

## Reference

Convert between text and objects.

```python
root = tree.to_node(tree_text)
       tree.to_text()
```

Reference and assignment.

```python
node.Name
node.Parent
node.Children
```
```python
node.Name = 'NewName'
node.Parent = Node('Parent')
node.Children.append(Node('Child'))
```

Move.

```python
node.to_first()
node.to_last()
node.to_next()
node.to_prev()
```

Get.

```python
Node.Path.select(root, 'A/A1/A11')
Node.Path.select(A, 'A1/A11')
```

Insertion / deletion.

```python
node.insert_first(Node('new'))
node.insert_last(Node('new'))
node.insert_next(Node('new'))
node.insert_prev(Node('new'))
```
```python
node.delete()
```

Update.

```python
node = Node.Path.select(root, 'A/A1/A11')
node.Name = 'UpdateName'
```

There are many others. Refer to the [code](./textree/py3/textree.py) or [API list](./doc/memo/apis_py3.txt) for details.

## Attribute of Node

Attributes can be assigned to the same line.

```python
import textree
tree_text = """
A	attrA
	A1	attrA1
		A11	attrA11
			A111	attrA111
			A112	attrA112
	A2	attrA2
B	attrB
"""
tree = TexTree()
root = tree.to_node(tree_text)
print(root, root.Name)
for node in tree.Nodes:
    print(node.Name, node,Attr)
```

### Attribute of RootNode

Attributes can be assigned to RootNode.

```python
import textree
tree_text = """
<ROOT>	root_attr
A	attrA
	A1	attrA1
		A11	attrA11
			A111	attrA111
			A112	attrA112
	A2	attrA2
B	attrB
"""
tree = TexTree()
root = tree.to_node(tree_text)
print(root, root.Name, root.Attr)
for node in tree.Nodes:
    print(node.Name, node,Attr)
```

### Serialization / Deserialization

The user can embed the attribute analysis code freely. Of course you can also write code to serialize to text.

The following code gives the node `my_name`.

```python
class MyNodeDeserializer(NodeDeserializer):
    def deserialize(self, ana, parent, parents=Node):
        node = Node(ana.Line, parent=parent)
        node.my_name = 'My name is ' + node.Name
        return node
```
```python
tree = TexTree(node_deserializer=MyNodeDeserializer())
root = tree.to_node(tree_text)
for node in tree.Nodes:
    print(node.my_name)
```
```python
class MyNodeAttributeSerializer(NodeAttributeSerializer):
    def serialize(self, attr): return 'my_name=' + attr
```
```python
tree = TexTree(node_deserializer=MyNodeDeserializer(), node_serializer=NodeSerializer(MyNodeAttributeSerializer()))
root = tree.to_node(tree_text)
for node in tree.Nodes:
    print(node.my_name)
print(tree.to_text())
```

#### Complex conversion

##### JSON style

tree_text
```
<ROOT>	{"height": 444, "name": " \\" NAME \\" "}
A
```
a.py
```python
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

tree = TexTree(root_deserializer=textree.RootDeserializer(MyRootAttributeDeserializer()), root_serializer=textree.RootSerializer(MyRootAttributeSerializer()))
tree_text = '<ROOT>\t{"height": 444, "name": " \\" NAME \\" "}\nA'
root = tree.to_node(tree_text)
self.assertEqual(640, root.Attr['width'])
self.assertEqual(444, root.Attr['height'])
self.assertEqual(' " NAME " ', root.Attr['name'])
```

##### Assignment style

tree_text
```
<ROOT>	height=444 name=" \" NAME \" "
A
```
b.py
```python
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
        attr_str = json.dumps(attr, False, True, True, True, None, None, (' ','='), "utf-8", None, False)
        attr_str = delete_key_quotes(delete_braces(attr_str))
        attr_str = attr_str.replace('width=640', '')
        attr_str = attr_str.replace('height=480', '')
        attr_str = attr_str.replace('name="new.xcf"', '')
        return None if attr_str is None else attr_str.strip()

tree = TexTree(root_deserializer=textree.RootDeserializer(attr_des=MyRootAttributeDeserializer()), root_serializer=textree.RootSerializer(attr_ser=MyRootAttributeSerializer()))
tree_text = '<ROOT>\theight=444 name=" \\" NAME \\" "\nA'
root = tree.to_node(tree_text)
self.assertEqual(640, root.Attr['width'])
self.assertEqual(444, root.Attr['height'])
self.assertEqual(' " NAME " ', root.Attr['name'])
self.assertEqual(tree_text, tree.to_text())
```

# Note

* Alpha version. Checking installation

# Author

　ytyaru

* [![github](http://www.google.com/s2/favicons?domain=github.com)](https://github.com/ytyaru "github")
* [![hatena](http://www.google.com/s2/favicons?domain=www.hatena.ne.jp)](http://ytyaru.hatenablog.com/ytyaru "hatena")
* [![mastodon](http://www.google.com/s2/favicons?domain=mstdn.jp)](https://mstdn.jp/web/accounts/233143 "mastdon")

# License

This software is [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html) licensed. (GNU Affero General Public License v3) `agpl-3.0`

[![agpl-3.0](./doc/res/AGPLv3.svg "agpl-3.0")](https://www.gnu.org/licenses/agpl-3.0.en.html)

