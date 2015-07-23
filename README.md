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

These images are supported by the Lucee community however they are provided with no warranty.

## Vagrant Workbench

You can build images locally using the Vagrant workbench provided, or using your own Docker tooling.

Workbench assumes: Virtualbox, `git v1.6.5`, `vagrant v1.7.3`

```
git clone git@github.com:lucee/lucee-dockerfiles.git
cd lucee-dockerfiles
vagrant up dockerhost
vagrant up lucee45 lucee50 nginx45 nginx50
```
You don't have to bring up all the images in one fell swoop; for example, `vagrant up lucee50` to just build Lucee 5.0.

Containers are forwarded onto the following ports:
```
lucee45 -> $ open http://localhost:8001/
lucee50 -> $ open http://localhost:8002/
nginx45 -> $ open http://localhost:8003/
nginx45 -> $ open http://localhost:8004/
```

## License

The Docker files and config files are available under the [MIT License](LICENSE). The Lucee engine, Tomcat, NGINX and any other softwares are available under their respective licenses.