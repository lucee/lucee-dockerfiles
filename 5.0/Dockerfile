FROM tomcat:8-jre8

MAINTAINER Geoff Bowers <modius@daemon.com.au>

ENV LUCEE_JARS_URL http://daemon-provisioning-resources.s3.amazonaws.com/lucee/5.0/lucee-all-5.0.0.175-SNAPSHOT.jar

# Download core JAR, and delete it in one step to avoid committing the installer in a FS layer
RUN wget -nv $LUCEE_JARS_URL -O /root/lucee.jar && \
	mkdir -p /usr/local/tomcat/lucee && \
	cp /root/lucee.jar /usr/local/tomcat/lucee/lucee.jar && \
	rm -rf /root/lucee.jar

# Delete the default Tomcat webapps so they aren't deployed at startup
RUN rm -rf /usr/local/tomcat/webapps/*

# Set Tomcat config to load Lucee
COPY catalina.properties server.xml web.xml /usr/local/tomcat/conf/

# Custom setenv.sh to load Lucee
COPY setenv.sh /usr/local/tomcat/bin/
RUN chmod a+x /usr/local/tomcat/bin/setenv.sh

# Create Lucee configs
COPY lucee-server.xml /opt/lucee/server/lucee-server/context/lucee-server.xml
COPY lucee-web.xml.cfm /opt/lucee/web/lucee-web.xml.cfm

# Create webroot with a default index.cfm
RUN mkdir -p /var/www
COPY index.cfm /var/www/

# Remove test page when used as base image
ONBUILD RUN rm -rf /var/www/*