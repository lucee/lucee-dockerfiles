#!/bin/sh
set -e

LUCEE_MINOR=$1

if [ "$LUCEE_MINOR" = "5.2" ]; then

    # legacy warmup support for Lucee 5.2 only
    /usr/local/tomcat/bin/catalina.sh start
    while [ ! -f "/opt/lucee/web/logs/application.log" ] ; do sleep 2; done
    while [ ! -d "/opt/lucee/server/lucee-server/deploy" ] ; do sleep 2; done
    sleep 1
    /usr/local/tomcat/bin/catalina.sh stop
    sleep 3
    rm -rf /opt/lucee/web/logs/*

    /usr/local/tomcat/bin/catalina.sh start
    while [ ! -f "/opt/lucee/web/logs/application.log" ] ; do sleep 2; done
    while [ ! -d "/opt/lucee/server/lucee-server/deploy" ] ; do sleep 2; done
    sleep 1
    /usr/local/tomcat/bin/catalina.sh stop
    sleep 3
    rm -rf /opt/lucee/web/logs/*

else

    # native warmup support
    LUCEE_ENABLE_WARMUP=true /usr/local/tomcat/bin/catalina.sh start

fi
