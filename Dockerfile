ARG TOMCAT_VERSION
ARG TOMCAT_JAVA_VERSION
ARG TOMCAT_BASE_IMAGE

FROM docker.io/library/tomcat:${TOMCAT_VERSION}-${TOMCAT_JAVA_VERSION}${TOMCAT_BASE_IMAGE}

ARG TARGETPLATFORM
ARG BUILDPLATFORM

ARG LUCEE_VERSION
ARG LUCEE_MINOR
ARG LUCEE_SERVER
ARG LUCEE_VARIANT
ARG LUCEE_JAR_URL

RUN echo ver: $LUCEE_VERSION minor: $LUCEE_MINOR server: $LUCEE_SERVER variant: $LUCEE_VARIANT jar: $LUCEE_JAR_URL

# Update packages
RUN DEBIAN_FRONTEND=noninteractive apt update && \
	apt upgrade -y && \
	apt-get install -y --no-install-recommends zip unzip && \
	rm -rf /var/lib/apt/lists/*

# Replace the Trusted SSL Certificates packaged with Lucee with those from
# Java. Different OpenJDK versions have different paths for cacerts
RUN mkdir -p /opt/lucee/server/lucee-server/context/security && \
	if   [ -e "$JAVA_HOME/jre/lib/security/cacerts" ]; then ln -s "$JAVA_HOME/jre/lib/security/cacerts" -t /opt/lucee/server/lucee-server/context/security/; \
	elif [ -e "$JAVA_HOME/lib/security/cacerts" ]; then ln -s "$JAVA_HOME/lib/security/cacerts" -t /opt/lucee/server/lucee-server/context/security/; \
	else echo "Unable to find/symlink cacerts."; exit 1; fi

# Delete the default Tomcat webapps so they aren't deployed at startup
RUN rm -rf /usr/local/tomcat/webapps/*

# Tomcat/Lucee memory settings
# -Xms<size> set initial Java heap size
# -Xmx<size> set maximum Java heap size
ENV LUCEE_JAVA_OPTS "-Xms64m -Xmx512m"

# Download Lucee JAR
RUN mkdir -p /usr/local/tomcat/lucee
ADD ${LUCEE_JAR_URL} /usr/local/tomcat/lucee/lucee.jar

# Set Tomcat config to load Lucee
COPY config/tomcat/catalina.properties \
	config/tomcat/server.xml \
	config/tomcat//web.xml \
	/usr/local/tomcat/conf/

# Custom setenv.sh to load Lucee
COPY supporting/setenv.sh /usr/local/tomcat/bin/
RUN chmod a+x /usr/local/tomcat/bin/setenv.sh

# Create Lucee configs
COPY config/lucee/server.xml /opt/lucee/server/lucee-server/context/lucee-server.xml
COPY config/lucee/web.xml /opt/lucee/web/lucee-web.xml.cfm
COPY config/lucee/config.json /opt/lucee/server/lucee-server/context/.CFConfig.json

# Provide test page
RUN mkdir -p /var/www
COPY www/ /var/www/
ONBUILD RUN rm -rf /var/www/*

# Lucee first time startup; explodes lucee and installs bundles/extensions
COPY supporting/prewarm.sh /usr/local/tomcat/bin/
RUN chmod +x /usr/local/tomcat/bin/prewarm.sh
RUN /usr/local/tomcat/bin/prewarm.sh ${LUCEE_MINOR}
