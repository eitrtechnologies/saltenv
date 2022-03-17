def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # The run.py is where your app should usually start
    for dyne in ["acct", "exec", "idem", "tool"]:
        hub.pop.sub.add(dyne_name=dyne)
    for dyne in ["exec", "tool"]:
        hub.pop.sub.load_subdirs(getattr(hub, dyne), recurse=True)


def cli(hub):
    hub.pop.config.load(["saltenv"], cli="saltenv")
    # Your app's options can now be found under hub.OPT.saltenv
    kwargs = dict(hub.OPT.saltenv)

    # Initialize the asyncio event loop
    hub.pop.loop.create()

    # Start the async code
    coroutine = hub.saltenv.init.run(**kwargs)
    hub.pop.Loop.run_until_complete(coroutine)


async def run(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    if hub.SUBPARSER == "list":
        return await hub.saltenv.cli.list()
    elif hub.SUBPARSER == "list-remote":
        return await hub.saltenv.cli.list_remote()
    elif hub.SUBPARSER == "install":
        return await hub.saltenv.cli.install()
