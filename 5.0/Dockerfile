FROM tomcat:8.0.41-jre8

MAINTAINER Daemonites <hello@daemon.com.au>

ENV LUCEE_JARS_URL http://release.lucee.org/rest/update/provider/loader/5.0.1.85
ENV LUCEE_JAVA_OPTS "-Xms256m -Xmx512m"

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

# Provide test page
RUN mkdir -p /var/www
COPY index.cfm /var/www/
ONBUILD RUN rm -rf /var/www/*

# lucee first time startup; explodes lucee and installs bundles/extensions
RUN /usr/local/tomcat/bin/catalina.sh start && \
    while [ ! -f "/opt/lucee/web/logs/application.log" ] ; do sleep 2; done && \
    /usr/local/tomcat/bin/catalina.sh stop

# Replace the Trusted SSL Certificates packaged with Lucee with those from Debian
#   ca-certificates package from the OS is the most recent authority
RUN cp -f /etc/ssl/certs/java/cacerts /opt/lucee/server/lucee-server/context/security/cacerts
