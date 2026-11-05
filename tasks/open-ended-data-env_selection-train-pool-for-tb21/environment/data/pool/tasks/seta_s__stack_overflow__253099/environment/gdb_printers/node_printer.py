import gdb
import gdb.printing

class NodePrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        node_id = self.val['id']
        name = self.val['name']
        if node_id >= 0
            return "Node(id={}, name={})".format(node_id, name)
        else:
            return "Node(invalid)"

def build_pretty_printer():
    pp = gdb.printing.RegexpCollectionPrettyPrinter("treestats")
    pp.add_printer('Node', '^Node$', NodePrinter)
    return pp

gdb.printing.register_pretty_printer(gdb.current_objfile(), build_pretty_printer())
