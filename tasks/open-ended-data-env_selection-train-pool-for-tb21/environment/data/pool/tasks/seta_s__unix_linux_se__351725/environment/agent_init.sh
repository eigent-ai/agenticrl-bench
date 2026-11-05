#!/bin/bash
DEPLOY_KEY="/opt/deploy/keys/ci_key"

ssh-agent
ssh-add "$DEPLOY_KEY"
