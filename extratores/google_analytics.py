from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Authenticate the API request using a service account JSON
keyfile_path = Path(__file__).parent.parent / "carregadores" / "credenciais" / "chave_datalake.json"
creds = service_account.Credentials.from_service_account_file(keyfile_path, scopes=['https://www.googleapis.com/auth/analytics.readonly'])

# Set up the Analytics Reporting API client
analytics = build('analyticsreporting', 'v4', credentials=creds)

# Set up the reporting query
view_id = '226955922'  # Replace with your Google Analytics view ID
start_date = "2023-01-01"  # Replace with your start date
end_date = "2023-03-31"  # Replace with your end date
dimensions = [{'name': 'ga:clientId'},
              {'name': 'ga:date'},
              {'name': 'ga:source'},
              {'name': 'ga:medium'},
              {'name': 'ga:sessionDurationBucket'}]
metrics = [{'expression': 'ga:users'}, {'expression': 'ga:transactionRevenue'}]
data = []

# Set up the first API request
request = {
    'viewId': view_id,
    'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
    'metrics': metrics,
    'dimensions': dimensions,
    'pageSize': 10000
}

# Make API requests until we have retrieved all the data
while True:
    # Execute the API request
    report = analytics.reports().batchGet(body={'reportRequests': [request]}).execute()

    # Extract the data from the API response
    rows = report['reports'][0]['data']['rows']
    for row in rows:
        client_id = row['dimensions'][0]
        date = row['dimensions'][1]
        source = row['dimensions'][2]
        medium = row['dimensions'][3]
        session_duration_bucket = row['dimensions'][4]
        users = row['metrics'][0]['values'][0]
        revenue = row['metrics'][0]['values'][1]
        data.append([client_id, date, source, medium, session_duration_bucket, users, revenue])

    # Check if there is more data to retrieve
    next_page_token = report['reports'][0].get('nextPageToken')
    if next_page_token:
        request['pageToken'] = next_page_token
        print("10.000 linhas de dados obtidas")
    else:
        break

# Export the data to a file
with open(f'user_data_{start_date}_to_{end_date}.csv', 'w', encoding='utf-8') as f:
    f.write('Client ID,Date,Source,Medium,Session Duration Bucket,Users,Revenue\n')
    for row in data:
        client_id = row[0]
        date = row[1]
        source = row[2]
        medium = row[3]
        session_duration_bucket = row[4]
        users = row[5]
        revenue = row[6]
        f.write(f'{client_id},{date},{source},{medium},{session_duration_bucket},{users},{revenue}\n')
