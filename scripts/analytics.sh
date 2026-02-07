#!/bin/bash

# VK Content Workflow - Analytics Collection Script
# This script collects analytics from VK API and updates the database

set -e

# Configuration
VK_ACCESS_TOKEN="${VK_ACCESS_TOKEN}"
VK_API_VERSION="${VK_API_VERSION:-5.131}"
PGHOST="${PGHOST:-postgres}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-postgres}"
PGDATABASE="${PGDATABASE:-vk_content}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# Check required variables
if [ -z "$VK_ACCESS_TOKEN" ]; then
    log_error "VK_ACCESS_TOKEN is not set"
    exit 1
fi

# Get posts that need analytics update
log_info "Fetching posts for analytics update..."

POSTS=$(psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -t -c \
    "SELECT full_id FROM vk_posts 
     WHERE metrics_updated_at IS NULL 
        OR metrics_updated_at < NOW() - INTERVAL '6 hours' 
     ORDER BY created_at DESC 
     LIMIT 100;" | tr -d ' ')

if [ -z "$POSTS" ]; then
    log_info "No posts need analytics update"
    exit 0
fi

POST_COUNT=$(echo "$POSTS" | wc -l)
log_info "Found $POST_COUNT posts to update"

# Process each post
UPDATED=0
FAILED=0

for FULL_ID in $POSTS; do
    log_debug "Processing post: $FULL_ID"
    
    # Call VK API to get post stats
    RESPONSE=$(curl -s "https://api.vk.com/method/wall.getById" \
        -d "posts=$FULL_ID" \
        -d "access_token=$VK_ACCESS_TOKEN" \
        -d "v=$VK_API_VERSION")
    
    # Check for errors
    if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
        ERROR_MSG=$(echo "$RESPONSE" | jq -r '.error.error_msg')
        log_warn "API Error for $FULL_ID: $ERROR_MSG"
        ((FAILED++))
        continue
    fi
    
    # Extract metrics
    LIKES=$(echo "$RESPONSE" | jq -r '.response[0].likes.count // 0')
    COMMENTS=$(echo "$RESPONSE" | jq -r '.response[0].comments.count // 0')
    REPOSTS=$(echo "$RESPONSE" | jq -r '.response[0].reposts.count // 0')
    VIEWS=$(echo "$RESPONSE" | jq -r '.response[0].views.count // 0')
    
    # Update database
    psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c \
        "UPDATE vk_posts 
         SET likes_count = $LIKES,
             comments_count = $COMMENTS,
             reposts_count = $REPOSTS,
             views_count = $VIEWS,
             metrics_updated_at = NOW()
         WHERE full_id = '$FULL_ID';" > /dev/null
    
    # Insert into metrics history
    psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c \
        "INSERT INTO vk_posts_metrics (post_id, owner_id, full_id, likes_count, comments_count, reposts_count, views_count)
         SELECT post_id, owner_id, full_id, $LIKES, $COMMENTS, $REPOSTS, $VIEWS
         FROM vk_posts WHERE full_id = '$FULL_ID';" > /dev/null
    
    log_info "Updated $FULL_ID: 👍 $LIKES | 💬 $COMMENTS | 🔄 $REPOSTS | 👁 $VIEWS"
    ((UPDATED++))
    
    # Rate limiting (3 requests per second max)
    sleep 0.35
done

# Summary
log_info "Analytics collection completed!"
log_info "Updated: $UPDATED posts"
if [ $FAILED -gt 0 ]; then
    log_warn "Failed: $FAILED posts"
fi

# Generate summary report
log_info "Generating summary report..."

TOTAL_POSTS=$(psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -t -c \
    "SELECT COUNT(*) FROM vk_posts;" | tr -d ' ')

TOTAL_LIKES=$(psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -t -c \
    "SELECT SUM(likes_count) FROM vk_posts;" | tr -d ' ')

TOTAL_COMMENTS=$(psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -t -c \
    "SELECT SUM(comments_count) FROM vk_posts;" | tr -d ' ')

TOTAL_REPOSTS=$(psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -t -c \
    "SELECT SUM(reposts_count) FROM vk_posts;" | tr -d ' ')

TOTAL_VIEWS=$(psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -t -c \
    "SELECT SUM(views_count) FROM vk_posts;" | tr -d ' ')

echo ""
echo "========================================="
echo "         ANALYTICS SUMMARY"
echo "========================================="
echo "Total Posts:    $TOTAL_POSTS"
echo "Total Likes:    $TOTAL_LIKES"
echo "Total Comments: $TOTAL_COMMENTS"
echo "Total Reposts:  $TOTAL_REPOSTS"
echo "Total Views:    $TOTAL_VIEWS"
echo "========================================="

# Optional: Send notification
if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    MESSAGE="📊 VK Analytics Update\n\nUpdated: $UPDATED posts\nTotal Posts: $TOTAL_POSTS\nTotal Likes: $TOTAL_LIKES\nTotal Views: $TOTAL_VIEWS"
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d chat_id="$TELEGRAM_CHAT_ID" \
        -d text="$MESSAGE" > /dev/null
fi

exit 0
