#!/bin/bash
/opt/webshot/startenv.sh
su -c "/opt/webshot/capture.sh" webshot
if [ $? -eq 0 ]; then
    echo "Pipeline completed successfully"
else
    echo "Pipeline failed" >&2
    exit 1
fi
