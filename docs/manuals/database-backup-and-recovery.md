# Database Backup and Recovery Guide

This guide explains how to **back up** and **restore** the PostgreSQL database for the Cogito backend using the provided scripts.

---

## Prerequisites

- Docker and Docker Compose installed.
- The PostgreSQL database container (`cogito_db`) running (start with `docker compose up --build` if not).
- Backup and restore scripts located in the `scripts/` directory.

---

## Backing Up the Database
The backup process creates a SQL dump of the entire database, which can be used to restore the database later. If one provides the credentials, the backup will be uploaded to an external storage service.

1. **Run the Backup Script**

    Use the provided script to create a backup of the database:

    ```bash
    ./scripts/backup-database.sh
    ```

    By default, this will create a local backup.  
    To upload the backup to external storage, provide your credentials after the command:

    ```bash
    ./scripts/backup-database.sh <your-credentials>
    ```

    Replace `<your-credentials>` with your actual storage service credentials.



   This will:
   - Create a timestamped `.sql` dump file in the `backups/` directory.
   - Use the running `cogito_db` container and the configured database credentials.

2. **Verify the Backup**

   Check the `backups/` directory for a new file named like `dump_YYYY-MM-DD_HH_MM_SS.sql`.

---

## Restoring the Database

1. **Place the Backup File**

   Ensure your backup SQL file (e.g., `dump_2025-07-06_16_53_10.sql`) is in the `backups/` directory at the project root.

2. **Run the Restore Script**

   Use the provided script to restore the database:

   ```bash
   ./scripts/restore-databse.sh dump_2025-07-06_16_53_10.sql
   ```

   Replace `dump_2025-07-06_16_53_10.sql` with the name of your backup file.

   The script will:
   - Check if the backup file exists.
   - Restore the dump into the running `cogito_db` container.
   - Display the tables in the restored database.

3. **Verify the Restore**

   After the script completes, you should see a list of tables in the database. You can also connect to the database manually for further verification:

   ```bash
   docker exec -it cogito_db psql -U cogitouser -d cogitodb
   ```

---

## Troubleshooting

- **File Not Found:**  
  If you see `File not found: ./backups/<your_file>.sql`, ensure the file exists and the name is correct.

- **Database Container Not Running:**  
  If you get connection errors, make sure the `cogito_db` container is running:
  ```bash
  docker compose up -d
  ```

## See Also
- [Docker Manual](docker.md)