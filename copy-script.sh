# Execution

# Replace the service file
if service --status-all | grep -Fq 'arm-cc-go'; then
  sudo service arm-cc-go stop
fi

sudo cp arm-cc-go.service /etc/systemd/system/arm-cc-go.service
sudo systemd-analyze verify arm-cc-go.service

sudo systemctl enable arm-cc-go
sudo systemctl daemon-reload
sudo systemctl start arm-cc-go