#!/bin/bash

# All LUKS environment setup is done at image build time.
# Simply hand off to whatever command was passed (default: sleep infinity).
exec "$@"
