import mock
from pathlib import Path, PosixPath


async def test_local_version_list_nonexistent_dir(mock_hub, hub):
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.local_version_list = hub.saltenv.ops.local_version_list
    mock_hub.OPT.saltenv.saltenv_dir = "nonexistent_testing_dir"
    actual = await mock_hub.saltenv.ops.local_version_list()
    expected = {}
    assert expected == actual


async def test_local_version_list_existent_dir(mock_hub, hub, tmp_path):
    # Link the function to the mock_hub
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
    expected = {
        valid_name_1.replace("salt-", ""): Path(valid_path_1),
        valid_name_2.replace("salt-", ""): Path(valid_path_2),
    }
    actual = await mock_hub.saltenv.ops.local_version_list()
    assert expected == actual


async def test_fill_local_version_list(mock_hub, hub):
    # Link the function to the mock_hub
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
    mock_hub.saltenv.ops.local_version_list.return_value = {"3001": Path("mocked/path/salt-3001")}

    # Call fill_local_version_list to populate the LOCAL_VERSIONS dict
    await mock_hub.saltenv.ops.fill_local_version_list()

    # Confirm the value of LOCAL_VERSIONS matches our expected results
    expected = {"3001": Path("mocked/path/salt-3001")}
    assert mock_hub.saltenv.ops.LOCAL_VERSIONS == expected


async def test_remote_version_list_valid_response(mock_hub, hub):
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.remote_version_list = hub.saltenv.ops.remote_version_list

    # Set the return value of the mocked hub.exec.request.raw.get to be a valid return object.
    # Note: Only the some of the dictionary values are included in this mocked return object.
    # This is because many values are not necessary from a testing perspective.
    mock_hub.exec.request.raw.get.return_value = {
        "result": True,
        "ret": b'<html><body><pre><a href="../">../</a><a href="3003.3-1/">3003.3-1/</a><a href="3003/">3003/</a><a href="3004-1/">3004-1/</a><a href="3004rc1-1/">3004rc1-1/</a><a href="latest/">latest/</a>2022-02-09 18:36:34+00:00 4.5 KB <a href="repo.json">repo.json</a>2022-02-09 18:36:34+00:00 4.1 KB <a href="repo.mp">repo.mp</a></pre></body></html>',
        "comment": "OK",
        "ref": "exec.request.raw.get",
        "status": 200,
    }

    # Compare the actual and expected results
    expected = {
        "3003.3": "3003.3-1",
        "3003": "3003",
        "3004": "3004-1",
        "3004rc1": "3004rc1-1",
        "latest": "latest",
    }
    actual = await mock_hub.saltenv.ops.remote_version_list()
    assert expected == actual


async def test_remote_version_list_invalid_response(mock_hub, hub):
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.remote_version_list = hub.saltenv.ops.remote_version_list

    ## SCENARIO #1: No ret value
    # Set the return value of the mocked hub.exec.request.raw.get to be an invalid return object.
    # Note: Only the some of the dictionary values are included in this mocked return object.
    # This is because many values are not necessary from a testing perspective.
    mock_hub.exec.request.raw.get.return_value = {
        "result": True,
        "comment": "OK",
        "ref": "exec.request.raw.get",
        "status": 200,
    }

    # Compare the actual and expected results
    expected = {}
    actual = await mock_hub.saltenv.ops.remote_version_list()
    assert expected == actual


async def test_fill_remote_version_list(mock_hub, hub):
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.fill_remote_version_list = hub.saltenv.ops.fill_remote_version_list

    # Default REMOTE_VERSIONS to {}
    mock_hub.saltenv.ops.REMOTE_VERSIONS = {}

    # Set the mocked return value of remote_version_list to be {}
    # and confirm that the remote_version_list value does not change
    mock_hub.saltenv.ops.remote_version_list.return_value = {}

    # Call fill_remote_version_list
    await mock_hub.saltenv.ops.fill_remote_version_list()

    # Confirm the value of REMOTE_VERSIONS matches our expected results
    expected = {}
    assert mock_hub.saltenv.ops.REMOTE_VERSIONS == expected

    # Now set the mocked return value to contain an element. This dictionary
    # with one element will be returned by remote_version_list and stored
    # within the REMOTE_VERSIONS dict
    mock_hub.saltenv.ops.remote_version_list.return_value = {
        "3003.3": "3003.3-1",
        "3003": "3003",
        "3004": "3004-1",
        "3004rc1": "3004rc1-1",
        "latest": "latest",
    }

    # Call fill_remote_version_list to populate the REMOTE_VERSIONS dict
    await mock_hub.saltenv.ops.fill_remote_version_list()

    # Confirm the value of REMOTE_VERSIONS matches our expected results
    expected = {
        "3003.3": "3003.3-1",
        "3003": "3003",
        "3004": "3004-1",
        "3004rc1": "3004rc1-1",
        "latest": "latest",
    }
    assert mock_hub.saltenv.ops.REMOTE_VERSIONS == expected
