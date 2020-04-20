if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    export PATH="/usr/local/opt/openssl@1.1/bin:$PATH"'
    source ~/venv/bin/activate
else
    echo "linux"
fi

