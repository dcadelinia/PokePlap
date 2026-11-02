import csv
import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pokeplap")
OUTPUT_FILE = "DEPLOYMENT_LEDGER.csv"

def export_telemetry_table_to_csv():
    print(f"Connecting to database to extract telemetry data arrays...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Pull records ordered longitudinally by time sequence
        query = "SELECT timestamp, source, target_variable, poked_value, timeline_index, computed_heart_rate, computed_spo2, computed_systolic_bp FROM telemetry_logs ORDER BY timestamp ASC;"
        cur.execute(query)
        rows = cur.fetchall()
        
        # Define fields matching clinical ledger spec
        headers = [
            "Timestamp", "Source", "Target Variable", "Poked Value", 
            "Timeline Index", "Heart Rate (bpm)", "SpO2 (%)", "Systolic BP (mmHg)"
        ]
        
        print(f"Writing {len(rows)} execution logs to {OUTPUT_FILE}...")
        with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers) # Write headers row
            writer.writerows(rows)   # Dump database records
            
        cur.close()
        conn.close()
        print(f"🏆 Export complete! Data saved successfully to: {os.path.abspath(OUTPUT_FILE)}")
        
    except Exception as error:
        print(f"❌ Failed to compile audited CSV export: {error}")

if __name__ == "__main__":
    export_telemetry_table_to_csv()
