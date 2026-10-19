from django.db import connections

try:
    conn = connections["mysql_wwf"]
    conn.ensure_connection()
    print("SUCCESS: Connected to MySQL wwf_lums database!")
    
    # List existing tables
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    
    if tables:
        print(f"\nExisting tables in wwf_lums:")
        for t in tables:
            print(f"  - {t[0]}")
    else:
        print("\nNo tables exist yet in wwf_lums.")
        
except Exception as e:
    print(f"FAILED: Could not connect to MySQL: {e}")