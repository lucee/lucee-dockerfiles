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
	apt-get install -y --no-install-recommends zip unzip wget && \
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

# Replace web.xml init-params with env vars (honored by Lucee 6.2+)
ENV LUCEE_SERVER_DIR=/opt/lucee/server
ENV LUCEE_WEB_DIR=/opt/lucee/web

# Download Lucee JAR
RUN mkdir -p /usr/local/tomcat/lucee
ADD ${LUCEE_JAR_URL} /usr/local/tomcat/lucee/lucee.jar

# Only execute if the major version is at least 10
# Check the major version and conditionally add the JAR files
RUN MAJOR_VERSION=$(echo ${TOMCAT_VERSION} | awk -F. '{print $1}') && \
	if [ "$MAJOR_VERSION" -ge 10 ]; then \
	wget -P /usr/local/tomcat/lib https://repo1.maven.org/maven2/javax/servlet/javax.servlet-api/4.0.1/javax.servlet-api-4.0.1.jar && \
	wget -P /usr/local/tomcat/lib https://repo1.maven.org/maven2/javax/servlet/jsp/javax.servlet.jsp-api/2.3.3/javax.servlet.jsp-api-2.3.3.jar && \
	wget -P /usr/local/tomcat/lib https://repo1.maven.org/maven2/javax/el/javax.el-api/3.0.0/javax.el-api-3.0.0.jar; \
	fi


# Copy the config directory to the build context
COPY config/ /config/

# Define the TOMCAT_MAJOR_MINOR_VERSION dynamically and conditionally copy the files
RUN TOMCAT_MAJOR_MINOR_VERSION=$(echo ${TOMCAT_VERSION} | awk -F. '{print $1 "." $2}') && \
	mkdir -p /usr/local/tomcat/conf /opt/lucee/server/lucee-server/context /opt/lucee/web && \
	if [ -f "/config/tomcat/${TOMCAT_MAJOR_MINOR_VERSION}/web.xml" ]; then \
	cp "/config/tomcat/${TOMCAT_MAJOR_MINOR_VERSION}/web.xml" /usr/local/tomcat/conf/web.xml; \
	fi && \
	if [ -f "/config/tomcat/${TOMCAT_MAJOR_MINOR_VERSION}/catalina.properties" ]; then \
	cp "/config/tomcat/${TOMCAT_MAJOR_MINOR_VERSION}/catalina.properties" /usr/local/tomcat/conf/catalina.properties; \
	fi && \
	if [ -f "/config/tomcat/${TOMCAT_MAJOR_MINOR_VERSION}/server.xml" ]; then \
	cp "/config/tomcat/${TOMCAT_MAJOR_MINOR_VERSION}/server.xml" /usr/local/tomcat/conf/server.xml; \
	fi && \
	if [ -f "/config/lucee/${LUCEE_MINOR}/lucee-server.xml" ]; then \
	cp "/config/lucee/${LUCEE_MINOR}/lucee-server.xml" /opt/lucee/server/lucee-server/context/lucee-server.xml; \
	fi && \
	if [ -f "/config/lucee/${LUCEE_MINOR}/lucee-web.xml.cfm" ]; then \
	cp "/config/lucee/${LUCEE_MINOR}/lucee-web.xml.cfm" /opt/lucee/web/lucee-web.xml.cfm; \
	fi && \
	rm -rf /config


# Custom setenv.sh to load Lucee
COPY supporting/setenv.sh /usr/local/tomcat/bin/
RUN chmod a+x /usr/local/tomcat/bin/setenv.sh

# Provide test page
RUN mkdir -p /var/www
COPY www/ /var/www/
ONBUILD RUN rm -rf /var/www/*

# Non-root user and read-only rootfs support (Lucee 6.2+ / Tomcat 11.x+ only)
RUN MAJOR_VERSION=$(echo ${TOMCAT_VERSION} | awk -F. '{print $1}') && \
	if [ "$MAJOR_VERSION" -ge 11 ]; then \
		groupadd -r -g 999 lucee && \
		useradd -r -u 999 -g lucee -s /bin/false -M lucee && \
		mkdir -p /opt/lucee/server-runtime && \
		chown -R lucee:lucee \
			/opt/lucee \
			/usr/local/tomcat/logs \
			/usr/local/tomcat/temp \
			/usr/local/tomcat/work \
			/var/www && \
		chmod 644 /usr/local/tomcat/lucee/lucee.jar; \
	fi

# Declare VOLUMEs so writable paths work under --read-only without --tmpfs
VOLUME ["/usr/local/tomcat/logs", "/usr/local/tomcat/temp", "/usr/local/tomcat/work", "/opt/lucee/server-runtime", "/tmp"]

# Lucee first time startup; explodes lucee and installs bundles/extensions
COPY supporting/prewarm.sh /usr/local/tomcat/bin/
RUN chmod +x /usr/local/tomcat/bin/prewarm.sh
RUN /usr/local/tomcat/bin/prewarm.sh ${LUCEE_MINOR}

# Entrypoint handles LUCEE_RUNTIME_DIR seeding for read-only rootfs support
COPY supporting/docker-entrypoint.sh /usr/local/tomcat/bin/
RUN chmod +x /usr/local/tomcat/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/tomcat/bin/docker-entrypoint.sh"]
# Setting ENTRYPOINT above clears the Tomcat base image's CMD; restore it
CMD ["catalina.sh", "run"]
