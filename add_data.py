"""
Script to add Vidhi's data via API requests
Authenticates as vidhi22 first.
"""
import requests

BASE_URL = "http://localhost:8000"
USERNAME = "vidhi22"
PASSWORD = "password123"

# Education data
education = [
    {
        "institution": "D.J. Sanghvi College of Engineering, Mumbai",
        "degree": "B.Tech",
        "field_of_study": "Artificial Intelligence and Data Science",
        "start_year": "2023",
        "end_year": "2027",
        "grade": "CGPA: 9.29",
        "description": "Pursuing Bachelors in AI and Data Science with focus on deep learning and computer vision."
    },
    {
        "institution": "Jiten Mody Junior College, Mumbai",
        "degree": "HSC",
        "field_of_study": "Science",
        "start_year": "2021",
        "end_year": "2023",
        "grade": "86.00% | MHT-CET: 99.65 Percentile",
        "description": "Higher Secondary Certificate with excellent MHT-CET performance."
    }
]

# Projects data
projects = [
    {
        "project_name": "Smart Attendance System",
        "techstack": "Python, OpenCV, Deep Learning, Face Recognition",
        "description": "AI-powered attendance using OpenCV and deep learning for real-time face detection and recognition. Automated attendance marking reduces manual effort and increases accuracy.",
        "project_url": "https://github.com/vidhishah2209/Attendance-System"
    },
    {
        "project_name": "Suspicious Activity Detection",
        "techstack": "Python, OpenCV, YOLO, Deep Learning",
        "description": "Real-time surveillance system using OpenCV, YOLO, and deep learning. Automated alerts reduced manual monitoring. Object detection and behavior analysis to detect anomalies.",
        "project_url": "https://github.com/vidhishah2209/Suspicious-activity-detection"
    },
    {
        "project_name": "Smart Parking Scanner",
        "techstack": "Python, OpenCV, YOLO, Deep Learning",
        "description": "Real-time parking space detection using OpenCV, YOLO, and deep learning. Reduced parking search time and improved efficiency.",
        "project_url": "https://github.com/vidhishah2209/Innovative-Parking"
    }
]

# DSA topics
dsa_topics = [
    {"topic_name": "Arrays", "category": "Data Structure", "problems_solved": "Two Sum, Best Time to Buy and Sell Stock, Maximum Subarray, Product of Array Except Self", "description": "Fundamental data structure. Mastered array manipulation, sliding window, and prefix sum.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"topic_name": "Linked Lists", "category": "Data Structure", "problems_solved": "Reverse Linked List, Linked List Cycle, Merge Two Sorted Lists, Remove Nth Node From End", "description": "Linear data structure with nodes. Practiced singly, doubly linked lists and cycle detection.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"topic_name": "Stacks", "category": "Data Structure", "problems_solved": "Valid Parentheses, Min Stack, Daily Temperatures, Evaluate Reverse Polish Notation", "description": "LIFO data structure for expression evaluation, backtracking, and monotonic stack problems.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"topic_name": "Queues", "category": "Data Structure", "problems_solved": "Implement Queue using Stacks, Moving Average from Data Stream, Number of Recent Calls", "description": "FIFO data structure for BFS, task scheduling, and circular queue implementations.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"topic_name": "Sorting Algorithms", "category": "Algorithm", "problems_solved": "Merge Sorted Array, Sort Colors, Kth Largest Element in an Array, Top K Frequent Elements", "description": "Mastered Quick Sort, Merge Sort, and their applications in problem solving.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"topic_name": "Two Pointers", "category": "Concept", "problems_solved": "Container With Most Water, 3Sum, Trapping Rain Water, Valid Palindrome", "description": "Efficient technique for array problems like finding pairs and removing duplicates.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"topic_name": "Recursion", "category": "Concept", "problems_solved": "Climbing Stairs, Generate Parentheses, Subsets, Permutations", "description": "Problem-solving where a function calls itself. Applied in trees and backtracking.", "resources": "https://leetcode.com/u/vidhishah2209/"},
]

# Certificate
certificates = [
    {
        "title": "100+ DSA Problems Solved",
        "issuer": "LeetCode",
        "issue_date": "2024",
        "credential_url": "https://leetcode.com/u/vidhishah2209/",
        "description": "Solved 100+ DSA problems covering arrays, linked lists, stacks, queues, sorting, two pointers, and recursion."
    }
]

def get_token():
    print(f"Logging in as {USERNAME}...")
    try:
        r = requests.post(f"{BASE_URL}/auth/login", json={"username": USERNAME, "password": PASSWORD})
        if r.status_code == 200:
            return r.json()["access_token"]
        else:
            print(f"Login failed: {r.text}")
            return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def add_data():
    token = get_token()
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}

    # Helper to check existence - needs auth too? No, GET endpoints are public if user_id=1, but we might want to check via API.
    # Actually, simpler to just attempt add. If duplicate, DB might error or we can check first.
    # But wait, GET /education?user_id=1 is public. 
    # Let's clean up logic. Just add unconditionally? Or check.
    
    # Check existing data for profile 1 (assuming vidhi22 is profile 1)
    print("Fetching existing data...")
    existing_edu = requests.get(f"{BASE_URL}/education?user_id=1").json()
    existing_proj = requests.get(f"{BASE_URL}/projects?user_id=1").json()
    existing_dsa = requests.get(f"{BASE_URL}/dsa?user_id=1").json()
    existing_cert = requests.get(f"{BASE_URL}/certificates?user_id=1").json()

    print("\nAdding education...")
    for edu in education:
        # Check dupe
        if any(e['institution'] == edu['institution'] for e in existing_edu):
            print(f"Skipped: {edu['institution']}")
            continue
        edu['user_id'] = 1 # Satisfy schema
        r = requests.post(f"{BASE_URL}/education", json=edu, headers=headers)
        print(f"Added {edu['institution']}: {r.status_code}")

    print("\nAdding projects...")
    for proj in projects:
        if any(p['project_name'] == proj['project_name'] for p in existing_proj):
            print(f"Skipped: {proj['project_name']}")
            continue
        proj['user_id'] = 1 # Satisfy schema
        r = requests.post(f"{BASE_URL}/projects", json=proj, headers=headers)
        print(f"Added {proj['project_name']}: {r.status_code}")

    print("\nAdding DSA...")
    for dsa in dsa_topics:
        if any(d['topic_name'] == dsa['topic_name'] for d in existing_dsa):
            print(f"Skipped: {dsa['topic_name']}")
            continue
        dsa['user_id'] = 1 # Satisfy schema
        r = requests.post(f"{BASE_URL}/dsa", json=dsa, headers=headers)
        print(f"Added {dsa['topic_name']}: {r.status_code}")

    print("\nAdding certificates...")
    for cert in certificates:
        if any(c['title'] == cert['title'] for c in existing_cert):
            print(f"Skipped: {cert['title']}")
            continue
        cert['user_id'] = 1 # Satisfy schema
        r = requests.post(f"{BASE_URL}/certificates", json=cert, headers=headers)
        print(f"Added {cert['title']}: {r.status_code}")

if __name__ == "__main__":
    add_data()
