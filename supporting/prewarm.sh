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
    export LUCEE_ENABLE_WARMUP=true
    /usr/local/tomcat/bin/catalina.sh run

fi

# ensure lucee user can read/write all Lucee and Tomcat files at runtime
if id lucee >/dev/null 2>&1; then
    chown -R lucee:lucee \
        /opt/lucee \
        /usr/local/tomcat/logs \
        /usr/local/tomcat/temp \
        /usr/local/tomcat/work \
        /var/www
fi
