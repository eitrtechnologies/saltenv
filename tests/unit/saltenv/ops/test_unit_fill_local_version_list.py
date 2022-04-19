import mock
from pathlib import Path


async def test_unit_fill_local_version_list(mock_hub, hub):
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
