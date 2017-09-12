FROM lucee/lucee52:latest

MAINTAINER Daemonites <hello@daemon.com.au>

# Install nginx and supervisord
COPY nginx_signing.key /tmp/nginx_signing.key
RUN apt-key add /tmp/nginx_signing.key
RUN echo "deb http://nginx.org/packages/debian/ stretch nginx" >> /etc/apt/sources.list
RUN set -x && \
	apt-get update && \
	apt-get install --no-install-recommends --no-install-suggests -y \
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
