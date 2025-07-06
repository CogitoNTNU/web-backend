#!/bin/bash

# Variables
DUMP_FILE_NAME="$1"
# Check if dump file is provided
if [ -z "$DUMP_FILE_NAME" ]; then
  echo "Usage: ./restore-databse.sh name_of_dump_file.sql"
  exit 1
fi

BACKUP_DIR="./backups"
DUMP_FILE="$BACKUP_DIR/$DUMP_FILE_NAME"

# Check if dump file exists
if [ ! -f "$DUMP_FILE" ]; then
  echo "File not found: $DUMP_FILE"
  exit 1
fi

# Restore the dump
docker exec -i cogito_db psql -U cogitouser -d cogitodb < $DUMP_FILE

echo "Restore completed from: $DUMP_FILE to cogito_db"

# Display the database tables
echo "Database tables:"
docker exec -it cogito_db psql -U cogitouser -d cogitodb -c "\dt"