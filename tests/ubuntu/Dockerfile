#
# A basic linux system that installs carapace, to verify behaviors
#

FROM ubuntu:16.04
MAINTAINER Chris Heilman <chris.heilman@gmail.com>

# Add necessary packages
RUN apt-get update && \
        apt-get upgrade -y && \
        apt-get install -y \
            software-properties-common

# Install PPAs and needed packages
RUN add-apt-repository ppa:git-core/ppa && \
        apt-get update && \
        apt-get install -y \
            git \
            vim \
            wget \
            zsh

# Add a user
RUN adduser --disabled-password --shell /usr/bin/zsh caratest
USER caratest

# Download and install carapace
ENV TESTHOME=/home/caratest
RUN cd $TESTHOME && \
        git clone https://github.com/cheilman/carapace.git .carapace && \
        $HOME/.carapace/install/carapace-install

