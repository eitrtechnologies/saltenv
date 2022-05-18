from pathlib import Path


async def test_unit_uninstall_empty_local_versions(mock_hub, hub, capfd):
    """
    SCENARIO #1:
    - No local versions
    - Salt version is irrelevant
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.cli.uninstall = hub.saltenv.cli.uninstall

    # Mock the fill functions to do nothing to do nothing
    mock_hub.saltenv.ops.fill_local_version_list.return_value = None
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = None

    # Set the LOCAL_VERSIONS dict to be {}
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {}

    # Mock the salt_version
    mock_hub.OPT.saltenv.salt_version = "3004"

    # Call install
    await mock_hub.saltenv.cli.uninstall()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{mock_hub.OPT.saltenv.salt_version} is already uninstalled.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.saltenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.saltenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.saltenv.ops.remove_version.called


async def test_unit_uninstall_matching_salt_version(mock_hub, hub, capfd, tmp_path):
    """
    SCENARIO #2:
    - Local versions
    - Matching salt version
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.cli.uninstall = hub.saltenv.cli.uninstall

    # Mock the fill functions to do nothing to do nothing
    mock_hub.saltenv.ops.fill_local_version_list.return_value = None
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = None

    # Set the LOCAL_VERSIONS dict to contain data
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {
        "3001": Path(tmp_path / "salt-3001"),
        "3004": Path(tmp_path / "salt-3004"),
    }

    # Mock the salt_version
    mock_hub.OPT.saltenv.salt_version = "3004"

    # Mock remove_version to do nothing
    mock_hub.saltenv.ops.remove_version.return_value = None

    # Call install
    await mock_hub.saltenv.cli.uninstall()

    # Check that there was not output printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = ""
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.saltenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.saltenv.ops.fill_local_version_list.assert_called_once()
    mock_hub.saltenv.ops.remove_version.assert_called_once()


async def test_unit_uninstall_nonmatching_salt_version(mock_hub, hub, capfd, tmp_path):
    """
    SCENARIO #3:
    - Local versions
    - Nonmatching salt version
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.cli.uninstall = hub.saltenv.cli.uninstall

    # Mock the fill functions to do nothing to do nothing
    mock_hub.saltenv.ops.fill_local_version_list.return_value = None
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = None

    # Set the LOCAL_VERSIONS dict to contain data
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {
        "3001": Path(tmp_path / "salt-3001"),
        "3004": Path(tmp_path / "salt-3004"),
    }

    # Mock the salt_version
    mock_hub.OPT.saltenv.salt_version = "3003"

    # Mock remove_version to do nothing
    mock_hub.saltenv.ops.remove_version.return_value = None

    # Call install
    await mock_hub.saltenv.cli.uninstall()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{mock_hub.OPT.saltenv.salt_version} is already uninstalled.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.saltenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.saltenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.saltenv.ops.remove_version.called
