import pytest
from pathlib import Path
from tree_builder import build_tree

def test_single_file(tmp_path):
    """Test building a tree from a single file"""
    file = tmp_path / "file.txt"
    file.write_text('content')
    tree = build_tree(str(file))

    assert tree.name == "file.txt"
    assert tree.is_file == True
    assert len(tree.children) == 0
    assert len(tree) == 1

def test_empty_directory(tmp_path):
    """Test building a tree from a single, empty directory"""
    my_dir = tmp_path / "my_dir"
    my_dir.mkdir()
    tree = build_tree(my_dir)

    assert tree.name == "my_dir"
    assert tree.is_file == False
    assert len(tree.children) == 0
    assert len(tree) == 1

def test_flat_directory(tmp_path):
    """Test building a tree for a directory with only files as children"""
    (tmp_path / "file1.txt").touch()
    (tmp_path / "file2.py").touch()
    (tmp_path / "file3.md").touch()

    tree = build_tree(str(tmp_path))

    assert len(tree.children) == 3
    assert len(tree) == 4

    child_names = {child.name for child in tree.children}
    assert child_names == {"file1.txt", "file2.py", "file3.md"}
    assert all(child.is_file for child in tree.children)

def test_nested_structure(tmp_path):
    """Test directory with nested sub-directories"""
    (tmp_path / "file1.txt").touch()

    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file2.txt").touch()

    nested = subdir / "nested"
    nested.mkdir()
    (nested / "file3.txt").touch()

    tree = build_tree(str(tmp_path))

    assert len(tree) == 6
    assert len(tree.children) == 2

    subdir_node = [c for c in tree.children if c.name == "subdir"][0]

    assert subdir_node.is_file == False
    assert len(subdir_node.children) == 2

def test_mixed_files_and_dirs(tmp_path):
    """Test directory with both files and sub-directory children"""
    (tmp_path / "file.py").touch()

    src_dir = tmp_path / 'src'
    src_dir.mkdir()
    (src_dir / "main.py").touch()

    test_dir = tmp_path / 'test'
    test_dir.mkdir()
    (test_dir / "test.py").touch()

    tree = build_tree(str(tmp_path))

    assert len(tree.children) == 3
    assert len(tree) == 6

    files = [c for c in tree.children if c.is_file]
    dirs = [c for c in tree.children if not c.is_file]

    assert len(files) == 1
    assert len(dirs) == 2

def test_file_not_found():
    """Test graceful error for building a tree for a file that doesn't exist"""
    with pytest.raises(FileNotFoundError):
        build_tree('/fake/path.txt')

def test_node_names_are_basenames(tmp_path):
    """Test that node names are basenames, not full file path"""
    test_file = tmp_path / "dir1" / "dir2" / "dir3" / "test.txt"
    test_file.parent.mkdir(parents=True)
    test_file.touch()

    tree = build_tree(test_file)

    assert tree.name == "test.txt"
    assert "/" not in tree.name
    assert "\\" not in tree.name

def test_hidden_files_included(tmp_path):
    """Test that hidden files are included in tree building"""
    (tmp_path / ".hidden_file").touch()
    (tmp_path / "normal_file.txt").touch()

    hidden_dir = tmp_path / ".hidden_dir"
    hidden_dir.mkdir()

    tree = build_tree(str(tmp_path))

    assert len(tree) == 4
    assert len(tree.children) == 3

    child_names = {c.name for c in tree.children}
    assert ".hidden_dir" in child_names
    assert ".hidden_file" in child_names

def test_large_directory(tmp_path):
    """Test building a tree for a directory with many files"""
    for i in range(50):
        (tmp_path / f"file_{i:03d}.txt").touch()
    
    tree = build_tree(str(tmp_path))
    
    assert len(tree) == 51
    assert len(tree.children) == 50

def test_deep_nesting(tmp_path):
    """Test deeply nested file structure"""
    deep_file = tmp_path / "a" / "b" / "c" / "d" / "e" / "f" / "g" / "file.txt"
    deep_file.parent.mkdir(parents=True)
    deep_file.touch()

    tree = build_tree(str(tmp_path))

    assert len(tree) == 9
