from tree_node import TreeNode

def test_create_file_node():
    """Test creating a file node"""
    file_node = TreeNode('test.py', True)
    assert file_node.name == 'test.py'
    assert file_node.is_file == True
    assert file_node.children == []

def test_create_directory_node():
    """Test creating a directory node"""
    dir_node = TreeNode('dir')
    assert dir_node.name == 'dir'
    assert dir_node.is_file == False
    assert dir_node.children == []

def test_add_child():
    """Test adding a child node to parent node"""
    parent = TreeNode('parent')
    child = TreeNode('child.txt', True)

    parent.add_child(child)

    assert len(parent.children) == 1
    assert parent.children[0] == child
    assert parent.children[0].name == 'child.txt'

def test_add_multiple_children():
    """Test adding multiple children nodes to parent node"""
    parent = TreeNode('src')
    child1 = TreeNode('utils.py', True)
    child2 = TreeNode('main.py', True)

    parent.add_child(child1)
    parent.add_child(child2)

    assert len(parent.children) == 2
    assert child1 in parent.children
    assert child2 in parent.children

def test_is_leaf():
    """Test if a node is a leaf"""
    file_node = TreeNode('file.txt', True)
    assert file_node.is_leaf() == True

    empty_dir = TreeNode('empty_dir')
    assert empty_dir.is_leaf() == True

    parent = TreeNode('parent')
    parent.add_child(TreeNode('child.txt', True))
    assert parent.is_leaf() == False

def test_len_single_node():
    """Test the length of a leaf node"""
    single_node = TreeNode('single')
    assert len(single_node) == 1

def test_len_with_children():
    """Test the length of a parent node with child"""
    multi_node = TreeNode('multi')
    multi_node.add_child(TreeNode('child'))
    assert len(multi_node) == 2

def test_len_deep_tree():
    """Test the length of a parent node with multiple levels of children"""
    parent = TreeNode('parent_dir')
    child1 = TreeNode('child1_dir')
    child2 = TreeNode('child2_dir')

    parent.add_child(child1)
    parent.add_child(child2)

    gchild1 = TreeNode('gchild1.txt', True)
    gchild2 = TreeNode('gchild2.txt', True)

    child1.add_child(gchild1)
    child1.add_child(gchild2)

    assert len(parent) == 5
    assert len(child1) == 3
    assert len(child2) == 1
    assert len(gchild1) == 1