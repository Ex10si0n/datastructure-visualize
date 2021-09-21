# Data Structure Visualization

script name: `visualize.py`

## Usage

in your Python code

```python
from visualize import *

'''
some data structres classes
defined in recursive way

such as:
	+ class Node(value, left_child, right_child):
	+     def __init__(value, left_child=None, right_child=None):
	+	      # constructor

then in your main method:
	+ if __name__ == '__main__':
	+     Node('root', Node('left_child'), Node('right_child'))
'''

Structure(root).print()
```

the Browser will open a new tab to visualize the tree by `root`

![](demo.gif)
