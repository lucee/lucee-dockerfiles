ARG LUCEE_IMAGE

FROM ${LUCEE_IMAGE}

# Install nginx and supervisord
COPY nginx/nginx_signing.key /tmp/nginx_signing.key
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
COPY nginx/nginx.conf /etc/nginx/
COPY nginx/default.conf /etc/nginx/conf.d/

# Copy supervisord.conf
COPY nginx/supervisord.conf /etc/supervisor/conf.d/

# Provide test page
RUN mkdir -p /var/www
COPY supporting/index.cfm /var/www/
ONBUILD RUN rm -rf /var/www/*

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Engage
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
