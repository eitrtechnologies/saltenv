from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path, PosixPath, PurePosixPath
import pathlib


async def test_unit_list_remote_empty(mock_hub, hub, capfd):
    """
    SCENARIO #1:
    - No remote versions
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.cli.list_remote = hub.saltenv.cli.list_remote

    # Mock fill_remote_version_list to do nothing
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = None

    # Set REMOTE_VERSIONS to be {}
    mock_hub.saltenv.ops.REMOTE_VERSIONS = {}

    # Call list_remote
    await mock_hub.saltenv.cli.list_remote()

    # Check that the expected list was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = "\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.saltenv.ops.fill_remote_version_list.assert_called_once()


async def test_unit_list_remote_nonempty(mock_hub, hub, tmp_path, capfd):
    """
    SCENARIO #2:
    - There are remote versions
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.cli.list_remote = hub.saltenv.cli.list_remote

    # Mock fill_remote_version_list to do nothing
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = None

    # Fill REMOTE_VERSIONS with two versions
    mock_hub.saltenv.ops.REMOTE_VERSIONS = {
        "3003.3": "3003.3-1",
        "3003": "3003",
        "3004": "3004-1",
        "3004rc1": "3004rc1-1",
        "latest": "latest",
    }

    # Call list_remote
    await mock_hub.saltenv.cli.list_remote()

    # Check that the expected list was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = "latest\n3004rc1\n3004\n3003.3\n3003\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.saltenv.ops.fill_remote_version_list.assert_called_once()
