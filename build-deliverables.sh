#!/usr/bin/env bash
rm -rf python/__pycache__
zip -r solution.zip ./python/ || exit 1;
echo "solution.zip ready";
