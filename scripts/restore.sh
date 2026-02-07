#!/bin/bash

# VK Content Workflow - Database Restore Script
# This script restores PostgreSQL database from backup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check arguments
if [ $# -eq 0 ]; then
    log_error "Usage: $0 <backup_file>"
    log_info "Example: $0 /backups/vk_content_20260207_120000.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    log_error "Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Database connection (from environment variables)
PGHOST="${PGHOST:-postgres}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-postgres}"
PGDATABASE="${PGDATABASE:-vk_content}"

# Check if PostgreSQL is accessible
log_info "Checking PostgreSQL connection..."
if ! pg_isready -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" > /dev/null 2>&1; then
    log_error "Cannot connect to PostgreSQL at $PGHOST:$PGPORT"
    exit 1
fi

log_info "PostgreSQL is accessible"

# Confirmation prompt
log_warn "⚠️  WARNING: This will replace all data in database '$PGDATABASE'"
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    log_info "Restore cancelled"
    exit 0
fi

# Create backup of current database before restore
TEMP_BACKUP="/tmp/vk_content_before_restore_$(date +%Y%m%d_%H%M%S).sql"
log_info "Creating safety backup of current database..."
pg_dump -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" > "$TEMP_BACKUP"
log_info "Safety backup created: $TEMP_BACKUP"

# Decompress if needed
if [[ "$BACKUP_FILE" == *.gz ]]; then
    log_info "Decompressing backup file..."
    TEMP_SQL="/tmp/$(basename ${BACKUP_FILE%.gz})"
    gunzip -c "$BACKUP_FILE" > "$TEMP_SQL"
    SQL_FILE="$TEMP_SQL"
else
    SQL_FILE="$BACKUP_FILE"
fi

# Drop existing connections
log_info "Terminating existing connections to database..."
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d postgres -c \
    "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$PGDATABASE' AND pid <> pg_backend_pid();" \
    > /dev/null 2>&1 || true

# Restore database
log_info "Restoring database from: $BACKUP_FILE"
if psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" < "$SQL_FILE"; then
    log_info "Database restored successfully!"
else
    log_error "Failed to restore database"
    log_warn "You can restore from safety backup: $TEMP_BACKUP"
    exit 1
fi

# Cleanup temporary file
if [ -n "$TEMP_SQL" ] && [ -f "$TEMP_SQL" ]; then
    rm "$TEMP_SQL"
    log_info "Temporary file cleaned up"
fi

# Verify restore
log_info "Verifying restore..."
POSTS_COUNT=$(psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -t -c "SELECT COUNT(*) FROM vk_posts;" | tr -d ' ')
log_info "Posts in database: $POSTS_COUNT"

# Remove safety backup if restore was successful
read -p "Remove safety backup? (yes/no): " REMOVE_BACKUP
if [ "$REMOVE_BACKUP" == "yes" ]; then
    rm "$TEMP_BACKUP"
    log_info "Safety backup removed"
else
    log_info "Safety backup kept: $TEMP_BACKUP"
fi

log_info "Restore completed successfully!"

exit 0
