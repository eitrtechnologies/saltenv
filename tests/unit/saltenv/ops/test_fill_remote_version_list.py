import mock
from pathlib import Path


async def test_unit_fill_remote_version_list(mock_hub, hub):
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
