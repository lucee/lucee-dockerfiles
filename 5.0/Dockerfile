# Lucee 5.0.0.84-SNAPSHOT
FROM tomcat:8-jre8

MAINTAINER Geoff Bowers <modius@daemon.com.au>

ENV LUCEE_JARS_URL http://stable.lucee.org/rest/update/provider/loader/5.0.0.84-SNAPSHOT
ENV LUCEE_DEPS_URL http://stable.lucee.org/rest/update/provider/dependencies/5.0.0.84-SNAPSHOT

# set up installation directories
RUN mkdir -p /opt/lucee/server/lucee-server/context /opt/lucee/server/lucee-server/patches /opt/lucee/web /usr/local/tomcat/lucee

# Download core JAR, and delete it in one step to avoid committing the installer in a FS layer
RUN wget -nv $LUCEE_JARS_URL -O /root/lucee.jar && \
	mkdir -p /usr/local/tomcat/lucee && \
	cp /root/lucee.jar /usr/local/tomcat/lucee/lucee.jar && \
	rm -rf /root/lucee.jar

# Download lucee dependencies
RUN wget -nv $LUCEE_DEPS_URL -O /root/lucee-jars.zip && \
	unzip /root/lucee-jars.zip -d /opt/lucee/server/lucee-server/bundles && \
	rm -rf /root/lucee-jars.zip

# COPY over random missing dependencies
COPY org.apache.felix.framework-4.2.1.jar /usr/local/tomcat/lucee/

# Delete the default Tomcat webapps so they aren't deployed at startup
RUN rm -rf /usr/local/tomcat/webapps/*

# Set Tomcat config to load Lucee
COPY catalina.properties server.xml web.xml /usr/local/tomcat/conf/

# Custom setenv.sh to load Lucee
COPY setenv.sh /usr/local/tomcat/bin/
RUN chmod a+x /usr/local/tomcat/bin/setenv.sh

# Create Lucee config dirs
COPY lucee-server.xml /opt/lucee/server/lucee-server/context/lucee-server.xml
COPY lucee-web.xml.cfm /opt/lucee/web/lucee-web.xml.cfm

# Create webroot with a default index.cfm
RUN mkdir -p /var/www
COPY index.cfm /var/www/

ONBUILD RUN rm -rf /var/www/*
