#!/bin/sh
set -e

/usr/local/tomcat/bin/catalina.sh start
while [ ! -f "/opt/lucee/web/logs/application.log" ] ; do sleep 2; done
while [ ! -d "/opt/lucee/server/lucee-server/deploy" ] ; do sleep 2; done
sleep 1
/usr/local/tomcat/bin/catalina.sh stop
sleep 3
rm -rf /opt/lucee/web/logs/*