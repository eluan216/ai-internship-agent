from cli import main


def test_cli_demo_exits_zero(capsys):
    code = main(["--demo", "-k", "internship", "-n", "3"])
    assert code == 0
    out = capsys.readouterr().out
    assert "Internship shortlist" in out


def test_cli_writes_output_file(tmp_path):
    out = tmp_path / "shortlist.md"
    code = main(["--demo", "-k", "ml", "internship", "-n", "3", "-o", str(out)])
    assert code == 0
    assert out.exists()
    assert "Internship shortlist" in out.read_text(encoding="utf-8")
