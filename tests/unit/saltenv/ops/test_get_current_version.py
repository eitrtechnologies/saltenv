from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path, PosixPath, PurePosixPath
import pathlib
import aiofiles
from aiofiles import threadpool
import os


async def test_get_current_version_both_files_dont_exist(mock_hub, hub):
    """
    SCENARIO #1
    - override_version_file DOES NOT EXIST
    - main_version_file DOES NOT EXIST
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.get_current_version = hub.saltenv.ops.get_current_version

    # Set the saltenv_dir as a nonexistent directory
    mock_hub.OPT.saltenv.saltenv_dir = "nonexistent_testing_dir"

    # Patch the exists function to return False for both times it is called
    with patch("pathlib.PosixPath.exists", side_effect=[False, False]) as mock_exists:
        expected = ("", "")
        actual = await mock_hub.saltenv.ops.get_current_version()
        actual == expected
        
        # Ensure every mocked function was called the appropriate number of times
        assert mock_exists.call_count == 2


async def test_get_current_version_only_override_exists(mock_hub, hub, tmp_path):
    """
    SCENARIO #2
    - override_version_file DOES EXIST
    - main_version_file DOES NOT EXIST
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.get_current_version = hub.saltenv.ops.get_current_version

    # Set the saltenv_dir as a nonexistent directory
    mock_hub.OPT.saltenv.saltenv_dir = "nonexistent_testing_dir"

    # Patch os.getcwd() to be the mock directory
    with patch("os.getcwd", return_value=tmp_path) as mock_cwd:
        # Patch exists to return True the first call and False the second call
        with patch("pathlib.PosixPath.exists", side_effect=[True, False]) as mock_exists:
            
            # Register the return type with aiofiles.threadpool.wrap dispatcher
            aiofiles.threadpool.wrap.register(MagicMock)(lambda *args, **kwargs: threadpool.AsyncBufferedIOBase(*args, **kwargs))

            # Mock the file returned by aiofiles.open
            mock_override_version = "3004"
            mock_file = MagicMock()
            with patch('aiofiles.threadpool.sync_open', return_value=mock_file) as mock_open:
                # Set the value of read() to be the mock version
                mock_file.read.return_value = mock_override_version
                # Call get_current_version
                expected = (mock_override_version, tmp_path / ".salt-version")
                actual = await mock_hub.saltenv.ops.get_current_version()
                actual == expected

                # Ensure every mocked function was called the appropriate number of times
                mock_cwd.assert_called_once()
                mock_exists.assert_called_once()
                mock_open.assert_called_once()
                mock_file.read.assert_called_once()


async def test_get_current_version_only_main_exists(mock_hub, hub, tmp_path):
    """
    SCENARIO #3
    - override_version_file DOES NOT EXIST
    - main_version_file DOES EXIST
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.get_current_version = hub.saltenv.ops.get_current_version

    # Set the saltenv_dir as the mock directory
    mock_hub.OPT.saltenv.saltenv_dir = tmp_path

    # Patch os.getcwd() to be the nonexistent directory
    with patch("os.getcwd", return_value="nonexistent_testing_dir") as mock_cwd:
        # Patch exists to return False the first call and True the second call
        with patch("pathlib.PosixPath.exists", side_effect=[False, True]) as mock_exists:

            # Register the return type with aiofiles.threadpool.wrap dispatcher
            aiofiles.threadpool.wrap.register(MagicMock)(lambda *args, **kwargs: threadpool.AsyncBufferedIOBase(*args, **kwargs))

            # Mock the file returned by aiofiles.open
            mock_main_version = "3003"
            mock_file = MagicMock()
            with patch('aiofiles.threadpool.sync_open', return_value=mock_file) as mock_open:
                # Set the value of read() to be the mock version
                mock_file.read.return_value = mock_main_version
                # Call get_current_version
                expected = (mock_main_version, tmp_path / "version")
                actual = await mock_hub.saltenv.ops.get_current_version()
                actual == expected

                # Ensure every mocked function was called the appropriate number of times
                mock_cwd.assert_called_once()
                assert mock_exists.call_count == 2
                mock_open.assert_called_once()
                mock_file.read.assert_called_once()


async def test_get_current_version_both_files_exist(mock_hub, hub, tmp_path):
    """
    SCENARIO #4
    - override_version_file DOES EXIST
    - main_version_file DOES EXIST
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.get_current_version = hub.saltenv.ops.get_current_version

    # Set the saltenv_dir as the mock directory
    mock_hub.OPT.saltenv.saltenv_dir = tmp_path

    # Patch os.getcwd() to be the mock directory
    with patch("os.getcwd", return_value=tmp_path) as mock_cwd:
        # Patch exists to return True for both calls
        with patch("pathlib.PosixPath.exists", side_effect=[True, True]) as mock_exists:

            # Register the return type with aiofiles.threadpool.wrap dispatcher
            aiofiles.threadpool.wrap.register(MagicMock)(lambda *args, **kwargs: threadpool.AsyncBufferedIOBase(*args, **kwargs))

            # Mock the file returned by aiofiles.open
            mock_override_version = "3004"
            mock_override_file = MagicMock()
            # Set the value of read() to "3004"
            mock_override_file.read.return_value = mock_override_version
            mock_main_version = "3003"
            mock_main_file = MagicMock()
            # Set the value of read() to "3003"
            mock_main_file.read.return_value = mock_main_file
            # Set the open() to return the mocked file for override and then the mocked file for main
            with patch('aiofiles.threadpool.sync_open', side_effect=[mock_override_file, mock_main_file]) as mock_open:
                # Call get_current_version
                expected = (mock_override_version, tmp_path / ".salt-version")
                actual = await mock_hub.saltenv.ops.get_current_version()
                actual == expected

                # Ensure every mocked function was called the appropriate number of times
                mock_cwd.assert_called_once()
                mock_exists.assert_called_once()
                mock_open.assert_called_once()
                mock_override_file.read.assert_called_once()
                assert mock_main_file.read.call_count == 0
