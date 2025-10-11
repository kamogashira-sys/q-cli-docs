#!/bin/bash

set -e

LOG_FILE="work_records/20251011/link_fix_log.txt"

echo "=== リンク修正開始 ===" | tee "$LOG_FILE"
echo "開始時刻: $(date)" | tee -a "$LOG_FILE"

cd docs

# パターン1: getting-started/ → for-users/getting-started/
echo "パターン1: getting-started/" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](getting-started/|](for-users/getting-started/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../getting-started/|](../for-users/getting-started/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../../getting-started/|](../../for-users/getting-started/|g' {} \;

# パターン2: user-guide/configuration/ → for-users/configuration/
echo "パターン2: user-guide/configuration/" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](user-guide/configuration/|](for-users/configuration/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../user-guide/configuration/|](../for-users/configuration/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../../user-guide/configuration/|](../../for-users/configuration/|g' {} \;

# パターン3: user-guide/features/ → for-users/features/
echo "パターン3: user-guide/features/" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](user-guide/features/|](for-users/features/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../user-guide/features/|](../for-users/features/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../../user-guide/features/|](../../for-users/features/|g' {} \;

# パターン4: user-guide/best-practices/ → for-users/best-practices/
echo "パターン4: user-guide/best-practices/" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](user-guide/best-practices/|](for-users/best-practices/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../user-guide/best-practices/|](../for-users/best-practices/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../../user-guide/best-practices/|](../../for-users/best-practices/|g' {} \;

# パターン5: user-guide/troubleshooting/ → for-users/troubleshooting/
echo "パターン5: user-guide/troubleshooting/" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](user-guide/troubleshooting/|](for-users/troubleshooting/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../user-guide/troubleshooting/|](../for-users/troubleshooting/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../../user-guide/troubleshooting/|](../../for-users/troubleshooting/|g' {} \;

# パターン6: user-guide/README.md → for-users/README.md
echo "パターン6: user-guide/README.md" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](user-guide/README.md)|](for-users/README.md)|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../user-guide/README.md)|](../for-users/README.md)|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../../user-guide/README.md)|](../../for-users/README.md)|g' {} \;

# パターン7: user-guide/enterprise-deployment.md → for-users/deployment/enterprise-deployment.md
echo "パターン7: enterprise-deployment.md" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](user-guide/enterprise-deployment.md)|](for-users/deployment/enterprise-deployment.md)|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../user-guide/enterprise-deployment.md)|](../for-users/deployment/enterprise-deployment.md)|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](enterprise-deployment.md)|](deployment/enterprise-deployment.md)|g' {} \;

# パターン8: reference/ → for-users/reference/
echo "パターン8: reference/" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](reference/|](for-users/reference/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../reference/|](../for-users/reference/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../../reference/|](../../for-users/reference/|g' {} \;

# パターン9: developer-guide/ → for-developers/
echo "パターン9: developer-guide/" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](developer-guide/|](for-developers/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../developer-guide/|](../for-developers/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../../developer-guide/|](../../for-developers/|g' {} \;

# パターン10: updates/ → for-community/updates/
echo "パターン10: updates/" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](updates/|](for-community/updates/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../updates/|](../for-community/updates/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../../updates/|](../../for-community/updates/|g' {} \;

# パターン11: community/ → for-community/community/
echo "パターン11: community/" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](community/|](for-community/community/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../community/|](../for-community/community/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../../community/|](../../for-community/community/|g' {} \;

# パターン12: analysis/ → for-community/analysis/
echo "パターン12: analysis/" | tee -a "../$LOG_FILE"
find . -name "*.md" -type f -exec sed -i 's|](analysis/|](for-community/analysis/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../analysis/|](../for-community/analysis/|g' {} \;
find . -name "*.md" -type f -exec sed -i 's|](../../analysis/|](../../for-community/analysis/|g' {} \;

cd ..
echo "=== リンク修正完了 ===" | tee -a "$LOG_FILE"
echo "完了時刻: $(date)" | tee -a "$LOG_FILE"
