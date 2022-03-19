"""
noxfile
~~~~~~~
Nox configuration script
"""
# pylint: disable=resource-leakage,3rd-party-module-not-gated
import datetime
import os
import pathlib
import shutil
import sys
from pathlib import Path

# fmt: off
if __name__ == "__main__":
    sys.stderr.write(
        "Do not execute this file directly. Use nox instead, it will know how to handle this file\n"
    )
    sys.stderr.flush()
    exit(1)
# fmt: on

import nox  # isort:skip
from nox.command import CommandFailed  # isort:skip

# Nox options
#  Reuse existing virtualenvs
nox.options.reuse_existing_virtualenvs = True
#  Don't fail on missing interpreters
nox.options.error_on_missing_interpreters = False

# Python versions to test against
PYTHON_VERSIONS = ("3", "3.7", "3.8", "3.9", "3.10")
# Be verbose when runing under a CI context
CI_RUN = os.environ.get("CI")
PIP_INSTALL_SILENT = CI_RUN is False
SKIP_REQUIREMENTS_INSTALL = "SKIP_REQUIREMENTS_INSTALL" in os.environ
EXTRA_REQUIREMENTS_INSTALL = os.environ.get("EXTRA_REQUIREMENTS_INSTALL")

COVERAGE_VERSION_REQUIREMENT = "coverage==5.5"

# Prevent Python from writing bytecode
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

# Global Path Definitions
REPO_ROOT = pathlib.Path(__file__).resolve().parent
# Change current directory to REPO_ROOT
os.chdir(REPO_ROOT)

ARTIFACTS_DIR = REPO_ROOT / "artifacts"
# Make sure the artifacts directory exists
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

RUNTESTS_LOGFILE = ARTIFACTS_DIR / "runtests-{}.log".format(
    datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")
)
COVERAGE_REPORT_DB = REPO_ROOT / ".coverage"
COVERAGE_REPORT_PROJECT = ARTIFACTS_DIR.relative_to(REPO_ROOT) / "coverage-project.xml"
COVERAGE_REPORT_TESTS = ARTIFACTS_DIR.relative_to(REPO_ROOT) / "coverage-tests.xml"
JUNIT_REPORT = ARTIFACTS_DIR.relative_to(REPO_ROOT) / "junit-report.xml"


def _get_session_python_version_info(session):
    try:
        version_info = session._runner._real_python_version_info
    except AttributeError:
        session_py_version = session.run_always(
            "python",
            "-c" 'import sys; sys.stdout.write("{}.{}.{}".format(*sys.version_info))',
            silent=True,
            log=False,
        )
        version_info = tuple(int(part) for part in session_py_version.split(".") if part.isdigit())
        session._runner._real_python_version_info = version_info
    return version_info


