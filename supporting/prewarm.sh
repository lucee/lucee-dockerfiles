#!/bin/sh

/usr/local/tomcat/bin/catalina.sh start
while [ ! -f "/opt/lucee/web/logs/application.log" ] ; do sleep 2; done && \
/usr/local/tomcat/bin/catalina.sh stop
rm -rf /opt/lucee/web/logs/*
