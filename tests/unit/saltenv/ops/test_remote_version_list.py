import mock
from pathlib import Path


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


async def test_remote_version_list_invalid_response1(mock_hub, hub):
    """
    SCENARIO #1: There is no valid "ret" value given in the request response
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.remote_version_list = hub.saltenv.ops.remote_version_list

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


async def test_remote_version_list_invalid_response2(mock_hub, hub):
    """
    SCENARIO #2: A HttpStatus error occurred (i.e., 404)
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.remote_version_list = hub.saltenv.ops.remote_version_list

    # Set the return value of the mocked hub.exec.request.raw.get to be an invalid return object.
    # Note: Only the some of the dictionary values are included in this mocked return object.
    # This is because many values are not necessary from a testing perspective.
    mock_hub.exec.request.raw.get.return_value = {
        "result": False,
        "ret": "An incorrect query parameter was specified",
        "comment": "Not Found",
        "ref": "exec.request.raw.get",
        "status": 404,
        "headers": {},
    }

    # Compare the actual and expected results
    expected = {}
    actual = await mock_hub.saltenv.ops.remote_version_list()
    assert expected == actual
