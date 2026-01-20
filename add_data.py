"""
Script to add Vidhi's data via API requests
Uses upsert logic - only adds data if it doesn't already exist
"""
import requests

BASE_URL = "http://localhost:8000"

# Education data
education = [
    {
        "user_id": 1,
        "institution": "D.J. Sanghvi College of Engineering, Mumbai",
        "degree": "B.Tech",
        "field_of_study": "Artificial Intelligence and Data Science",
        "start_year": "2023",
        "end_year": "2027",
        "grade": "CGPA: 9.29",
        "description": "Pursuing Bachelors in AI and Data Science with focus on deep learning and computer vision."
    },
    {
        "user_id": 1,
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
        "user_id": 1,
        "project_name": "Smart Attendance System",
        "techstack": "Python, OpenCV, Deep Learning, Face Recognition",
        "description": "AI-powered attendance using OpenCV and deep learning for real-time face detection and recognition. Automated attendance marking reduces manual effort and increases accuracy.",
        "project_url": "https://github.com/vidhishah2209/Attendance-System"
    },
    {
        "user_id": 1,
        "project_name": "Suspicious Activity Detection",
        "techstack": "Python, OpenCV, YOLO, Deep Learning",
        "description": "Real-time surveillance system using OpenCV, YOLO, and deep learning. Automated alerts reduced manual monitoring. Object detection and behavior analysis to detect anomalies.",
        "project_url": "https://github.com/vidhishah2209/Suspicious-activity-detection"
    },
    {
        "user_id": 1,
        "project_name": "Smart Parking Scanner",
        "techstack": "Python, OpenCV, YOLO, Deep Learning",
        "description": "Real-time parking space detection using OpenCV, YOLO, and deep learning. Reduced parking search time and improved efficiency.",
        "project_url": "https://github.com/vidhishah2209/Innovative-Parking"
    }
]

