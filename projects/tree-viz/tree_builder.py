import os
from tree_node import TreeNode

def build_tree(path: str) -> TreeNode:
    """
    Build a tree structure from a file system path.
    
    Args:
        path: Path to file or directory
        
    Returns:
        TreeNode representing the file system structure
        
    Raises:
        FileNotFoundError: If path doesn't exist
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} directory/file does not exist.")
    
    # case where input path is a single file
    if not os.path.isdir(path):
        return TreeNode(os.path.basename(path), True)
    else:
        root = TreeNode(os.path.basename(path))

        for object in os.listdir(path):
            full_path = os.path.join(path, object)

            if os.path.isdir(full_path):
                root.add_child(build_tree(full_path))
            else:
                root.add_child(TreeNode(os.path.basename(full_path), True))

    return root

if __name__ == '__main__':
    print(build_tree('../../projects'))