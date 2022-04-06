import mock
from pathlib import Path, PosixPath


async def test_local_version_list_nonexistent_dir(mock_hub, hub):
    # Link the real function to the mock_hub
    mock_hub.saltenv.ops.local_version_list = hub.saltenv.ops.local_version_list
    mock_hub.OPT.saltenv.saltenv_dir = "nonexistent_testing_dir"
    actual = await mock_hub.saltenv.ops.local_version_list()
    expected = {}
    assert expected == actual


async def test_local_version_list_existent_dir(mock_hub, hub, tmp_path):
    # Link the real function to the mock_hub    
    mock_hub.saltenv.ops.local_version_list = hub.saltenv.ops.local_version_list
    mock_hub.OPT.saltenv.saltenv_dir = tmp_path
    
    # Create the mocked version dir to insert files in for testing
    mocked_versions_dir = tmp_path / "versions"
    mocked_versions_dir.mkdir()

    # Confirm that the return dictionary is empty if the directory does not contain any version files
    expected = {}
    actual = await mock_hub.saltenv.ops.local_version_list()
    assert actual == expected

    # Confirm that the return directory is correct when the directory contains valid and invalid version files
    # Create valid version files that will get picked up by the function 
    valid_name_1 = "salt-3001"
    valid_path_1 = mocked_versions_dir / valid_name_1
    valid_path_1.write_text("valid")

    valid_name_2 = "salt-214"
    valid_path_2 = mocked_versions_dir / valid_name_2
    valid_path_2.write_text("valid")

    # Create invalid version files that will get picked up by the function
    invalid_name_1 = "salt3002"
    invalid_path_1 = mocked_versions_dir / invalid_name_1
    invalid_path_1.write_text("invalid")

    invalid_name_2 = "slt-3003"
    invalid_path_2 = mocked_versions_dir / invalid_name_2
    invalid_path_2.write_text("invalid")

    invalid_name_3 = "rand0m"
    invalid_path_3 = mocked_versions_dir / invalid_name_3
    invalid_path_3.write_text("invalid")

    # Compare the actual and expected results
    expected = {valid_name_1.replace("salt-", ""): Path(valid_path_1), valid_name_2.replace("salt-", ""): Path(valid_path_2)}
    actual = await mock_hub.saltenv.ops.local_version_list()
    assert expected == actual


async def test_fill_local_version_list(mock_hub, hub):
    # Link the real function to the mock_hub
    mock_hub.saltenv.ops.fill_local_version_list = hub.saltenv.ops.fill_local_version_list

    # Default LOCAL_VERSIONS to {}    
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {}

    # Set the mocked return value of local_version_list to be {}
    # and confirm that the local_version_list value does not change
    mock_hub.saltenv.ops.local_version_list.return_value = {}
    
    # Call fill_local_version_list
    await mock_hub.saltenv.ops.fill_local_version_list()
    
    # Confirm the value of LOCAL_VERSIONS matches our expected results
    expected = {}
    assert mock_hub.saltenv.ops.LOCAL_VERSIONS == expected
 
    # Now set the mocked return value to contain an element. This dictionary
    # with one element will be returned by local_version_list and stored
    # within the LOCAL_VERSIONS dict
    mock_hub.saltenv.ops.local_version_list.return_value = {"salt-3001": Path('mocked/path/salt-3001')}
    
    # Call fill_local_version_list to populate the LOCAL_VERSIONS dict
    await mock_hub.saltenv.ops.fill_local_version_list()

    # Confirm the value of LOCAL_VERSION matches our expected results
    expected = {"salt-3001": Path('mocked/path/salt-3001')}
    assert mock_hub.saltenv.ops.LOCAL_VERSIONS == expected
    
