FROM tomcat:8.0.53-jre8

MAINTAINER Daemonites <hello@daemon.com.au>

ENV LUCEE_JARS_URL https://cdn.lucee.org/lucee-4.5.5.015-jars.zip
ENV LUCEE_JAVA_OPTS "-Xms256m -Xmx512m"

# Download jars archive, extract it, and delete it in one step to avoid committing the installer in a FS layer
RUN wget -nv $LUCEE_JARS_URL -O /root/lucee-jars.zip && \
	unzip /root/lucee-jars.zip -d /usr/local/tomcat/lucee && \
	rm -rf /root/lucee-jars.zip

# Delete the default Tomcat webapps so they aren't deployed at startup
RUN rm -rf /usr/local/tomcat/webapps/*

# Set Tomcat config to load Lucee
COPY catalina.properties server.xml web.xml /usr/local/tomcat/conf/

# Custom setenv.sh to load Lucee
COPY setenv.sh /usr/local/tomcat/bin/
RUN chmod a+x /usr/local/tomcat/bin/setenv.sh

# Create Lucee config dirs
RUN mkdir -p /opt/lucee/server/lucee-server/context /opt/lucee/web
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
