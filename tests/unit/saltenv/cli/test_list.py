import mock
from pathlib import Path

"""
async def list_(hub, **kwargs):
    '''
    This is the entrypoint for the async code in your project
    '''
    await hub.saltenv.ops.fill_local_version_list()
    current_version = await hub.saltenv.ops.get_current_version()
    version_list = []
    for ver in sorted(hub.saltenv.ops.LOCAL_VERSIONS.keys(), reverse=True):
        prefix = "  "
        suffix = ""
        if ver == current_version[0]:
            prefix = "* "
            suffix = f" (set by {current_version[1]})"
        version_list.append(prefix + ver + suffix)
    print("\n".join(version_list))
"""


async def test_list(mock_hub, hub):
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
