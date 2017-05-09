FROM lucee/lucee52:latest

MAINTAINER Daemonites <hello@daemon.com.au>

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

# Engage
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
