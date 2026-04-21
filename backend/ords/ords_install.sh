#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Environment variables from Dockerfile/docker-compose.yaml
ORDS_HOME="/opt/ords"
ORDS_CONFIG_DIR="/opt/ords_config"
CATALINA_HOME="/usr/local/tomcat"

# File to check for existing ORDS configuration
CONFIG_CHECK_FILE="${ORDS_CONFIG_DIR}/config/ords/defaults.xml"


    # Write a temporary properties file for silent installation
    cat > /tmp/ords_params.properties <<- EOF
db.hostname=${DB_HOSTNAME}
db.port=${DB_PORT}
db.servicename=${DB_SERVICE}
db.username=SYS
db.password=${DB_PASSWORD}
ords.public.user.password=${ORDS_PUBLIC_PASSWORD}
feature.sdw=true
feature.rest=true
feature.soda=true
rest.services.apex.add=true
EOF

if [ ! -f "$CONFIG_CHECK_FILE" ]; then
  echo "ORDS configuration not found. Starting initial installation..."

  MAX_ATTEMPTS=20
  ATTEMPT_NUM=1
  DB_STATUS=1

  echo "Waiting for Oracle Database at ${DB_HOSTNAME}:${DB_PORT} Service: ${DB_SERVICE}..."

  MAX_ATTEMPTS=40  # Increase attempts to allow up to 10 minutes of waiting
    ATTEMPT_NUM=1
    DB_STATUS=1

    echo "Waiting for Oracle Database at ${DB_HOSTNAME}:${DB_PORT} Service: ${DB_SERVICE}..."
    
    while [ $DB_STATUS -ne 0 ] && [ $ATTEMPT_NUM -le $MAX_ATTEMPTS ]; do
        echo "Attempt $ATTEMPT_NUM of $MAX_ATTEMPTS: Running 'ords validate'..."
        
        # Use the most robust user: PDBADMIN
        ( printf "${DB_PASSWORD}\n" | /usr/local/bin/ords --config ${ORDS_CONFIG_DIR} validate \
          --db-hostname "${DB_HOSTNAME}" --db-port "${DB_PORT}" \
          --db-servicename "${DB_SERVICE}" --admin-user PDBADMIN --password-stdin )
        
        DB_STATUS=$?
        
        if [ $DB_STATUS -ne 0 ]; then
            echo "Validation failed (Code $DB_STATUS, ORA-01017 likely). Waiting 15 seconds..."
            sleep 15  # Pause for 15 seconds
        fi
        ATTEMPT_NUM=$((ATTEMPT_NUM + 1))
    done

    # 2. Execute the fully non-interactive install using direct flags and stdin

    # The command is structured to pipe two passwords: 
    # The first password is for the --admin-user (SYS), 
    # the second is for the --proxy-user (ORDS_PUBLIC_USER).

    # (
    #   printf "${DB_PASSWORD}\n${ORDS_PUBLIC_PASSWORD}"
    #   ) | /usr/local/bin/ords --config ${ORDS_CONFIG_DIR} install \
    #     --admin-user PDBADMIN \
    #     --password-stdin \
    #     --db-hostname "${DB_HOSTNAME}" \
    #     --db-port "${DB_PORT}" \
    #     --db-servicename "${DB_SERVICE}" \
    #     --feature-sdw true \
    #     --proxy-user \
    #     --log-folder ${ORDS_CONFIG_DIR}/logs

      echo "ORDS installation complete."
    else
      echo "ORDS configuration found. Skipping installation."
fi

# --- DEPLOYMENT STEP ---
# The ords.war file is inside the ORDS_HOME. We copy it to the Tomcat webapps directory.
echo "Deploying ords.war to Tomcat webapps..."
cp "${ORDS_HOME}/ords.war" "${CATALINA_HOME}/webapps/"

# If deploying as a specific root path (e.g., /ords), you can rename it:
# cp "${ORDS_HOME}/ords.war" "${CATALINA_HOME}/webapps/ords.war"
# The default Tomcat will deploy it to the root context by default if named 'ROOT.war',
# but using 'ords.war' is clearer and deploys to the /ords context path.

echo "Deployment complete. Starting Tomcat server."

# Execute the main command passed to the container (the original Tomcat CMD)
exec "$@"
