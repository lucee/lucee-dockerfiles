# Dockerfiles for Lucee application servers

This repository contains Dockerfiles to build Lucee application servers.

Docker images are available on Docker Hub:

- https://registry.hub.docker.com/repos/lucee/

## Features

### Java optisation tweaks

- Lucee 4's [Java Agent](http://blog.getrailo.com/post.cfm/railo-4-1-smarter-template-compilation) is enabled for better memory management of compiled CFML code.

- JVM is set to [use /dev/urandom as an entropy source for secure random numbers](http://support.run.pivotal.io/entries/59869725-Java-Web-Applications-Slow-Startup-or-Failing) to avoid blocking Tomcat on startup.

- Tomcat is configured to [skip the default scanning of Jar files on startup](http://www.gpickin.com/index.cfm/blog/how-to-get-your-tomcat-to-pounce-on-startup-not-crawl), significantly improving startup time.

### Optimised for single-site application

The default configuration serves a single application for any hostname on the listening port. Multiple applications can be supported by editing the `server.xml` in the Tomcat config.


## Details on Docker images

- [Lucee on Tomcat](lucee-tomcat/README.md)
- [Lucee on Tomcat with nginx](lucee-nginx/README.md)

## Prebuilt images on Docker Hub registry

Prebuilt Docker images are available on [Docker Hub](https://registry.hub.docker.com/repos/lucee/). These images are are created via [automated builds](https://docs.docker.com/docker-hub/builds/).

These images are not 'trusted' and are provided with no warranty.

## License

The Docker files and config files are available under the [MIT License](LICENSE). The Lucee engine, Tomcat, NGINX and any other softwares are available under their respective licenses.