#!/bin/bash
# Script to upgrade Oracle MAX_STRING_SIZE to EXTENDED

echo "Starting MAX_STRING_SIZE migration..."

sqlplus / as sysdba <<EOF
-- 1. Shutdown and restart in UPGRADE mode
SHUTDOWN IMMEDIATE;
STARTUP UPGRADE;

-- 2. Change the parameter
ALTER SYSTEM SET max_string_size=EXTENDED SCOPE=SPFILE;

-- 3. Run the mandatory migration script
-- Note: This can take some time depending on your DB size
@?/rdbms/admin/utl32k.sql

-- 4. Restart the database normally to apply changes
SHUTDOWN IMMEDIATE;
STARTUP;

-- 5. Recompile invalid objects (standard practice after utl32k)
@?/rdbms/admin/utlrp.sql

SELECT name, value FROM v\$parameter WHERE name = 'max_string_size';
EXIT;
EOF

echo "Migration complete. Check the output above for confirmation."
