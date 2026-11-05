# Step 4: Run migrations
echo "Running database migrations"
python manage.py migrate --no-input

# Step 5: Restart services
echo "Restarting ${APP_NAME} services"
systemctl restart myapp-web
systemctl restart myapp-worker

# Step 6: Health check
echo "Running health check"
sleep 5
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health || true)
if [ "${HEALTH}" != "200" ]; then
    echo "Health check failed with status ${HEALTH}" >&2
    echo "Rolling back to ${BACKUP_DIR}/${TIMESTAMP}" >&2
    exit 1
fi

echo "Deployment of ${APP_NAME} completed successfully at $(date)"
