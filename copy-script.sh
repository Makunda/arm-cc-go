# Execution

# Replace the service file
if service --status-all | grep -Fq 'arm-cc-go'; then
  sudo service arm-cc-go stop
fi

sudo cp arm-cc-go.service /etc/systemd/arm-cc-go.service

systemctl enable arm-cc-go
systemctl daemon-reload
systemctl start arm-cc-go