# DSA topics - with problems_solved field
dsa_topics = [
    {"user_id": 1, "topic_name": "Arrays", "category": "Data Structure", "problems_solved": "Two Sum, Best Time to Buy and Sell Stock, Maximum Subarray, Product of Array Except Self", "description": "Fundamental data structure. Mastered array manipulation, sliding window, and prefix sum.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"user_id": 1, "topic_name": "Linked Lists", "category": "Data Structure", "problems_solved": "Reverse Linked List, Linked List Cycle, Merge Two Sorted Lists, Remove Nth Node From End", "description": "Linear data structure with nodes. Practiced singly, doubly linked lists and cycle detection.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"user_id": 1, "topic_name": "Stacks", "category": "Data Structure", "problems_solved": "Valid Parentheses, Min Stack, Daily Temperatures, Evaluate Reverse Polish Notation", "description": "LIFO data structure for expression evaluation, backtracking, and monotonic stack problems.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"user_id": 1, "topic_name": "Queues", "category": "Data Structure", "problems_solved": "Implement Queue using Stacks, Moving Average from Data Stream, Number of Recent Calls", "description": "FIFO data structure for BFS, task scheduling, and circular queue implementations.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"user_id": 1, "topic_name": "Sorting Algorithms", "category": "Algorithm", "problems_solved": "Merge Sorted Array, Sort Colors, Kth Largest Element in an Array, Top K Frequent Elements", "description": "Mastered Quick Sort, Merge Sort, and their applications in problem solving.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"user_id": 1, "topic_name": "Two Pointers", "category": "Concept", "problems_solved": "Container With Most Water, 3Sum, Trapping Rain Water, Valid Palindrome", "description": "Efficient technique for array problems like finding pairs and removing duplicates.", "resources": "https://leetcode.com/u/vidhishah2209/"},
    {"user_id": 1, "topic_name": "Recursion", "category": "Concept", "problems_solved": "Climbing Stairs, Generate Parentheses, Subsets, Permutations", "description": "Problem-solving where a function calls itself. Applied in trees and backtracking.", "resources": "https://leetcode.com/u/vidhishah2209/"},
]

# Certificate
certificates = [
    {
        "user_id": 1,
        "title": "100+ DSA Problems Solved",
        "issuer": "LeetCode",
        "issue_date": "2024",
        "credential_url": "https://leetcode.com/u/vidhishah2209/",
        "description": "Solved 100+ DSA problems covering arrays, linked lists, stacks, queues, sorting, two pointers, and recursion."
    }
]


def get_existing_data():
    """Fetch all existing data from the API"""
    existing = {
        "education": [],
        "projects": [],
        "dsa": [],
        "certificates": []
    }
    
    try:
        r = requests.get(f"{BASE_URL}/education")
        if r.status_code == 200:
            existing["education"] = r.json()
    except:
        pass
    
    try:
        r = requests.get(f"{BASE_URL}/projects")
        if r.status_code == 200:
            existing["projects"] = r.json()
    except:
        pass
    
    try:
        r = requests.get(f"{BASE_URL}/dsa")
        if r.status_code == 200:
            existing["dsa"] = r.json()
    except:
        pass
    
    try:
        r = requests.get(f"{BASE_URL}/certificates")
        if r.status_code == 200:
            existing["certificates"] = r.json()
    except:
        pass
    
    return existing


def education_exists(edu, existing_list):
    """Check if education already exists based on institution and degree"""
    for e in existing_list:
        if e.get("institution") == edu["institution"] and e.get("degree") == edu["degree"]:
            return True
    return False


def project_exists(proj, existing_list):
    """Check if project already exists based on project_name"""
    for p in existing_list:
        if p.get("project_name") == proj["project_name"]:
            return True
    return False


def dsa_exists(topic, existing_list):
    """Check if DSA topic already exists based on topic_name"""
    for t in existing_list:
        if t.get("topic_name") == topic["topic_name"]:
            return True
    return False


def cert_exists(cert, existing_list):
    """Check if certificate already exists based on title and issuer"""
    for c in existing_list:
        if c.get("title") == cert["title"] and c.get("issuer") == cert["issuer"]:
            return True
    return False


def add_data():
    print("Fetching existing data...")
    existing = get_existing_data()
    
    print("\nAdding education...")
    for edu in education:
        if education_exists(edu, existing["education"]):
            print(f"  Skipped (exists): {edu['institution']} - {edu['degree']}")
        else:
            try:
                r = requests.post(f"{BASE_URL}/education", json=edu)
                print(f"  Added: {edu['institution']} - {edu['degree']} (Status: {r.status_code})")
            except Exception as e:
                print(f"  Error: {e}")
    
    print("\nAdding projects...")
    for proj in projects:
        if project_exists(proj, existing["projects"]):
            print(f"  Skipped (exists): {proj['project_name']}")
        else:
            try:
                r = requests.post(f"{BASE_URL}/projects", json=proj)
                print(f"  Added: {proj['project_name']} (Status: {r.status_code})")
            except Exception as e:
                print(f"  Error: {e}")
    
    print("\nAdding DSA topics...")
    for topic in dsa_topics:
        if dsa_exists(topic, existing["dsa"]):
            print(f"  Skipped (exists): {topic['topic_name']}")
        else:
            try:
                r = requests.post(f"{BASE_URL}/dsa", json=topic)
                print(f"  Added: {topic['topic_name']} (Status: {r.status_code})")
            except Exception as e:
                print(f"  Error: {e}")
    
    print("\nAdding certificates...")
    for cert in certificates:
        if cert_exists(cert, existing["certificates"]):
            print(f"  Skipped (exists): {cert['title']}")
        else:
            try:
                r = requests.post(f"{BASE_URL}/certificates", json=cert)
                print(f"  Added: {cert['title']} (Status: {r.status_code})")
            except Exception as e:
                print(f"  Error: {e}")
    
    print("\nDone! Check http://localhost:8000")


if __name__ == "__main__":
    add_data()
