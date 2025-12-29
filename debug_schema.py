# debug_schema.py
import os
import json
from dotenv import load_dotenv
from grid_client import GridClient

# Load variables from .env file
load_dotenv()

def debug_schema():
    api_key = os.getenv("GRID_API_KEY")
    if not api_key:
        print("❌ Error: GRID_API_KEY not found in .env file")
        return

    client = GridClient(api_key)
    
    # Reset to original request to be sure, but let's check Match/Matches too
    query = """
    query {
      __type(name: "Match") {
        name
        fields {
          name
        }
      }
    }
    """
    print("\n🔍 Checking if 'Match' type exists...")
    res = client._execute_query(query)
    if res and res['__type']:
        print("✅ 'Match' type exists. Fields:")
        for f in res['__type']['fields']:
            print(f" - {f['name']}")

    query_series = """
    query {
      __type(name: "Series") {
        fields {
          name
          type {
            name
            kind
            ofType {
              name
              kind
              ofType {
                name
                kind
              }
            }
          }
        }
      }
    }
    """
    print("\n🔍 Re-checking 'Series' type fields...")
    result = client._execute_query(query_series)
    if result and result['__type']:
        fields = result['__type']['fields']
        for field in fields:
            print(f" - {field['name']}")

if __name__ == "__main__":
    debug_schema()
