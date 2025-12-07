from tree_node import TreeNode
from tree_builder import build_tree

def render_tree(node: TreeNode, prefix: str = "", is_last: bool = True) -> str:
    """
    Render a tree structure with ASCII art.
    
    Args:
        node: The TreeNode to render
        prefix: Current line prefix (for indentation/continuation)
        is_last: Whether this node is the last child of its parent
        
    Returns:
        String representation of the tree with box-drawing characters
    """
    render_str = ""

    suffix = "/" if not node.is_file else ""
    
    if prefix == "":
        current_line = node.name + suffix + "\n"
    else:
        connector = "└── " if is_last else "├── "
        current_line = prefix + connector + node.name + suffix + "\n"
    
    render_str += current_line

    child_prefix = prefix + "    " if is_last else prefix + "│   "

    for i, child in enumerate(node.children):
        is_last_child = (i == len(node.children) - 1)
        render_str += render_tree(child, child_prefix, is_last_child)

    return render_str

if __name__ == '__main__':
    print(render_tree(build_tree('../../projects')))