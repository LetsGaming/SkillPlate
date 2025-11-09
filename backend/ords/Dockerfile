# Start with the AL2 base image (tomcat:9.0.111-jdk8-corretto-al2)
FROM tomcat:9.0.111-jdk21-corretto-al2 

# Set environment variables
ENV ORDS_HOME="/opt/ords"
ENV ORDS_CONFIG_DIR="/opt/ords_config"
ENV ORDS_DOWNLOAD_URL="https://download.oracle.com/otn_software/java/ords/ords-latest.zip"
# Tomcat's home directory is /usr/local/tomcat
ENV CATALINA_HOME="/usr/local/tomcat"

# 1. Install necessary packages using YUM (the AL2 package manager)
# 2. Create the ORDS user/group
# 3. Create the ORDS configuration directories
RUN yum update -y && \
    yum install -y bash curl unzip shadow-utils openssl && \
    groupadd -r ords && \
    useradd -r -g ords ords && \
    mkdir -p ${ORDS_HOME} ${ORDS_CONFIG_DIR}/logs && \
    chown -R ords:ords ${ORDS_HOME} ${ORDS_CONFIG_DIR} && \
    yum clean all 

# 4. Download and Extract ORDS
RUN set -x && \
    # Download the latest ORDS zip
    curl -L -o /tmp/ords.zip ${ORDS_DOWNLOAD_URL} && \
    # Unzip ORDS into its home directory
    unzip -q /tmp/ords.zip -d ${ORDS_HOME} && \
    rm /tmp/ords.zip && \
    # Link the ords executable
    ln -s ${ORDS_HOME}/bin/ords /usr/local/bin/ords

# 5. Copy configuration script and make it executable
COPY ords_install.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/ords_install.sh

# 6. Change ownership of ORDS files
RUN chown -R ords:ords ${ORDS_HOME}

# Use the 'root' user for the initial command to call our script,
# which runs before Tomcat's default entrypoint.
# The original Tomcat ENTRYPOINT/CMD will start the server.
ENTRYPOINT ["/usr/local/bin/ords_install.sh"]
CMD ["catalina.sh", "run"]
