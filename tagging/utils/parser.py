from utils.counter import count_tab
from utils.topic_tree import Node


def parse_topic(file_path):
    """
    读取topics
    :param file_path: 文件路径
    :return:
    """
    node_stack = list()
    num_stack = list()
    num_stack.append(0)
    node_stack.append(Node('null'))
    with open(file_path) as f:
        for line in f.readlines():
            l = len(num_stack)
            line = line.lower()
            line = line.rstrip()
            count = count_tab(line)
            current_num = num_stack[-1]

            if count == current_num:
                num_stack.append(count)
                node_stack.append(Node(line.strip()))
            elif count > current_num:
                num_stack.append(count)
                node_stack.append(Node(line.strip()))
            elif count < current_num:
                for i in range(count, current_num, -1):
                    children = []
                    while num_stack[-1] == i:
                        num_stack = num_stack[:-1]
                        children.append(node_stack.pop())
                    node_stack[-1].children = children
                num_stack.append(count)
                node_stack.append(Node(line.strip()))
    num_temp = []
    node_temp = []

    while len(num_stack) > 0:
        if len(num_temp) == 0:
            num_temp.append(num_stack.pop())
            node_temp.append(node_stack.pop())
        else:
            num_top = num_stack[-1]
            merge_top = num_temp[-1]
            if num_top >= merge_top:
                num_temp.append(num_stack.pop())
                node_temp.append(node_stack.pop())
            else:
                children = []
                while len(num_temp) > 0 and num_top < num_temp[-1]:
                    num_temp.pop()
                    children.append(node_temp.pop())
                node_stack[-1].children.extend(children)
    return node_temp[0]
