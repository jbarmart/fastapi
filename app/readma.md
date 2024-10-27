


Expose Metrics in FastAPI: Your app/main.py is already set up to expose metrics at the /metrics endpoint. Ensure your FastAPI application is running:  
`uvicorn app.main:app --host 0.0.0.0 --port 8080
`

Start Prometheus: Run Prometheus with your configuration file:  
prometheus `prometheus --config.file=prometheus.yml`


Verify Metrics: Open your browser and navigate to http://localhost:8080/metrics to verify that your FastAPI application is exposing metrics.

To run Grafana and create a dashboard for your metrics, follow these steps:  
Start Grafana: Ensure Grafana is installed and start the Grafana server: 

`brew services start grafana`

Access Grafana: Open your web browser and go to http://localhost:3000. Log in with the default credentials:  
Username: admin
Password: admin

Add Prometheus as a Data Source:  
Go to Configuration > Data Sources.

Click Add data source and select Prometheus.
Set the URL to http://localhost:9090 (assuming Prometheus is running on the default port).
Click Save & Test to verify the connection.

Create a Dashboard:  
Go to Create > Dashboard.

Click Add new panel.

I n the Query section, enter your Prometheus query, for example:

`sum(request_count) by (method, endpoint)
`

Configure the visualization options as needed.

Click Apply to save the panel.

Save the Dashboard:  

Click the Save icon at the top of the dashboard.
Provide a name for your dashboard and click Save.
By following these steps, you will have Grafana running and a dashboard displaying your Prometheus metrics.

To tear down Grafana instance, run the following command:
`brew services stop grafana`

To tear down Prometheus instance, run the following command:
`pkill prometheus`