# Lucee Docker Images

[![](https://api.travis-ci.org/lucee/lucee-dockerfiles.svg?branch=travis-build-matrix)](https://travis-ci.org/lucee/lucee-dockerfiles)
[![](https://images.microbadger.com/badges/image/lucee/lucee.svg)](https://microbadger.com/images/lucee/lucee)

[Lucee](http://www.lucee.org/) application engine running on [Apache Tomcat](https://tomcat.apache.org/) J2EE application server.


## Supported tags and respective Dockerfile links

### Latest stable release (5.2)

- `5.2.9.31-tomcat8.5-jre8`, `5.2.9.31`, `5.2`, `latest` ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/travis-build-matrix/Dockerfile))
  - `5.2.9.31-nginx-tomcat8.5-jre8`, `5.2.9.31-nginx`, `5.2-nginx` ([Dockerfile.nginx](https://github.com/lucee/lucee-dockerfiles/blob/travis-build-matrix/Dockerfile.nginx))
  - `5.2.9.31-tomcat8.5-jre8-alpine`, `5.2.9.31-alpine`, `5.2-alpine` ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/travis-build-matrix/Dockerfile))
  - `5.2.9.31-nginx-tomcat8.5-jre8-alpine`, `5.2.9.31-nginx-alpine`, `5.2-nginx-alpine` ([Dockerfile.nginx.alpine](https://github.com/lucee/lucee-dockerfiles/blob/travis-build-matrix/Dockerfile.nginx.alpine))

### Bleeding edge Snapshot / RC / Beta (5.3)

- `5.3.2.33-SNAPSHOT-tomcat9.0-jre11`, `5.3.2.33-SNAPSHOT`
  - `5.3.2.33-SNAPSHOT-nginx-tomcat9.0-jre11`, `5.3.2.33-SNAPSHOT-nginx`
  - `5.3.2.33-SNAPSHOT-tomcat9.0-jre8-alpine`, `5.3.2.33-SNAPSHOT-alpine`
  - `5.3.2.33-SNAPSHOT-nginx-tomcat9.0-jre8-alpine`, `5.3.2.33-SNAPSHOT-nginx-alpine`


## Example Project Dockerfile

For the latest stable release with Tomcat only:

```
FROM lucee/lucee:5.2

# Lucee configs
COPY config/lucee/ /opt/lucee/web/
# Code
COPY www /var/www
```

For the latest stable release with NGINX and Tomcat:

```
FROM lucee/lucee:5.2-nginx

# NGINX configs
COPY config/nginx/ /etc/nginx/
# Lucee configs
COPY config/lucee/ /opt/lucee/web/
# Code
COPY www /var/www
```


## Features

### Java optisation tweaks

- JVM is set to [use /dev/urandom as an entropy source for secure random numbers](http://support.run.pivotal.io/entries/59869725-Java-Web-Applications-Slow-Startup-or-Failing) to avoid blocking Tomcat on startup.

- Tomcat is configured to [skip the default scanning of Jar files on startup](http://www.gpickin.com/index.cfm/blog/how-to-get-your-tomcat-to-pounce-on-startup-not-crawl), significantly improving startup time.

### Optimised for single-site application

The default configuration serves a single application for any hostname on the listening port. Multiple applications can be supported by editing the server.xml in the Tomcat config.


## Using this image

### Accessing the service

Lucee server's Tomcat installation listens on port 8888.

This base image exposes port 8080 to linked containers but its **not used**.You must publish or expose port 8888 if you wish to access Tomcat from your installation.

### Accessing the Web admin

The Lucee admin URL is `/lucee/admin/` from the exposed port. No admin passwords are set.

**THIS IS NOT A SECURE CONFIGURATION FOR PRODUCTION ENVIRONMENTS!** It is **strongly** recommended that you secure the container by:

- Changing the server password
- Using IP or URL filtering to restrict access to the Lucee web admin
- Following recommended security practices such as the [Lucee Lockdown Guide](https://bitbucket.org/lucee/lucee/wiki/tips_and_tricks_Lockdown_Guide)

The NGINX tagged Docker images are configured to deny access to the Lucee admin by default in the nginx `default.conf`.

### Folder locations

Web root for default site: /var/www

Configuration folders:

- Tomcat config: /usr/local/tomcat/conf
- Lucee config for default site: /opt/lucee/web
- Lucee server context: /opt/lucee/server/lucee-server/context

Log folders:

- Tomcat logs: /usr/local/tomcat/logs
- Lucee logs for default site: /opt/lucee/web/logs

### Environment variables

The default image contains scripts that use the following environment variables if they are set in the container.

`LUCEE_JAVA_OPTS`: Additional JVM parameters for Tomcat. Used by /usr/local/tomcat/bin/setenv.sh. Default: "-Xms64m -Xmx512m".

# Contributing to this Project

The Lucee Dockerfiles project is maintained by the community. Chief protagonist is @justincarter ([Justin Carter](https://github.com/justincarter) of [Daemon](http://www.daemon.com.au)). Bug reports and pull requests are most welcome.

Special thanks to @rye ([Kristofer Rye](https://github.com/rye)) and @hawkrives ([Hawken Rives](https://github.com/hawkrives)) for their work on the Travis build matrix.

# License

The Docker files and config files are available under the [MIT License](LICENSE). The Lucee engine, Tomcat, NGINX and any other softwares are available under their respective licenses.
