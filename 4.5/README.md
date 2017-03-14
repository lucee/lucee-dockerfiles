# Lucee 4.5 on Tomcat (JAR deployment)

[![](https://images.microbadger.com/badges/image/lucee/lucee4.svg)](https://microbadger.com/images/lucee/lucee4)

[Lucee](http://www.lucee.org/)  application engine running on [Apache Tomcat](https://tomcat.apache.org/) J2EE application server

Latest [Docker images tagged](https://registry.hub.docker.com/u/lucee/lucee-tomcat/tags/manage/) as `latest` on Docker Hub; specific versions of Lucee are tagged with the corresponding version number.

For latest:
```
FROM lucee/lucee4:latest
```

For a specific version:
```
FROM lucee/lucee4:4.5.1.024
```

_Consider using the compound container with NGINX and Tomcat pre-installed and configured._

```
FROM lucee/lucee4-nginx:4.5.1.024
```


## Features

### Java optisation tweaks

- Lucee 4's [Java Agent](http://blog.getrailo.com/post.cfm/railo-4-1-smarter-template-compilation) is enabled for better memory management of compiled CFML code.

- JVM is set to [use /dev/urandom as an entropy source for secure random numbers](http://support.run.pivotal.io/entries/59869725-Java-Web-Applications-Slow-Startup-or-Failing) to avoid blocking Tomcat on startup.

- Tomcat is configured to [skip the default scanning of Jar files on startup](http://www.gpickin.com/index.cfm/blog/how-to-get-your-tomcat-to-pounce-on-startup-not-crawl), significantly improving startup time.

### Optimised for single-site application

The default configuration serves a single application for any hostname on the listening port. Multiple applications can be supported by editing the server.xml in the Tomcat config.

### Session management

The default session type in Lucee is "cfml". This often causes issues for Lucee servers running in Docker containers. If you use CFML sessions you should set the session type to "j2ee" in a Lucee configuration file or Application.cfc.

## Using this image

### Accessing the service

The default configuration has Tomcat listening on port 8080 in the container. However, Lucee server's Tomcat installation is on port 8888.

This base image exposes port 8080 to linked containers but its **not used**.You must publish or expose port 8888 if you wish to access Tomcat from your installation.

### Accessing the Web admin

The Lucee admin URL is `/lucee/admin/` from the exposed port. No admin passwords are set.

**THIS IS NOT A SECURE CONFIGURATION FOR PRODUCTION ENVIRONMENTS!** It is **strongly** recommended that you secure the container by:

- Changing the server password
- Using IP or URL filtering to restrict access to the Lucee web admin
- Following recommended security practices such as the [Lucee Lockdown Guide](https://bitbucket.org/lucee/lucee/wiki/tips_and_tricks_Lockdown_Guide)

### Sample CFML page

The default webroot contains a simple "Hello world" index.cfm file which dumps the CFML server scope. This can be replaced with your own CFML code and assets in derived images.

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

`LUCEE_JAVA_OPTS`: Additional JVM parameters for Tomcat. Used by /usr/local/tomcat/bin/setenv.sh. Default: "-Xms256m -Xmx512m".

### Examples

#### Persisting Logs

Stash your logs wherever you like, but these examples use the following directory, which we'll create as follows:

```bash
mkdir -p /var/log/lucee/tomcat
```

Either of the following examples should yield a Hello World page at http://192.168.99.100:8888/.

#### Docker Compose Option

Docker Compose file:

```yaml
# docker-compose.yml
lucee50:
  image: lucee/lucee4:latest
  ports: 
   - "8888:8888"
  volumes:
   - /var/log/lucee:/opt/lucee/server/lucee-server/context/logs
   - /var/log/lucee/tomcat:/usr/local/tomcat/logs
```

Running `docker-compose`:

```bash
cd /path/to/dir/containing/docker-compose.yml
docker-compose up -d
```

#### Docker Run Option

Executing `docker run`:

```bash
docker run -d \
 -p 8888:8888 \
 -v "/var/log/lucee:/opt/lucee/server/lucee-server/context/logs" \
 -v "/var/log/lucee/tomcat:/usr/local/tomcat/logs" \
 lucee/lucee4:latest
```
