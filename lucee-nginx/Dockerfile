# Dockerfile for nginx on Lucee/Tomcat

FROM boomfish/lucee-tomcat:4.5

MAINTAINER Dennis Clark <boomfish@gmail.com>

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
RUN echo "deb http://nginx.org/packages/debian/ jessie nginx" >> /etc/apt/sources.list

# Install nginx and supervisord
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y \
		nginx \
		supervisor && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy nginx config files
COPY nginx.conf /etc/nginx/
COPY default.conf /etc/nginx/conf.d/

# Copy supervisord.conf
COPY supervisord.conf /etc/supervisor/conf.d/

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]

# Expose HTTP and HTTPS ports
EXPOSE 80 443
