# Lucee Docker Images

This repository focuses on building and maintaining the Lucee Docker Images provided for [Lucee](http://www.lucee.org/).


[![Build Lucee Docker Images](https://github.com/lucee/lucee-dockerfiles/actions/workflows/main.yml/badge.svg)](https://github.com/lucee/lucee-dockerfiles/actions/workflows/main.yml)
[![](https://images.microbadger.com/badges/image/lucee/lucee.svg)](https://microbadger.com/images/lucee/lucee)
[![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee/)

[Lucee](http://www.lucee.org/) application engine running on [Apache Tomcat](https://tomcat.apache.org/) J2EE application server.


## Supported tags and respective Dockerfile links

### Latest stable release

**Lucee 6.0.x - Tomcat 9.0 with Java 11 (recommended)**

- `6.0.3.1-tomcat9.0-jre11-temurin-jammy`, `6.0.3.1`, **`6.0`**, **`latest`** ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile))
  - `6.0.3.1-nginx-tomcat9.0-jre11-temurin-jammy`, `6.0.3.1-nginx`, **`6.0-nginx`** ([Dockerfile.nginx](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile.nginx))

### Previous stable release (LTS)

**Lucee 5.4.x - Tomcat 9.0 with Java 11 (recommended)**

- `5.4.5.23-tomcat9.0-jre11-temurin-jammy`, `5.4.5.23`, **`5.4`** ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile))
  - `5.4.5.23-nginx-tomcat9.0-jre11-temurin-jammy`, `5.4.5.23-nginx`, **`5.4-nginx`** ([Dockerfile.nginx](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile.nginx))

Lucee 5.4.x - Tomcat 9.0 with Java 8

- `5.4.5.23-tomcat9.0-jre8-temurin-jammy`, ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile))
  - `5.4.5.23-nginx-tomcat9.0-jre8-temurin-jammy` ([Dockerfile.nginx](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile.nginx))

### Bleeding edge Snapshot / RC / Beta

- `6.1.0.175-BETA-tomcat9.0-jre21-temurin-jammy`, `6.1.0.175-BETA`
  - `6.1.0.175-BETA-nginx-tomcat9.0-jre21-temurin-jammy`, `6.1.0.175-BETA-nginx`
- `6.0.2.41-RC-tomcat9.0-jre11-temurin-jammy`, `6.0.2.41-RC`
  - `6.0.2.41-RC-nginx-tomcat9.0-jre11-temurin-jammy`, `6.0.2.41-RC-nginx`

The `SNAPSHOTS` Docker image builds are automatically generated after a successful Lucee build. Check the [Docker Hub tags](https://hub.docker.com/r/lucee/lucee/tags) and/or the [Lucee Downloads](https://download.lucee.org/) page to see the latest SNAPSHOT version numbers.

The `RC` and `Beta` builds are manually triggered when they are announced.

For more information about Lucee versions and extensions see the [Lucee Downloads](https://download.lucee.org/) page.

## How the tags work

The Lucee Docker image tags follow a naming convention which is used to produce "simple tags" that are updated with each release (e.g. `6.1`, `6.1-nginx`) as well as "full tags" which allow for very specific version targeting (e.g. `6.1.0.175-tomcat9.0-jre21-temurin-jammy`).

The tag naming convention is;

`LUCEE_VERSION[-RELEASE_TYPE][-light][-nginx][-TOMCAT_VERSION-JRE_VERSION]`

- `LUCEE_VERSION` is the Lucee Version number string. For simple tags it may optionally be in the `MAJOR.MINOR` format (e.g. `5.4`) and for full tags it's in the `MAJOR.MINOR.PATCH.BUILD` format (e.g. `6.1.0.175`). Snapshot, RC and Beta builds always include the full version number.
- `RELEASE_TYPE` is the type of release; omitted for Releases, otherwise `SNAPSHOT`, `RC` or `BETA`
- `-light` (optional) is a build with the Lucee "Light" JAR file, WITHOUT any extensions (users must install extensions separately, this includes database drivers, ORM, ESAPI, S3, image handling, etc)
- `-nginx` (optional) is a build with the NGINX web server bundled and configured
- `-TOMCAT_VERSION-JRE_VERSION` is the Tomcat major and minor version and Java major version of the build to allow users to choose between different combinations (e.g. `tomcat9.0-jre11-temurin-jammy` vs `tomcat9.0-jre21-temurin-jammy`). This is omitted for "simple tags" where the recommended Tomcat and Java versions are used.

**Base Image / Operating System Notes:** 
- The Lucee images are based on the [Docker Tomcat images](https://hub.docker.com/_/tomcat).
- The Docker Tomcat images were previously based on OpenJDK images which used Debian as the underlying OS. The OpenJDK Debian images have been [discontinued for Java 8 and Java 11](https://github.com/docker-library/tomcat/issues/262) so the next best match in the Docker Tomcat images are now the Ubuntu Jammy (22.04 LTS) and Focal (20.04 LTS) images using the OpenJDK baed Temurin Java distributions.
- The Docker Tomcat images [removed support for Alpine](https://github.com/docker-library/tomcat/issues/166) and so the Lucee `-alpine` variant can no longer be supported. If the Tomcat base images add support for Alpine in the future then we will look to support the `-alpine` variant again.


## Example Project Dockerfile

For the latest stable release with Tomcat only:

```
FROM lucee/lucee:6.0

COPY config/lucee/ /opt/lucee/web/
COPY www /var/www
```

For the latest stable release with NGINX and Tomcat:

```
FROM lucee/lucee:6.0-nginx

COPY config/nginx/ /etc/nginx/
COPY config/lucee/ /opt/lucee/web/
COPY www /var/www
```

More examples [here](https://github.com/lucee/lucee-docs/tree/master/examples/docker)


## Features

### Java optimisation tweaks

- JVM is set to [use `/dev/urandom` as an entropy source for secure random numbers](http://support.run.pivotal.io/entries/59869725-Java-Web-Applications-Slow-Startup-or-Failing) to avoid blocking Tomcat on startup.

- Tomcat is configured to [skip the default scanning of Jar files on startup](http://www.gpickin.com/index.cfm/blog/how-to-get-your-tomcat-to-pounce-on-startup-not-crawl), significantly improving startup time.

### Optimised for single-site application

The default configuration serves a single application for any hostname on the listening port. Multiple applications can be supported by editing the server.xml in the Tomcat config.

Lucee 6 by default runs in single mode (only one configuration and Administrator), if you prefer to run it in multi mode you need to to set the flag "mode" to "multi" in the of the .CFConfig.json file.

## Using this image

### Accessing the service

Lucee server's Tomcat installation listens on port 8888.

This base image exposes port 8080 to linked containers but its **not used**. You must publish or expose port 8888 if you wish to access Tomcat from your installation.

### Accessing the Lucee Admin

The Lucee Admin URL is `/lucee/admin/` from the exposed port. With Lucee 5.4.6 (and above), 6.0.2 (and above) and 6.1 (and above),
you can set the password with the environment variable `LUCEE_ADMIN_PASSWORD=qwerty` or the system property `-Dlucee.admin.password=123456`.

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

Following some helpful Environment variables you can use with the Lucee docker image.

- `LUCEE_ADMIN_PASSWORD`: The password for the Lucee Administrator
- `LUCEE_VERSION`: If set Lucee will run this version independent of the version installed.
- `LUCEE_JAVA_OPTS`: Additional JVM parameters for Tomcat. Used by /usr/local/tomcat/bin/setenv.sh. Default: "-Xms64m -Xmx512m".

For all possible enviroment variables supported by Lucee, see [here](https://github.com/lucee/lucee-docs/blob/master/docs/recipes/environment-variables-system-properties.md).


## How to locally develop Lucee Docker builds

Developing and testing builds locally requires a Docker environment with buildx support and Python 3 installed. Run `pip3 install -r requirements.txt`
to install the required dependencies.

To build and test specific verions set environment variables for the Tomcat and Lucee verions that are to be used, e.g.

```
export TOMCAT_VERSION=9.0
export TOMCAT_JAVA_VERSION=jre11-temurin-jammy
export TOMCAT_BASE_IMAGE=
export LUCEE_MINOR=5.4
export LUCEE_SERVER=,-nginx
export LUCEE_VARIANTS=

export LUCEE_VERSION=5.4.4.38
```

Then use the default builder with buildx and run the `build-images` script using a single target platform only (matching your native platform), e.g.
```
docker buildx use default
./build-images.py --no-push --buildx-load --buildx-platform linux/amd64
```

Specify the newly built image tag in a Docker Compose file to run and test the container image with `docker-compose up`;
```
lucee:
  image: lucee/lucee:5.4.4.38
  ports: 
    - "8854:8888"
    - "8054:80"
```

You can also find examples that show you how to for example add your own configuration or custom extensions [here](https://github.com/lucee/lucee-docs/tree/master/examples/docker)

### Advanced build changes

If adding new Tomcat base (OS) images, Tomcat versions, Java versions, or Lucee versions or variants, the matrix.yaml needs to be edited so that several features
like the tag building/lookups will work. After modifying the matrix.yaml run the script `./generate-matrix.py` to generate the new Travis configuration (note: Travis CI is deprecated as builds have transitioned to GitHub Actions, however this part of the build hasn't been fully removed yet).

## Older Lucee Base Images

The older versions of Lucee remain available as tags in the `lucee/lucee` Docker Hub repository. Listed are the newest releases for each minor version.

Lucee 5.3.x - Tomcat 9.0 with Java 11

- `5.3.12.1-tomcat9.0-jre11-temurin-jammy`, `5.3.12.1`, **`5.3`** ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile))
  - `5.3.12.1-nginx-tomcat9.0-jre11-temurin-jammy`, `5.3.12.1-nginx`, **`5.3-nginx`** ([Dockerfile.nginx](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile.nginx))

Lucee 5.2.x - Tomcat 9.0 with Java 11

- `5.2.9.31-tomcat9.0-jre11`, `5.2.9.31`, **`5.2`** ([Dockerfile](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile))
  - `5.2.9.31-nginx-tomcat9.0-jre11`, `5.2.9.31-nginx`, **`5.2-nginx`** ([Dockerfile.nginx](https://github.com/lucee/lucee-dockerfiles/blob/master/Dockerfile.nginx))


## Legacy Lucee Base Images

The legacy Lucee Base Images / repositories will remain available for the projects that are using them, though the build process for those images is considered "legacy" as they have been superseded by the new build matrix builds.

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

The [Lucee Dockerfiles project](https://github.com/lucee/lucee-dockerfiles) is maintained by the community. Chief protagonist is @justincarter ([Justin Carter](https://github.com/justincarter) of [Daemon](http://www.daemon.com.au)). Bug reports and pull requests are most welcome.

Special thanks to @rye ([Kristofer Rye](https://github.com/rye)) and @hawkrives ([Hawken Rives](https://github.com/hawkrives)) for their work on the Travis build matrix.


# License

The Docker files and config files are available under the [MIT License](LICENSE). The Lucee engine, Tomcat, NGINX and any other softwares are available under their respective licenses.
