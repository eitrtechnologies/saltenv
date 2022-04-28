from pathlib import Path
from unittest.mock import MagicMock


async def test_unit_install_empty_version_dicts(mock_hub, hub, capfd):
    """
    SCENARIO #1:
    - No local versions
    - No remote versions
    - Salt version is irrelevant
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.cli.install = hub.saltenv.cli.install

    # Mock the fill functions to do nothing to do nothing
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = None
    mock_hub.saltenv.ops.fill_local_version_list.return_value = None

    # Set the VERSIONS dicts to be {}
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {}
    mock_hub.saltenv.ops.REMOTE_VERSIONS = {}

    # Mock the salt_version
    mock_hub.OPT.saltenv.salt_version = "3004"

    # Call install
    await mock_hub.saltenv.cli.install()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"ERROR: {mock_hub.OPT.saltenv.salt_version} is not available as a binary.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.saltenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.saltenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.saltenv.ops.download_version.called


async def test_unit_install_nonempty_version_dicts_nonmatching_salt_version(
    mock_hub, hub, tmp_path, capfd
):
    """
    SCENARIO #2:
    - Local versions
    - Remote versions
    - Nonmatching salt version
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.cli.install = hub.saltenv.cli.install

    # Mock the fill functions to do nothing to do nothing
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = None
    mock_hub.saltenv.ops.fill_local_version_list.return_value = None

    # Set the VERSIONS dicts to contain data
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {
        "3001": Path(tmp_path / "salt-3001"),
        "3004": Path(tmp_path / "salt-3004"),
    }
    mock_hub.saltenv.ops.REMOTE_VERSIONS = {
        "3003.3": "3003.3-1",
        "3003": "3003",
        "3004": "3004-1",
        "3004rc1": "3004rc1-1",
        "latest": "latest",
    }

    # Mock the salt_version to not match any entries in the VERSIONS dicts
    mock_hub.OPT.saltenv.salt_version = "nonexistent"

    # Call install
    await mock_hub.saltenv.cli.install()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"ERROR: {mock_hub.OPT.saltenv.salt_version} is not available as a binary.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.saltenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.saltenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.saltenv.ops.download_version.called


async def test_unit_install_nonempty_local_empty_remote_matching_salt_version(
    mock_hub, hub, tmp_path, capfd
):
    """
    SCENARIO #3:
    - Local versions
    - No Remote versions
    - Matching salt version
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.cli.install = hub.saltenv.cli.install

    # Mock the fill functions to do nothing to do nothing
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = None
    mock_hub.saltenv.ops.fill_local_version_list.return_value = None

    # Set the LOCAL_VERSIONS dict to be nonempty
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {
        "3001": Path(tmp_path / "salt-3001"),
        "3004": Path(tmp_path / "salt-3004"),
    }
    # Set the REMOTE_VERSIONS dict to be empty
    mock_hub.saltenv.ops.REMOTE_VERSIONS = {}

    # Mock the salt_version to match an entry in the LOCAL_VERSIONS dict
    mock_hub.OPT.saltenv.salt_version = "3004"

    # Call install
    await mock_hub.saltenv.cli.install()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{mock_hub.OPT.saltenv.salt_version} is already installed.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.saltenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.saltenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.saltenv.ops.download_version.called


async def test_unit_install_empty_local_nonempty_remote_matching_salt_version(
    mock_hub, hub, tmp_path, capfd
):
    """
    SCENARIO #4:
    - No Local versions
    - Remote versions
    - Matching salt version
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.cli.install = hub.saltenv.cli.install

    # Mock the fill functions to do nothing to do nothing
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = None
    mock_hub.saltenv.ops.fill_local_version_list.return_value = None

    # Set the LOCAL_VERSIONS dict to be empty
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {}
    # Set the REMOTE_VERSIONS dict to be nonempty
    mock_hub.saltenv.ops.REMOTE_VERSIONS = {
        "3003.3": "3003.3-1",
        "3003": "3003",
        "3004": "3004-1",
        "3004rc1": "3004rc1-1",
        "latest": "latest",
    }

    # Mock the salt_version to match an entry in the REMOTE_VERSIONS dict
    mock_hub.OPT.saltenv.salt_version = "3004"

    # Mock download_version to not do anything
    mock_hub.saltenv.ops.download_version.return_value = MagicMock()

    # Call install
    await mock_hub.saltenv.cli.install()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = ""
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.saltenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.saltenv.ops.fill_local_version_list.assert_called_once()
    mock_hub.saltenv.ops.download_version.assert_called_once_with("3004")


async def test_unit_install_nonempty_local_nonempty_remote_matching_salt_version(
    mock_hub, hub, tmp_path, capfd
):
    """
    SCENARIO #5:
    - Local versions
    - Remote versions
    - Matching salt version
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.cli.install = hub.saltenv.cli.install

    # Mock the fill functions to do nothing to do nothing
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = None
    mock_hub.saltenv.ops.fill_local_version_list.return_value = None

    # Set the VERSION dicts to be nonempty
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {
        "3001": Path(tmp_path / "salt-3001"),
        "3004": Path(tmp_path / "salt-3004"),
    }
    mock_hub.saltenv.ops.REMOTE_VERSIONS = {
        "3003.3": "3003.3-1",
        "3003": "3003",
        "3004": "3004-1",
        "3004rc1": "3004rc1-1",
        "latest": "latest",
    }

    # Mock the salt_version to match an entry in both VERSION dicts
    mock_hub.OPT.saltenv.salt_version = "3004"

    # Mock download_version to not do anything (it should not be called, but just in case code is changed)
    mock_hub.saltenv.ops.download_version.return_value = MagicMock()

    # Call install
    await mock_hub.saltenv.cli.install()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{mock_hub.OPT.saltenv.salt_version} is already installed.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.saltenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.saltenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.saltenv.ops.download_version.called
