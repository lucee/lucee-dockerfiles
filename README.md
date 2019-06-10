# Lucee Docker Images

[![](https://api.travis-ci.org/lucee/lucee-dockerfiles.svg?branch=master)](https://travis-ci.org/lucee/lucee-dockerfiles)
[![](https://images.microbadger.com/badges/image/lucee/lucee.svg)](https://microbadger.com/images/lucee/lucee)
[![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee/)

[Lucee](http://www.lucee.org/) application engine running on [Apache Tomcat](https://tomcat.apache.org/) J2EE application server.


## Supported tags and respective Dockerfile links

### Latest stable release (5.3)

**Tomcat 9.0 with OpenJDK 11 (recommended)**

- `5.3.2.77-tomcat9.0-jre11`, `5.3.2.77`, **`5.3`**, **`latest`** ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile))
  - `5.3.2.77-nginx-tomcat9.0-jre11`, `5.3.2.77-nginx`, **`5.3-nginx`** ([Dockerfile.nginx](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile.nginx))

Tomcat 9.0 with OpenJDK 8

- `5.3.2.77-tomcat9.0-jre8`, ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile))
  - `5.3.2.77-nginx-tomcat9.0-jre8` ([Dockerfile.nginx](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile.nginx))
  - `5.3.2.77-tomcat9.0-jre8-alpine`, ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile))
  - `5.3.2.77-nginx-tomcat9.0-jre8-alpine` ([Dockerfile.nginx.alpine](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile.nginx.alpine))


## How the tags work

The Lucee Docker image tags follow a naming convention which is used to produce "simple tags" that are updated with each release (e.g. `5.3`, `5.3-nginx`) as well as "full tags" which allow for very specific version targeting (e.g. `5.3.2.77-tomcat9.0-jre11`).

The tag naming convention is;

`LUCEE_VERSION[-RELEASE_TYPE][-light][-nginx][-TOMCAT_VERSION-JRE_VERSION][-alpine]`

- `LUCEE_VERSION` is the Lucee Version number string. For simple tags it may optionally be in the `MAJOR.MINOR` format (e.g. `5.3`) and for full tags it's in the `MAJOR.MINOR.PATCH.BUILD` format (e.g. `5.3.2.77`). Snapshot, RC and Beta builds always include the full version number.
- `RELEASE_TYPE` is the type of release; omitted for Releases, otherwise `SNAPSHOT`, `RC` or `BETA`
- `-light` (optional) is a build with the Lucee "Light" JAR file, WITHOUT any extensions (users must install extensions separately, this includes database drivers, ORM, ESAPI, S3, image handling, etc)
- `-nginx` (optional) is a build with the NGINX web server bundled and configured
- `-TOMCAT_VERSION-JRE_VERSION` is the Tomcat major and minor version and OpenJDK major version of the build to allow users to choose between different combinations (e.g. `tomcat9.0-jre11` vs `tomcat9.0-jre8`). This is omitted for "simple tags" where the recommended Tomcat and OpenJDK versions are used.
- `-alpine` (optional) is a build using Alpine Linux as the base image. This results in a smaller Docker image which may be useful in some scenarios. **NOTE:** Alpine images currently support `jre8` only, `jre11` / Java 11 is not available. Alpine "simple tags" such as `5.3-alpine` will be added in future builds


### Previous stable release (5.2)

Tomcat 8.5 with OpenJDK 8

- `5.2.9.31-tomcat8.5-jre8`, `5.2.9.31`, `5.2`, `latest` ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile))
  - `5.2.9.31-nginx-tomcat8.5-jre8`, `5.2.9.31-nginx`, `5.2-nginx` ([Dockerfile.nginx](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile.nginx))
  - `5.2.9.31-tomcat8.5-jre8-alpine`, `5.2.9.31-alpine`, `5.2-alpine` ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile))
  - `5.2.9.31-nginx-tomcat8.5-jre8-alpine`, `5.2.9.31-nginx-alpine`, `5.2-nginx-alpine` ([Dockerfile.nginx.alpine](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile.nginx.alpine))


### Bleeding edge Snapshot / RC / Beta (5.3)

- `5.3.3.34-SNAPSHOT-tomcat9.0-jre11`, `5.3.3.34-SNAPSHOT`
  - `5.3.3.34-SNAPSHOT-nginx-tomcat9.0-jre11`, `5.3.3.34-SNAPSHOT-nginx`
  - `5.3.3.34-SNAPSHOT-tomcat9.0-jre8-alpine`, `5.3.3.34-SNAPSHOT-alpine`
  - `5.3.3.34-SNAPSHOT-nginx-tomcat9.0-jre8-alpine`, `5.3.3.34-SNAPSHOT-nginx-alpine`

