from tree_node import TreeNode

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
    render_str = ''
    return render_str