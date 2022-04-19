from pathlib import Path
import aiofiles
from unittest.mock import patch, MagicMock


async def test_unit_pin_current_version_no_active_version(mock_hub, hub, tmp_path):
    """
    SCENARIO #1:
    - There is no active version
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.pin_current_version = hub.saltenv.ops.pin_current_version

    # Mock the return of get_current_version to be ("",""), meaning that
    # there is no active version
    mock_hub.saltenv.ops.get_current_version.return_value = ("", "")

    # Check that pin_current_version return False AND
    # that the override_version_file version IS NOT CHANGED
    with patch("os.getcwd") as mocked_override_dir:
        # Set up the mocked_override_file
        mocked_override_dir.return_value = tmp_path

        # Confirm the return is False
        expected = False
        actual = await mock_hub.saltenv.ops.pin_current_version()
        actual == expected


async def test_unit_pin_current_version_active_version(mock_hub, hub, tmp_path):
    """
    SCENARIO #2:
    - There is an active version
    - The active version matches the version in the override file.
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.pin_current_version = hub.saltenv.ops.pin_current_version

    # Mock the return of get_current_version to be ("3004", tmp_path/version), where
    # tmp_path/version is the main version file. The main version file would have 3004 as its value.
    existing_override_version = "3004"
    mock_hub.saltenv.ops.get_current_version.return_value = (
        existing_override_version,
        str(tmp_path / "version"),
    )

    # Check that pin_current_version return True AND that the
    # override_version_file version IS NOT CHANGED
    with patch("os.getcwd") as mocked_override_dir:
        # Set up the mocked_override_file
        mocked_override_dir.return_value = tmp_path

        # Confirm the return is True
        expected = True
        actual = await mock_hub.saltenv.ops.pin_current_version()
        assert actual == expected
