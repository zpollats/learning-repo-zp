class TreeNode:
    """
    Represents a node in a file system - can be either a directory or a file.
    """
    def __init__(self, name: str, is_file: bool = False) -> None:
        self.name = name
        self.is_file = is_file
        self.children = []

    def add_child(self, child: 'TreeNode') -> None:
        """Add a child node to this node"""
        self.children.append(child)
    
    def is_leaf(self) -> bool:
        """Return True if node has no children nodes"""
        return len(self.children) == 0
    
    def __len__(self) -> int:
        """Return total number of nodes in subtree (including self)"""
        total = 1
        for child in self.children:
            total += len(child)
        return total

    def __repr__(self) -> str:
        """Return a string representation of the node"""
        return f"TreeNode(NAME={self.name}, IS_FILE={self.is_file}, CHILDREN={self.children})"