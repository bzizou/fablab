#!/bin/bash

set -e

ssh -o ConnectTimeout=5 -fNR 8001:localhost:443 albator.bzizou.net
ssh -o ConnectTimeout=5 -NR 2222:localhost:22 albator.bzizou.net
exit 1
