import ast

# Sample Python source code as a string
source_code = """
@my_decorator
class Dog(Animal):
    field = "str"

    def bark(self):
        return "Woof!"

    def __init__(self):
        self.name = 'Spike'
"""

# Parse the source code into an AST
tree = ast.parse(source_code)

# Extract the ClassDef node (it sits inside the top-level Module body)
class_node = tree.body[0]

if isinstance(class_node, ast.ClassDef):
    print(f"Class Name: {class_node.name}")
    print(f"Bases: {[b.id for b in class_node.bases if isinstance(b, ast.Name)]}")
    print(
        f"Decorators: {[d.id for d in class_node.decorator_list if isinstance(d, ast.Name)]}"
    )
    print(
        f"Body Functions: {[node.name for node in class_node.body if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef))]}"
    )
    print(
        f"Body Variables?: {[node.targets[0].id for node in class_node.body if isinstance(node, (ast.Assign, ast.AnnAssign))]}"
    )
