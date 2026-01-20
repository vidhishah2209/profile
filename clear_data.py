"""
Script to clear all data from the database and reset it
"""
import requests

BASE_URL = "http://localhost:8000"


def clear_all_data():
    print("Clearing all existing data...")
    
    # Get and delete all education entries
    print("\nClearing education...")
    try:
        r = requests.get(f"{BASE_URL}/education")
        if r.status_code == 200:
            for edu in r.json():
                del_r = requests.delete(f"{BASE_URL}/education/{edu['id']}")
                print(f"  Deleted education ID {edu['id']}: {del_r.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Get and delete all projects
    print("\nClearing projects...")
    try:
        r = requests.get(f"{BASE_URL}/projects")
        if r.status_code == 200:
            for proj in r.json():
                del_r = requests.delete(f"{BASE_URL}/projects/{proj['id']}")
                print(f"  Deleted project ID {proj['id']}: {del_r.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Get and delete all DSA topics
    print("\nClearing DSA topics...")
    try:
        r = requests.get(f"{BASE_URL}/dsa")
        if r.status_code == 200:
            for topic in r.json():
                del_r = requests.delete(f"{BASE_URL}/dsa/{topic['id']}")
                print(f"  Deleted DSA topic ID {topic['id']}: {del_r.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Get and delete all certificates
    print("\nClearing certificates...")
    try:
        r = requests.get(f"{BASE_URL}/certificates")
        if r.status_code == 200:
            for cert in r.json():
                del_r = requests.delete(f"{BASE_URL}/certificates/{cert['id']}")
                print(f"  Deleted certificate ID {cert['id']}: {del_r.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\nAll data cleared!")


if __name__ == "__main__":
    clear_all_data()
