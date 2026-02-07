#!/bin/bash

# VK Content Workflow - Database Backup Script
# This script creates automated backups of the PostgreSQL database

set -e

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/vk_content_$DATE.sql"

# Database connection (from environment variables)
PGHOST="${PGHOST:-postgres}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-postgres}"
PGDATABASE="${PGDATABASE:-vk_content}"

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

# Create backup directory if not exists
if [ ! -d "$BACKUP_DIR" ]; then
    log_info "Creating backup directory: $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
fi

# Check if PostgreSQL is accessible
log_info "Checking PostgreSQL connection..."
if ! pg_isready -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" > /dev/null 2>&1; then
    log_error "Cannot connect to PostgreSQL at $PGHOST:$PGPORT"
    exit 1
fi

log_info "PostgreSQL is accessible"

# Create backup
log_info "Creating backup: $BACKUP_FILE"
if pg_dump -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" > "$BACKUP_FILE"; then
    log_info "Backup created successfully"
else
    log_error "Failed to create backup"
    exit 1
fi

# Compress backup
log_info "Compressing backup..."
if gzip "$BACKUP_FILE"; then
    log_info "Backup compressed: $BACKUP_FILE.gz"
    BACKUP_FILE="$BACKUP_FILE.gz"
else
    log_warn "Failed to compress backup, keeping uncompressed"
fi

# Get backup size
BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
log_info "Backup size: $BACKUP_SIZE"

# Clean old backups
log_info "Cleaning old backups (older than $RETENTION_DAYS days)..."
DELETED_COUNT=$(find "$BACKUP_DIR" -name "vk_content_*.sql.gz" -mtime +$RETENTION_DAYS -delete -print | wc -l)
if [ "$DELETED_COUNT" -gt 0 ]; then
    log_info "Deleted $DELETED_COUNT old backup(s)"
else
    log_info "No old backups to delete"
fi

# List current backups
log_info "Current backups:"
ls -lh "$BACKUP_DIR"/vk_content_*.sql.gz 2>/dev/null | tail -5 || log_warn "No backups found"

# Summary
log_info "Backup completed successfully!"
log_info "Backup file: $BACKUP_FILE"
log_info "Backup size: $BACKUP_SIZE"

# Optional: Upload to cloud storage (uncomment and configure)
# if [ -n "$AWS_S3_BUCKET" ]; then
#     log_info "Uploading to S3: $AWS_S3_BUCKET"
#     aws s3 cp "$BACKUP_FILE" "s3://$AWS_S3_BUCKET/backups/"
# fi

# Optional: Send notification (uncomment and configure)
# if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
#     MESSAGE="✅ VK Content Workflow backup completed\nFile: $(basename $BACKUP_FILE)\nSize: $BACKUP_SIZE"
#     curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
#         -d chat_id="$TELEGRAM_CHAT_ID" \
#         -d text="$MESSAGE"
# fi

exit 0
