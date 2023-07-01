FROM plandes/mimicsid:latest


## User environment
#
ENV DEV_USER=devusr
ENV DEV_GROUP=devgrp


## Setup and install user account
#
USER $DEV_USER
WORKDIR $DEV_USER_HOME

RUN $DEV_USER_HOME/opt/lib/python/bin/pip3 install \
    --use-deprecated=legacy-resolver zensols.dsprov
RUN touch trash.conf
RUN $DEV_USER_HOME/opt/lib/python/bin/dsprov -c trash.conf ids -l 1

# cleanup
RUN rm trash.conf
RUN rm -r .cache/pip

# cached data directory mapped by the container
RUN mkdir -p data

# tell programs where to find the DB parameters for container logins
RUN echo "export DSPROVRC=/mnt/db.conf" >> ~/.profile


## Container config
#
USER root

# default to root home dir on login
WORKDIR /root
