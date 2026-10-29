# BMS-Monitoring-Lab
A Dockerized mini Building Management System that simulates a sensor, raises alerts, deduplicates them, and visualizes everything
## Architecture

<img width="1231" height="824" alt="image" src="https://github.com/user-attachments/assets/03def721-042b-4488-a560-d715bc4a9983" />

| Component | Role |

| Modbus Sensor simulator script | Generates temperature readings | 

| Alerta | Receives, deduplicates, and manages alerts | 

| Grafana | Dashboards for sensor data, alerts and system resources | 

| FUXA | SCADA/HMI visualization | 

| Mongo DB | DB for Alerta | 


## How to ( Clone & deploy)
git clone [repo]

cd [repo]

docker compose up -d

Then open the apps with mentiond ports using http://localhost:[port]
If you want to access the apps in remote mode just use tunneling app like cloudflare or it is eay to setup tailscale funnels as well. 

## Alert flow
1. The sensor generates and sends a simulated temperatire reading every 5 seconds.
2. If temperature exceeds the [threshold], an alert is sent to Alerta from FUXA.
3. Repeated alerts with the same resource and event are merged and the duplicate count increases.
4. When the value returns to normal, the alert is cleared auto matically.
5. Grafana displays all the alerts, temperature trends and internal resource utilisations in 2 seperate dashboards.
6. Resource utilisation dash board is publicly viewable while the temperature sensors date is behind the login.

## Walkthrough 


https://github.com/user-attachments/assets/a7ec1dcb-e4c4-41a0-a9a5-6568a7b48512





## Runbooks [not yet available]
- [High temperature alarm](runbooks/high-temperature.md)

## What I learned 
- Modbus integration / Troubleshooting
- Alert deduplication
- Inter system connectivity / Troubleshooting
- System integration
- Hands on BMS system configuration

## Next steps
- Modbus simulation using industry specific application
- Error injection and behavioural analysis
- Modbus specific troubleshooting
- Modbus TCP and how it works in real environment
- More runbooks for real world scenarios
- Integration of ticket management backend like Zendesk
- Integration of automation platforms like N8N for critical alert automations
