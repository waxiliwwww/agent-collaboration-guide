import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "skills/agent-collaboration-guide/scripts/update_install.py"
spec = importlib.util.spec_from_file_location("skill_update", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InstallProtection(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.target = self.root / "target"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("public version 1")

    def test_update_changes_public_files_and_preserves_private_and_custom_files(self):
        (self.target / "local/history").mkdir(parents=True)
        private = self.target / "local/history/person.md"
        private.write_bytes(b"private\x00bytes")
        (self.target / "custom.md").write_text("local customization")
        module.update(self.source, self.target, True)
        (self.source / "SKILL.md").write_text("public version 2")
        module.update(self.source, self.target, True)
        self.assertEqual((self.target / "SKILL.md").read_text(), "public version 2")
        self.assertEqual(private.read_bytes(), b"private\x00bytes")
        self.assertEqual((self.target / "custom.md").read_text(), "local customization")

    def test_export_excludes_private_source_without_reading_linked_private_directory(self):
        outside = self.root / "private"
        outside.mkdir()
        (outside / "secret.md").write_text("must not export")
        (self.source / "local").symlink_to(outside, target_is_directory=True)
        module.update(self.source, self.target)
        self.assertFalse((self.target / "local").exists())
        self.assertEqual(sorted(p.name for p in self.target.iterdir()), ["SKILL.md"])

    def test_invalid_source_and_dry_run_do_not_modify_destination(self):
        with self.assertRaises(ValueError):
            module.update(self.root / "absent", self.target)
        module.update(self.source, self.target, True, True)
        self.assertFalse(self.target.exists())

    def test_public_destination_symlink_is_rejected_before_other_files_are_written(self):
        self.target.mkdir()
        outside = self.root / "protected"
        outside.write_text("keep")
        (self.target / "SKILL.md").symlink_to(outside)
        (self.source / "extra.md").write_text("new")
        with self.assertRaises(ValueError):
            module.update(self.source, self.target)
        self.assertEqual(outside.read_text(), "keep")
        self.assertFalse((self.target / "extra.md").exists())

    def test_existing_preference_entry_is_not_initialized_again(self):
        (self.target / "local").mkdir(parents=True)
        entry = self.target / "local/preferences.md"
        entry.write_text("confirmed preference")
        module.update(self.source, self.target, True)
        self.assertEqual(entry.read_text(), "confirmed preference")


    def test_symlinked_target_parent_is_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        parent = self.root / "linked"
        parent.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            module.update(self.source, parent / "install")
        self.assertFalse((outside / "install").exists())

    def test_missing_preference_is_not_initialized_through_private_directory_symlink(self):
        outside = self.root / "outside"
        outside.mkdir()
        self.target.mkdir()
        (self.target / "local").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            module.update(self.source, self.target, True)
        self.assertFalse((outside / "preferences.md").exists())
        self.assertFalse((self.target / "SKILL.md").exists())

    def test_dangling_private_entry_symlink_is_not_followed(self):
        (self.target / "local").mkdir(parents=True)
        outside = self.root / "must-not-create.md"
        (self.target / "local/preferences.md").symlink_to(outside)
        with self.assertRaises(ValueError):
            module.update(self.source, self.target, True)
        self.assertFalse(outside.exists())
        self.assertFalse((self.target / "SKILL.md").exists())


    def test_unreadable_public_directory_fails_before_writing_target(self):
        reference = self.source / "references"
        reference.mkdir()
        (reference / "required.md").write_text("required")
        actual_scandir = module.os.scandir
        def denied(path):
            if Path(path) == reference:
                raise PermissionError("public reference unavailable")
            return actual_scandir(path)
        with mock.patch.object(module.os, "scandir", side_effect=denied):
            with self.assertRaises(PermissionError):
                module.update(self.source, self.target)
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main()
