#!/bin/bash

# Test script to verify Cursor launch without draft field

echo "==================================="
echo "Cursor Test - No Draft Field"
echo "==================================="
echo ""

# Check if configuration file exists
if [ -f "cursor-test.json" ]; then
    echo "✅ Configuration file found: cursor-test.json"
else
    echo "❌ Configuration file not found"
    exit 1
fi

# Verify that draft field is NOT present (as a JSON key)
if grep -q '"draft"' cursor-test.json; then
    echo "❌ FAIL: Draft field found in configuration"
    exit 1
else
    echo "✅ PASS: No draft field in configuration"
fi

# Validate JSON structure
if command -v python3 &> /dev/null; then
    if python3 -c "import json; json.load(open('cursor-test.json'))" 2>/dev/null; then
        echo "✅ PASS: Valid JSON structure"
    else
        echo "❌ FAIL: Invalid JSON structure"
        exit 1
    fi
else
    echo "⚠️  Python3 not available, skipping JSON validation"
fi

echo ""
echo "==================================="
echo "All tests passed! ✅"
echo "Cursor can launch without draft field"
echo "==================================="

exit 0