The `SNAPSHOTS` Docker image builds are automatically generated after a successful Lucee build. The `5.3.3.34` version number above is just an example of the latest SNAPSHOT version number; check the [Docker Hub tags](https://hub.docker.com/r/lucee/lucee/tags) and/or the [Lucee Downloads](https://download.lucee.org/) page to see the latest SNAPSHOT version numbers.

The `RC` and `Beta` builds are manually triggered when they are announced.


## Example Project Dockerfile

For the latest stable release with Tomcat only:

```
FROM lucee/lucee:5.3

# Lucee configs
COPY config/lucee/ /opt/lucee/web/
# Code
COPY www /var/www
```

For the latest stable release with NGINX and Tomcat:

```
FROM lucee/lucee:5.3-nginx

# NGINX configs
COPY config/nginx/ /etc/nginx/
# Lucee configs
COPY config/lucee/ /opt/lucee/web/
# Code
COPY www /var/www
```


## Features

### Java optimisation tweaks

- JVM is set to [use `/dev/urandom` as an entropy source for secure random numbers](http://support.run.pivotal.io/entries/59869725-Java-Web-Applications-Slow-Startup-or-Failing) to avoid blocking Tomcat on startup.

- Tomcat is configured to [skip the default scanning of Jar files on startup](http://www.gpickin.com/index.cfm/blog/how-to-get-your-tomcat-to-pounce-on-startup-not-crawl), significantly improving startup time.

### Optimised for single-site application

The default configuration serves a single application for any hostname on the listening port. Multiple applications can be supported by editing the server.xml in the Tomcat config.


## Using this image

### Accessing the service

Lucee server's Tomcat installation listens on port 8888.

This base image exposes port 8080 to linked containers but its **not used**. You must publish or expose port 8888 if you wish to access Tomcat from your installation.

### Accessing the Lucee Admin

The Lucee Admin URL is `/lucee/admin/` from the exposed port. No admin passwords are set.

**THIS IS NOT A SECURE CONFIGURATION FOR PRODUCTION ENVIRONMENTS!** It is **strongly** recommended that you secure the container by:

- Changing the server password
- Using IP or URL filtering to restrict access to the Lucee Admin
- Following recommended security practices such as the [Lucee Lockdown Guide](https://docs.lucee.org/guides/deploying-lucee-server-apps/lockdown-guide.html)

The NGINX tagged Docker images are configured to deny access to the Lucee Admin by default in the `default.conf`.

### Folder locations

Web root for default site: `/var/www`

Configuration folders:

- Tomcat config: `/usr/local/tomcat/conf`
- Lucee config for default site: `/opt/lucee/web`
- Lucee server context: `/opt/lucee/server/lucee-server/context`

Log folders:

- Tomcat logs: `/usr/local/tomcat/logs`
- Lucee logs for default site: `/opt/lucee/web/logs`

### Environment variables

The default image contains scripts that use the following environment variables if they are set in the container.

`LUCEE_JAVA_OPTS`: Additional JVM parameters for Tomcat. Used by /usr/local/tomcat/bin/setenv.sh. Default: "-Xms64m -Xmx512m".


## Legacy Lucee Base Images

The older Lucee Base Images will remain available for the projects that are using them, though the build process for those images is considered "legacy" as they have been superseded by the new build matrix builds.

The base images can be accessed in the existing Docker Hub repositories and the source is now in the `legacy` branch;

https://github.com/lucee/lucee-dockerfiles/tree/legacy


### Lucee 5.2 (Legacy builds)

- [nginx + Tomcat 8.0-JRE8](./lucee-nginx/5.2/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee52-nginx.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee52-nginx/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee52-nginx.svg)](https://microbadger.com/images/lucee/lucee52-nginx)
- [Tomcat 8.0-JRE8](./5.2/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee52.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee52/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee52.svg)](https://microbadger.com/images/lucee/lucee52)

### Lucee 5.1 (Legacy builds)

- [nginx + Tomcat 8.0-JRE8](./lucee-nginx/5.1/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee51-nginx.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee51-nginx/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee51-nginx.svg)](https://microbadger.com/images/lucee/lucee51-nginx)
- [Tomcat 8.0-JRE8](./5.1/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee51.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee51/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee51.svg)](https://microbadger.com/images/lucee/lucee51)

### Lucee 5.0 (Legacy builds)

- [nginx + Tomcat 8.0-JRE8](./lucee-nginx/5.0/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee5-nginx.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee5-nginx/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee5-nginx.svg)](https://microbadger.com/images/lucee/lucee5-nginx)
- [Tomcat 8.0-JRE8](./5.0/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee5.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee5/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee5.svg)](https://microbadger.com/images/lucee/lucee5)

### Lucee 4.5 (Legacy builds)

- [nginx + Tomcat 8.0-JRE8](./lucee-nginx/4.5/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee4-nginx.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee4-nginx/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee4-nginx.svg)](https://microbadger.com/images/lucee/lucee4-nginx)
- [Tomcat 8.0-JRE8](./4.5/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee4.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee4/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee4.svg)](https://microbadger.com/images/lucee/lucee4)


# Contributing to this Project

The Lucee Dockerfiles project is maintained by the community. Chief protagonist is @justincarter ([Justin Carter](https://github.com/justincarter) of [Daemon](http://www.daemon.com.au)). Bug reports and pull requests are most welcome.

Special thanks to @rye ([Kristofer Rye](https://github.com/rye)) and @hawkrives ([Hawken Rives](https://github.com/hawkrives)) for their work on the Travis build matrix.


# License

The Docker files and config files are available under the [MIT License](LICENSE). The Lucee engine, Tomcat, NGINX and any other softwares are available under their respective licenses.
