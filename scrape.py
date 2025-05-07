import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('violations.db')

# Query to count Moderate Risk violations on Fridays
query = """
SELECT business_id, COUNT(*) as violation_count
FROM violations
WHERE risk_category = 'Moderate Risk' AND strftime('%w', date) = '5'
GROUP BY business_id
"""
moderate_risk_violations = pd.read_sql_query(query, conn)

conn.close()