#! /bin/bash
BASE_IMAGE_NAME=idlaborg
IMAGE_TAG=latest

# AATH
AATH_REPO=https://github.com/hyperledger/aries-agent-test-harness.git
AATH_DIRECTORY=$PWD/aries-agent-test-harness
git clone $AATH_REPO

cd $AATH_DIRECTORY/aries-backchannels
IMAGE_NAME=$BASE_IMAGE_NAME/aath-backchannel-acapy
docker build \
    -t $IMAGE_NAME:$IMAGE_TAG \
    -f acapy/Dockerfile.acapy-main . \
    && docker push $IMAGE_NAME:$IMAGE_TAG
IMAGE_NAME=$BASE_IMAGE_NAME/aath-backchannel-afgo
docker build \
    -t $IMAGE_NAME:$IMAGE_TAG \
    -f afgo/Dockerfile.afgo-master . \
    --build-arg="REPO_URL=https://github.com/hyperledger/aries-framework-go.git" \
    && docker push $IMAGE_NAME:$IMAGE_TAG
IMAGE_NAME=$BASE_IMAGE_NAME/aath-backchannel-vcx
docker build \
    -t $IMAGE_NAME:$IMAGE_TAG \
    -f aries-vcx/Dockerfile.aries-vcx . \
    && docker push $IMAGE_NAME:$IMAGE_TAG
IMAGE_NAME=$BASE_IMAGE_NAME/aath-backchannel-dotnet
docker build \
    -t $IMAGE_NAME:$IMAGE_TAG \
    -f dotnet/Dockerfile.dotnet-master . \
    && docker push $IMAGE_NAME:$IMAGE_TAG
IMAGE_NAME=$BASE_IMAGE_NAME/aath-backchannel-findy
docker build \
    -t $IMAGE_NAME:$IMAGE_TAG \
    -f findy/Dockerfile.findy . \
    && docker push $IMAGE_NAME:$IMAGE_TAG
IMAGE_NAME=$BASE_IMAGE_NAME/aath-backchannel-afj
docker build \
    -t $IMAGE_NAME:$IMAGE_TAG \
    -f javascript/Dockerfile.javascript . \
    && docker push $IMAGE_NAME:$IMAGE_TAG

cd $AATH_DIRECTORY/aries-test-harness
IMAGE_NAME=$BASE_IMAGE_NAME/aath-test-harness
docker build \
    -t $IMAGE_NAME:$IMAGE_TAG \
    -f Dockerfile.harness . \
    && docker push $IMAGE_NAME:$IMAGE_TAG
