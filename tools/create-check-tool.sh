#!/bin/bash
# Create new check tool from template

set -e

TOOL_NAME="$1"
PURPOSE="$2"

# ===== Validation =====

if [ -z "$TOOL_NAME" ]; then
    echo "Usage: $0 <tool-name> [purpose]"
    echo ""
    echo "Example:"
    echo "  $0 check-duplicate-headers 'Check for duplicate headers'"
    echo ""
    echo "Tool name must start with 'check-'"
    exit 1
fi

# Validate tool name format
if [[ ! "$TOOL_NAME" =~ ^check- ]]; then
    echo "❌ Error: Tool name must start with 'check-'"
    echo "   Example: check-duplicate-headers"
    exit 1
fi

# Check if tool already exists
if [ -f "tools/$TOOL_NAME.sh" ]; then
    echo "❌ Error: Tool already exists: tools/$TOOL_NAME.sh"
    exit 1
fi

# ===== Create from templates =====

echo "Creating tool from templates..."

# Copy templates
cp tools/templates/check-tool-template.sh "tools/$TOOL_NAME.sh"
cp tools/templates/test-tool-template.sh "tools/test-$TOOL_NAME.sh"

# Get metadata
DATE=$(date +%Y-%m-%d)
AUTHOR=$(git config user.name 2>/dev/null || echo "Unknown")

# Replace placeholders
sed -i "s/\[TOOL_NAME\]/$TOOL_NAME/g" "tools/$TOOL_NAME.sh" "tools/test-$TOOL_NAME.sh"
sed -i "s/\[PURPOSE\]/${PURPOSE:-TODO: Add purpose}/g" "tools/$TOOL_NAME.sh"
sed -i "s/\[AUTHOR\]/$AUTHOR/g" "tools/$TOOL_NAME.sh"
sed -i "s/\[DATE\]/$DATE/g" "tools/$TOOL_NAME.sh"

# Set executable permissions
chmod +x "tools/$TOOL_NAME.sh" "tools/test-$TOOL_NAME.sh"

# ===== Success message =====

echo ""
echo "✅ Created:"
echo "  - tools/$TOOL_NAME.sh"
echo "  - tools/test-$TOOL_NAME.sh"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Edit tools/$TOOL_NAME.sh"
echo "   - Implement check_file() function"
echo "   - Replace [WHAT] with what you're checking"
echo ""
echo "2. Edit tools/test-$TOOL_NAME.sh"
echo "   - Add known bug content (Test 1)"
echo "   - Add normal content (Test 2)"
echo ""
echo "3. Run test:"
echo "   ./tools/test-$TOOL_NAME.sh"
echo ""
echo "4. Verify it works:"
echo "   ./tools/$TOOL_NAME.sh docs/"
echo ""
echo "5. Integrate:"
echo "   - Add to .git/hooks/pre-commit"
echo "   - Update docs/05_meta/05_automation-tools.md"
echo ""
echo "📖 See also:"
echo "   - tools/templates/README.md"
echo "   - docs/05_meta/14_tool-creation-checklist.md"
