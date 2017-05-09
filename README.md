# Dockerfiles for Lucee application servers

Dockerfiles to build Lucee application servers.; used for the official LAS Lucee Docker images.

Lucee Docker images are available on Docker Hub: https://hub.docker.com/u/lucee/

## Lucee Base Images

Lucee provides a number of different base images for your Lucee project.

### Lucee 5.2

- [nginx + Tomcat 8.0-JRE8](./lucee-nginx/5.2/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee52-nginx.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee52-nginx/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee52-nginx.svg)](https://microbadger.com/images/lucee/lucee52-nginx)
- [Tomcat 8.0-JRE8](./5.2/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee52.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee52/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee52.svg)](https://microbadger.com/images/lucee/lucee52)

### Lucee 5.1

- [nginx + Tomcat 8.0-JRE8](./lucee-nginx/5.1/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee51-nginx.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee51-nginx/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee51-nginx.svg)](https://microbadger.com/images/lucee/lucee51-nginx)
- [Tomcat 8.0-JRE8](./5.1/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee51.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee51/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee51.svg)](https://microbadger.com/images/lucee/lucee51)

### Lucee 5.0

- [nginx + Tomcat 8.0-JRE8](./lucee-nginx/5.0/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee5-nginx.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee5-nginx/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee5-nginx.svg)](https://microbadger.com/images/lucee/lucee5-nginx)
- [Tomcat 8.0-JRE8](./5.0/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee5.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee5/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee5.svg)](https://microbadger.com/images/lucee/lucee5)

### Lucee 4.5

- [nginx + Tomcat 8.0-JRE8](./lucee-nginx/4.5/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee4-nginx.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee4-nginx/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee4-nginx.svg)](https://microbadger.com/images/lucee/lucee4-nginx)
- [Tomcat 8.0-JRE8](./4.5/) &nbsp; &nbsp;
  [![docker pulls](https://img.shields.io/docker/pulls/lucee/lucee4.svg?label=docker+pulls)](https://hub.docker.com/r/lucee/lucee4/)
  [![](https://images.microbadger.com/badges/image/lucee/lucee4.svg)](https://microbadger.com/images/lucee/lucee4)


## Example Project Dockerfile

```
FROM lucee/lucee51-nginx:latest

# NGINX configs
COPY config/nginx/ /etc/nginx/
# Lucee server configs
COPY config/lucee/ /opt/lucee/web/
# Deploy codebase to container
COPY www /var/www
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

Using the [Daemon Docker Workbench](https://github.com/justincarter/docker-workbench) provided, or using your own Docker tooling.

These instructions assume you have the parent Workbench up and running:
```
git clone git@github.com:lucee/lucee-dockerfiles.git
cd lucee-dockerfiles
docker-compose up
```

Containers are forwarded onto the following addresses:
```
lucee45 -> $ open http://lucee-dockerfiles.192.168.99.100.nip.io:8045
lucee50 -> $ open http://lucee-dockerfiles.192.168.99.100.nip.io:8050
lucee51 -> $ open http://lucee-dockerfiles.192.168.99.100.nip.io:8051
lucee52 -> $ open http://lucee-dockerfiles.192.168.99.100.nip.io:8052
nginx45 -> $ open http://nginx45.192.168.99.100.nip.io
nginx50 -> $ open http://nginx50.192.168.99.100.nip.io
nginx51 -> $ open http://nginx51.192.168.99.100.nip.io
nginx52 -> $ open http://nginx52.192.168.99.100.nip.io
```

## License

The Docker files and config files are available under the [MIT License](LICENSE). The Lucee engine, Tomcat, NGINX and any other softwares are available under their respective licenses.
