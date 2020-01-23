HERE="$(cd "$(dirname "${BASH_SOURCE:-0}")"; pwd)"
REPO_ROOT_DIR="$(cd "$(dirname "$HERE")"; pwd)"
REPO_ROOT_DIR="$(cd "$(dirname "$REPO_ROOT_DIR")"; pwd)"
cd "$REPO_ROOT_DIR"
rm -rf build
rm -rf dist
rm -rf textree.egg-info
python2 setup.py sdist bdist_wheel
python3 setup.py sdist bdist_wheel
sudo pip2 install --upgrade "$(find ./dist/*-py2-*.whl)"
sudo pip3 install --upgrade "$(find ./dist/*-py3-*.whl)"
