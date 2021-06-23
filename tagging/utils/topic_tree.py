
class Node(object):

    def __init__(self, topic):
        self._topic = topic
        self._children = []
        self._count = 0
        self._sum = 0
        self.title = 0
        self.abstract = 0
        self.text = 0

    @property
    def topic(self):
        return self._topic

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        self._count = count

    @property
    def sum(self):
        return self._sum

    @sum.setter
    def sum(self, sum):
        self._sum = sum

    def add_child(self, child):
        self._children.append(child)


def bfs(root: Node):
    queue = list()
    queue.append(root)
    while len(queue) > 0:
        node = queue[0]
        print(node.topic, node.count, node.sum)
        queue = queue[1:]
        for child in node.children:
            queue.append(child)


def clear_data(node: Node):
    node.count = 0
    node.sum = 0
    node.text = 0
    node.abstract = 0
    node.text = 0
    for child in node.children:
        clear_data(child)
