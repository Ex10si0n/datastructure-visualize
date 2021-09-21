import webbrowser
import os

def Singleton(cls):
    _instance = {}
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton


@Singleton
class Mermaid(object):
    def __init__(self, builder):
        self.builder = builder
        self.pattern = builder.pattern
        self.js = '<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>\n<script>mermaid.initialize({startOnLoad:true});</script>'
        self.html = "<div class='mermaid'>%s</div>"

    def expandPattern(self, pattern):
        self.pattern += pattern

    def getHtml(self):
        return self.html % self.pattern + self.js




class GraphBuilder(object):
    def __init__(self, theme='stadium', direction='TD'):
        self.theme = theme
        self.direction = direction
        self.open = '('
        self.close = ')'
        self.pattern = 'graph ' + direction + '\n'
        if theme == 'round': self.open = '(('; self.close = '))';
        if theme == 'stadium': self.open = '(['; self.close = '])';
        if theme == 'square': self.open = '['; self.close = ']';

    def buildConnection(self, ins, fromNode, toNode, valueAttr):
        f = str(fromNode.__getattribute__(valueAttr))
        t = str(toNode.__getattribute__(valueAttr))
        ins.mermaid.expandPattern(f + self.open + f + self.close + '-->' + t + self.open + t + self.close + '\n')




class Structure(object):
    def __init__(self, prototype):
        self.prototype = prototype
        self.type = prototype.__class__.__name__
        self.attributes = prototype.__dict__.items()
        self.builder = GraphBuilder()
        self.mermaid = Mermaid(self.builder)

    def getGraphBuilder(self):
        return self.builder

    def log(self):
        logging = '''printing Structure.log\nprototype class: %s\nprototype attributes: %s''' % (\
            self.type,
            self.attributes
        )
        print(logging)

    def print(self):
        self.visualize()
        f = open('index.html', 'w')
        f.write(self.mermaid.getHtml())
        f.close()
        print(self.mermaid.getHtml())
        fileName = 'file:///'+os.getcwd()+'/' + 'index.html'
        webbrowser.open_new_tab(fileName)


    def visualize(self):
        toNode = []
        thisValue = []
        valueAttribute = None
        for attr in self.attributes:
            if type(attr[1]) == type(self.prototype):
                # BUG?
                toNode.append(attr[1])
            else:
                thisValue.append(attr[1])
                valueAttribute = attr[0]
        for node in toNode:
            self.builder.buildConnection(self, self.prototype, node, valueAttribute)
            nextNode = Structure(node)
            nextNode.visualize()



class Node:
    def __init__(self, val, lch=None, rch=None):
        self.val = val
        self.lch = lch
        self.rch = rch


if __name__ == "__main__":
    root = Node(1, Node(2, Node(3), Node(4)), Node(5, Node(6, Node(8), Node(9)), Node(7)))
    tree = Structure(root)
    tree.print()
    # tree.log()
