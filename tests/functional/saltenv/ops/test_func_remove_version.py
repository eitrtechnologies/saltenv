from pathlib import Path


async def test_func_remove_version_exists(mock_hub, hub, tmp_path):
    """
    SCENARIO #1:
    - The version exists within LOCAL_VERSIONS
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.remove_version = hub.saltenv.ops.remove_version

    # Create the new valid versions to include in LOCAL_VERSIONS
    mocked_versions_dir = tmp_path / "versions"
    mocked_versions_dir.mkdir()
    valid_path_3001 = mocked_versions_dir / "salt-3001"
    valid_path_3001.write_text("valid")
    valid_path_3004 = mocked_versions_dir / "salt-3004"
    valid_path_3004.write_text("valid")

    # Add the two valid versions to LOCAL_VERSIONS
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {
        "3001": Path(valid_path_3001),
        "3004": Path(valid_path_3004),
    }

    # Set the expected LOCAL_VERSIONS value after remove_version is called.
    # This needs to be created before remove_version because otherwise
    # the Path object creation would fail due to the file having been deleted.
    expected_local_versions = {
        "3001": Path(valid_path_3001),
        "3004": Path(valid_path_3004),
    }

    # Call remove_version with a version that is present in LOCAL_VERSIONS
    ret = await mock_hub.saltenv.ops.remove_version("3004")
    assert ret == True

    # Confirm that the specified version had its file removed
    assert valid_path_3004.exists() == False

    # Confirm that the LOCAL_VERSIONS list is unchanged.
    assert expected_local_versions == mock_hub.saltenv.ops.LOCAL_VERSIONS


async def test_func_remove_version_does_not_exist(mock_hub, hub, tmp_path):
    """
    SCENARIO #2:
    - The version does not exist within LOCAL_VERSIONS
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.remove_version = hub.saltenv.ops.remove_version

    # Create the new valid versions to include in LOCAL_VERSIONS
    mocked_versions_dir = tmp_path / "versions"
    mocked_versions_dir.mkdir()
    valid_path_3001 = mocked_versions_dir / "salt-3001"
    valid_path_3001.write_text("valid")
    valid_path_3004 = mocked_versions_dir / "salt-3004"
    valid_path_3004.write_text("valid")

    # Add the two valid versions to LOCAL_VERSIONS
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {
        "3001": Path(valid_path_3001),
        "3004": Path(valid_path_3004),
    }

    # Set the expected LOCAL_VERSIONS value after remove_version is called.
    expected_local_versions = {
        "3001": Path(valid_path_3001),
        "3004": Path(valid_path_3004),
    }

    # Call remove_version with a version that is not present in LOCAL_VERSIONS
    ret = await mock_hub.saltenv.ops.remove_version("3003")
    assert ret == True

    # Confirm that the two valid version files still exist and were unaffected by
    # the remove_version call
    assert valid_path_3001.exists() == True
    assert valid_path_3004.exists() == True

    # Confirm that the LOCAL_VERSIONS list is unchanged.
    assert expected_local_versions == mock_hub.saltenv.ops.LOCAL_VERSIONS


async def test_func_remove_version_empty_local_versions(mock_hub, hub):
    """
    SCENARIO #3:
    - LOCAL_VERSIONS is empty
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.remove_version = hub.saltenv.ops.remove_version

    # Set LOCAL_VERSIONS as empty
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {}

    # Set the expected LOCAL_VERSIONS value after remove_version is called.
    expected_local_versions = {}

    # Call remove_version with a version that is not present in LOCAL_VERSIONS
    ret = await mock_hub.saltenv.ops.remove_version("3003")
    assert ret == True

    # Confirm that the LOCAL_VERSIONS list is unchanged.
    assert expected_local_versions == mock_hub.saltenv.ops.LOCAL_VERSIONS
