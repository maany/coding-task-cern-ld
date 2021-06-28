import nox


@nox.session()
def lint(session):
    session.install("flake8")
    session.run("flake8", "python")

@nox.session(python="3.7")
def test(session):
    session.run("python","-m", "unittest", "python/test.py")

@nox.session(python="3.7")
def coverage(session):
    session.install("coverage")
    session.run("coverage", "run", "-m", "unittest", "python/test.py")
    session.run("coverage", "report")

@nox.session()
def build(session):
    session.run("bash", "./build-deliverables.sh")
