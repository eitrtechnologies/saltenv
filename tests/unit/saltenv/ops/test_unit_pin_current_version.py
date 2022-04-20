from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path, PosixPath, PurePosixPath
import pathlib
import aiofiles
from aiofiles import threadpool


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
    with patch("os.getcwd") as mock_override_dir:
        # Set up the mock_override_file
        mock_override_dir.return_value = tmp_path

        # Confirm the return is False
        expected = False
        actual = await mock_hub.saltenv.ops.pin_current_version()
        actual == expected

        # Ensure every mocked function was called the appropriate number of times
        mock_override_dir.assert_called_once()


async def test_unit_pin_current_version_active_version(mock_hub, hub, tmp_path):
    """
    SCENARIO #2:
    - There is an active version
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
    with patch("os.getcwd") as mock_override_dir:
        # Set up the mock_override_file
        mock_override_dir.return_value = tmp_path

        # Register the return type with aiofiles.threadpool.wrap dispatcher
        aiofiles.threadpool.wrap.register(MagicMock)(
            lambda *args, **kwargs: threadpool.AsyncBufferedIOBase(*args, **kwargs)
        )

        # Mock the file returned by aiofiles.open
        mock_version_file = MagicMock()
        with patch("aiofiles.threadpool.sync_open", return_value=mock_version_file) as mock_open:
            mock_version_file.write.side_effect = None

            # Confirm the return is True
            expected = True
            actual = await mock_hub.saltenv.ops.pin_current_version()
            assert actual == expected

            # Ensure every mocked function was called the appropriate number of times
            mock_override_dir.assert_called_once()
            mock_open.assert_called_once()
            mock_version_file.write.assert_called_once()