def _get_pydir(session):
    version_info = _get_session_python_version_info(session)
    if version_info < (3, 7):
        session.error("Only Python >= 3.7 is supported")
    return "py{}.{}".format(*version_info)


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    if SKIP_REQUIREMENTS_INSTALL is False:
        # Always have the wheel package installed
        session.install("wheel", silent=PIP_INSTALL_SILENT)
        session.install(COVERAGE_VERSION_REQUIREMENT, silent=PIP_INSTALL_SILENT)
        session.install("-e", ".", silent=PIP_INSTALL_SILENT)

        # Install requirements
        requirements_file = REPO_ROOT / "requirements" / _get_pydir(session) / "tests.txt"
        install_command = [
            "--progress-bar=off",
            "-r",
            str(requirements_file.relative_to(REPO_ROOT)),
        ]
        session.install(*install_command, silent=PIP_INSTALL_SILENT)

        if EXTRA_REQUIREMENTS_INSTALL:
            session.log(
                "Installing the following extra requirements because the "
                "EXTRA_REQUIREMENTS_INSTALL environment variable was set: "
                "EXTRA_REQUIREMENTS_INSTALL='%s'",
                EXTRA_REQUIREMENTS_INSTALL,
            )
            install_command = ["--progress-bar=off"]
            install_command += [req.strip() for req in EXTRA_REQUIREMENTS_INSTALL.split()]
            session.install(*install_command, silent=PIP_INSTALL_SILENT)

    session.run("coverage", "erase")
    args = [
        "--rootdir",
        str(REPO_ROOT),
        f"--log-file={RUNTESTS_LOGFILE}",
        "--log-file-level=debug",
        "--show-capture=no",
        f"--junitxml={JUNIT_REPORT}",
        "--showlocals",
        "-ra",
        "-s",
    ]
    if session._runner.global_config.forcecolor:
        args.append("--color=yes")
    if not session.posargs:
        args.append("tests/")
    else:
        for arg in session.posargs:
            if arg.startswith("--color") and args[0].startswith("--color"):
                args.pop(0)
            args.append(arg)
        for arg in session.posargs:
            if arg.startswith("-"):
                continue
            if arg.startswith(f"tests{os.sep}"):
                break
            try:
                pathlib.Path(arg).resolve().relative_to(REPO_ROOT / "tests")
                break
            except ValueError:
                continue
        else:
            args.append("tests/")
    try:
        session.run("coverage", "run", "-m", "pytest", *args)
    finally:
        # Always combine and generate the XML coverage report
        try:
            session.run("coverage", "combine")
        except CommandFailed:
            # Sometimes some of the coverage files are corrupt which would
            # trigger a CommandFailed exception
            pass
        # Generate report for salt code coverage
        session.run(
            "coverage",
            "xml",
            "-o",
            str(COVERAGE_REPORT_PROJECT),
            "--omit=tests/*",
            "--include=saltenv/*",
        )
        # Generate report for tests code coverage
        session.run(
            "coverage",
            "xml",
            "-o",
            str(COVERAGE_REPORT_TESTS),
            "--omit=saltenv/*",
            "--include=tests/*",
        )
        # Move the coverage DB to artifacts/coverage in order for it to be archived by CI
        if COVERAGE_REPORT_DB.exists():
            shutil.move(str(COVERAGE_REPORT_DB), str(ARTIFACTS_DIR / COVERAGE_REPORT_DB.name))


@nox.session(name="docs-html", python="3")
@nox.parametrize("clean", [False, True])
def docs_html(session, clean):
    """
    Build Sphinx HTML Documentation
    """
    _get_pydir(session)

    # Latest pip, setuptools, and wheel
    install_command = ["--progress-bar=off", "-U", "pip", "setuptools", "wheel"]
    session.install(*install_command, silent=True)

    # Install requirements
    requirements_file = Path("requirements", "docs.txt")
    install_command = ["--progress-bar=off", "-r", str(requirements_file)]
    session.install(*install_command, silent=True)

    build_dir = Path("docs", "_build", "html")
    sphinxopts = "-Wn"
    if clean:
        sphinxopts += "E"
    args = [sphinxopts, "--keep-going", "docs", str(build_dir)]
    session.run("sphinx-build", *args, external=True)


@nox.session(python="3")
def docs(session) -> None:
    """
    Build and serve the Sphinx HTML documentation, with live reloading on file changes, via sphinx-autobuild.

    Note: Only use this in INTERACTIVE DEVELOPMENT MODE. This SHOULD NOT be called
        in CI/CD pipelines, as it will hang.
    """
    _get_pydir(session)

    # Latest pip, setuptools, and wheel
    install_command = ["--progress-bar=off", "-U", "pip", "setuptools", "wheel"]
    session.install(*install_command, silent=True)

    # Install requirements
    requirements_file = Path("requirements", "docs.txt")
    install_command = ["--progress-bar=off", "-r", str(requirements_file)]
    session.install(*install_command, silent=True)

    # Install autobuild req
    install_command = ["--progress-bar=off", "-U", "sphinx-autobuild"]
    session.install(*install_command, silent=True)

    # Launching LIVE reloading Sphinx session
    build_dir = Path("docs", "_build", "html")
    args = ["--watch", ".", "--open-browser", "docs", str(build_dir)]
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)
