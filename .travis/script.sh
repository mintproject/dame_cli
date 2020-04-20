if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    source ~/venv/bin/activate
    tox
else
    echo "linux"
fi

