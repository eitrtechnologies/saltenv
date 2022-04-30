from unittest.mock import AsyncMock


async def test_unit_pin(mock_hub, hub):
    # Link the function to the mock_hub
    mock_hub.saltenv.cli.pin = hub.saltenv.cli.pin

    mock_hub.saltenv.ops.pin_current_version = AsyncMock()

    # Call the pin function
    await mock_hub.saltenv.cli.pin()

    # Confirm that pin_version was called
    mock_hub.saltenv.ops.pin_current_version.assert_called_once_with()
