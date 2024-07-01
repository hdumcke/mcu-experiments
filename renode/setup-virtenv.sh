#!/bin/bash

pip install git+https://github.com/antmicro/pyrenode.git
pip install git+https://github.com/antmicro/renode-run
cat > /tmp/renode << EOF
#!/bin/bash

mono /Applications/Renode.app/Contents/MacOS/bin/Renode.exe \$@
EOF
cat > /tmp/renode-test << EOF
#!/bin/bash

/Applications/Renode.app/Contents/MacOS/tests/renode-test \$@
EOF
chmod +x /tmp/renode
chmod +x /tmp/renode-test
mv  /tmp/renode $VIRTUAL_ENV/bin
mv  /tmp/renode-test $VIRTUAL_ENV/bin

pip install --upgrade pip
pip install -U pip setuptools
pip install "cython<3.0.0"
pip install --no-build-isolation pyyaml==6.0
pip install -r /Applications/Renode.app/Contents/MacOS/tests/requirements.txt
