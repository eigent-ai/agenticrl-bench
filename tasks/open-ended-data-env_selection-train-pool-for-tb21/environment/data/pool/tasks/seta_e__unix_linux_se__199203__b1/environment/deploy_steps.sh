# Step 1: Create backup
echo "Creating backup at ${BACKUP_DIR}/${TIMESTAMP}"
mkdir -p "${BACKUP_DIR}"
if [ -d "${DEPLOY_DIR}/current" ]; then
    cp -a "${DEPLOY_DIR}/current" "${BACKUP_DIR}/${TIMESTAMP}"
fi

# Step 2: Pull latest release
echo "Pulling latest release for ${APP_NAME}"
cd "${DEPLOY_DIR}"
git fetch origin main
git checkout main
git pull origin main

# Step 3: Install dependencies
echo "Installing dependencies"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
