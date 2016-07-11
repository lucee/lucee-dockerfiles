# Dockerfile for nginx on Lucee/Tomcat8-jre8
FROM lucee/lucee5:latest

MAINTAINER Geoff Bowers <modius@daemon.com.au>

# Install nginx and supervisord
RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
RUN echo "deb http://nginx.org/packages/debian/ jessie nginx" >> /etc/apt/sources.list
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y \
		nginx \
		supervisor && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy default nginx config files
COPY nginx.conf /etc/nginx/
COPY default.conf /etc/nginx/conf.d/

# Copy supervisord.conf
COPY supervisord.conf /etc/supervisor/conf.d/

# Provide test page
RUN mkdir -p /var/www
COPY index.cfm /var/www/
ONBUILD RUN rm -rf /var/www/*

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Write the Nginx logs out - COMMENT OUT WHEN NEEDED though they can create a lot of noise
#RUN ln -sf /dev/stdout /var/log/nginx/access.log
#RUN ln -sf /dev/stderr /var/log/nginx/error.log

# Write the Lucee logs to stdout
# As these files don't exists until later we'll use "touch" to create them
RUN mkdir -p /opt/lucee/web/logs
RUN touch /opt/lucee/web/logs/application.log
RUN ln -sf /dev/stdout /opt/lucee/web/logs/application.log

RUN touch /opt/lucee/web/logs/exception.log
RUN ln -sf /dev/stderr /opt/lucee/web/logs/exception.log

RUN touch /opt/lucee/web/logs/orm.log
RUN ln -sf /dev/stdout /opt/lucee/web/logs/orm.log

RUN touch /opt/lucee/web/logs/mail.log
RUN ln -sf /dev/stdout /opt/lucee/web/logs/mail.log

# Engage
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
