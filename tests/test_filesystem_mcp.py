from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from modules.filesystem_mcp.main import categorize_file, organize_directory


def test_categorize_file():
    assert categorize_file(Path("note.txt")) == "Documents"
    assert categorize_file(Path("image.JPG")) == "Images"
    assert categorize_file(Path("archive.unknown")) == "Other"


def test_organize_directory(tmp_path):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.jpg").write_text("img")
    (tmp_path / "bad*name.txt").write_text("x")
    (tmp_path / "bad?name.txt").write_text("y")

    moves = organize_directory(tmp_path, dry_run=False)

    assert (tmp_path / "Documents" / "a.txt").exists()
    assert (tmp_path / "Images" / "b.jpg").exists()
    assert (tmp_path / "Documents" / "bad_name.txt").read_text() == "x"
    assert (tmp_path / "Documents" / "bad_name_1.txt").read_text() == "y"
    expected = {
        tmp_path / "a.txt": tmp_path / "Documents" / "a.txt",
        tmp_path / "b.jpg": tmp_path / "Images" / "b.jpg",
        tmp_path / "bad*name.txt": tmp_path / "Documents" / "bad_name.txt",
        tmp_path / "bad?name.txt": tmp_path / "Documents" / "bad_name_1.txt",
    }
    assert moves == expected
