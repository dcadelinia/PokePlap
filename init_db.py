import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pokeplap")

def initialize_telemetry_ledger():
    """Creates the structural tables required to store historical ICU digital twin data."""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS telemetry_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            source VARCHAR(100) NOT NULL,
            target_variable VARCHAR(50) NOT NULL,
            poked_value NUMERIC(5,2) NOT NULL,
            timeline_index INT NOT NULL,
            computed_heart_rate INT NOT NULL,
            computed_spo2 INT NOT NULL,
            computed_systolic_bp INT NOT NULL
        )
        """,
    )
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        conn.close()
        print("✅ Database topology initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to seed database schema: {e}")

if __name__ == "__main__":
    initialize_telemetry_ledger()
