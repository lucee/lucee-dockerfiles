# Dockerfiles for Lucee application servers

This repository contains Dockerfiles to build Lucee application servers.

Lucee Docker images are available on Docker Hub: https://hub.docker.com/u/lucee/

## Lucee Base Images

Lucee provides a number of different base images for your Lucee project.  For an example of setting up a Lucee Docker project see [Lucee Docker Workbench](https://github.com/modius/lucee-docker-workbench).

### Lucee 4 with Tomcat/NGINX `lucee/lucee4-nginx`

[README, Dockerfile and associated assets.](./lucee-nginx/4.5/README.md)

```
FROM lucee/lucee4-nginx:latest
```

Stable releases of Lucee 4.5+ on Tomcat 8 JRE8 combined with an integrated NGINX web server. [Available Tags](https://hub.docker.com/r/lucee/lucee4-nginx/tags/)

### Lucee 4 with Tomcat `lucee/lucee4`

[README, Dockerfile and associated assets.](./4.5/README.md)

```
FROM lucee/lucee4:latest
```

Stable releases of Lucee 4.5+ on Tomcat 8 JRE8. [Available Tags](https://hub.docker.com/r/lucee/lucee4/tags/)

### Lucee 5 with Tomcat/NGINX `lucee/lucee5-nginx`

[README, Dockerfile and associated assets.](./lucee-nginx/5.0/README.md)

```
FROM lucee/lucee5-nginx:latest
```

BETA releases of Lucee 5 "Velvet" on Tomcat 8 JRE8 combined with an integrated NGINX web server. [Available Tags](https://hub.docker.com/r/lucee/lucee5-nginx/tags/)

### Lucee 5 with Tomcat `lucee/lucee5`

[README, Dockerfile and associated assets.](./5.0/README.md)

```
FROM lucee/lucee5:latest
```

BETA releases of Lucee 5 "Velvet" on Tomcat 8 JRE8. [Available Tags](https://hub.docker.com/r/lucee/lucee5/tags/)


## Example Project Dockerfile

**Example FarCry application from [Chelsea Docker](https://github.com/modius/chelsea-docker)**
```
FROM lucee/lucee4-nginx:latest

MAINTAINER Geoff Bowers <modius@daemon.com.au>

# TOMCAT CONFIGS
# COPY catalina.properties server.xml web.xml /usr/local/tomcat/conf/
# Custom setenv.sh to load Lucee
# COPY setenv.sh /usr/local/tomcat/bin/

# NGINX configs
COPY config/nginx/ /etc/nginx/
# Lucee server configs
COPY config/lucee/ /opt/lucee/web/
# Deploy codebase to container
COPY code /var/www/farcry
```


## Features

### Java optimisation tweaks

- Lucee 4's [Java Agent](http://blog.getrailo.com/post.cfm/railo-4-1-smarter-template-compilation) is enabled for better memory management of compiled CFML code.

- JVM is set to [use /dev/urandom as an entropy source for secure random numbers](http://support.run.pivotal.io/entries/59869725-Java-Web-Applications-Slow-Startup-or-Failing) to avoid blocking Tomcat on startup.

- Tomcat is configured to [skip the default scanning of Jar files on startup](http://www.gpickin.com/index.cfm/blog/how-to-get-your-tomcat-to-pounce-on-startup-not-crawl), significantly improving startup time.

### Optimised for single-site application

The default configuration serves a single application for any hostname on the listening port. Multiple applications can be supported by editing the `server.xml` in the Tomcat config.


## Contributing to this Project

The Lucee Dockerfiles project is maintained by the community. Chief protagonist is @modius ([Geoff Bowers](https://github.com/modius) of [Daemon](http://www.daemon.com.au)). Bug reports and pull requests are most welcome.

### Spinning things up locally

Using the [Daemon Docker Workbench](https://github.com/Daemonite/workbench) provided, or using your own Docker tooling.

These instructions assume you have the parent Workbench up and running:
```
git clone git@github.com:lucee/lucee-dockerfiles.git
cd lucee-dockerfiles
docker-compose up
```

You don't have to bring up all the images in one fell swoop; for example, `vagrant up lucee50` to just build Lucee 5.0.

Containers are forwarded onto the following addresses:
```
lucee45 -> $ open http://workbench.192.168.99.100.xip.io:8045/
lucee50 -> $ open http://workbench.192.168.99.100.xip.io:8050/
nginx45 -> $ open http://nginx45.192.168.99.100.xip.io
nginx50 -> $ open http://nginx50.192.168.99.100.xip.io
```


## License

The Docker files and config files are available under the [MIT License](LICENSE). The Lucee engine, Tomcat, NGINX and any other softwares are available under their respective licenses.
