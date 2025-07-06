#!/bin/bash

# Variables
CREDENTIALS=$1

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y-%m-%d_%H_%M_%S)
DUMP_FILE="$BACKUP_DIR/dump_$TIMESTAMP.sql"


# Perform the backup
mkdir -p $BACKUP_DIR
docker exec -t cogito_db pg_dumpall -c -U cogitouser > $DUMP_FILE

echo "Backup completed: $DUMP_FILE"

# Display the first 3 lines of the dump file
head -n 3 $DUMP_FILE

# Send backup
if [[ -n "$CREDENTIALS" ]]; then
    curl -k -T $DUMP_FILE -u "$CREDENTIALS" -H 'X-Requested-With: XMLHttpRequest' https://nextcloud.eduardp.com/public.php/webdav/$DUMP_FILE
else
    echo "No credentials provided, skipping upload."
fi