"""
Seed script to populate the database with Vidhi's real data.
Run from project root: python seed.py
"""
import sys
sys.path.insert(0, './backend')

from database import SessionLocal, engine
import models

# Drop and recreate all tables to ensure clean state
# This is important because we changed the schema (problems_solved)
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
print("✅ Database tables recreated")


def seed_database():
    db = SessionLocal()
    
    try:
        # Create Vidhi's profile
        profile = models.BasicInfo(
            full_name="Vidhi Shah",
            email="vidhishah2209@gmail.com",
            phone="+91 9321750450",
            location="Mumbai, India",
            linkedin="https://linkedin.com/in/username",
            github="https://github.com/vidhishah2209",
            leetcode="https://leetcode.com/u/vidhishah2209/",
            bio="AI & Data Science student at D.J. Sanghvi College of Engineering. Passionate about deep learning, computer vision, and solving DSA problems."
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        print(f"✅ Created profile: {profile.full_name}")
        
        # Education 1
        edu1 = models.Education(
            user_id=profile.id,
            institution="D.J. Sanghvi College of Engineering, Mumbai",
            degree="B.Tech",
            field_of_study="Artificial Intelligence and Data Science",
            start_year="2023",
            end_year="2027",
            grade="CGPA: 9.29",
            description="Pursuing Bachelor's in AI & Data Science with focus on deep learning and computer vision."
        )
        db.add(edu1)
        
        # Education 2
        edu2 = models.Education(
            user_id=profile.id,
            institution="Jiten Mody Junior College, Mumbai",
            degree="HSC",
            field_of_study="Science",
            start_year="2021",
            end_year="2023",
            grade="86.00% | MHT-CET: 99.65 Percentile",
            description="Higher Secondary Certificate with excellent MHT-CET performance."
        )
        db.add(edu2)
        db.commit()
        print("✅ Created 2 education entries")
        
        # Project 1
        proj1 = models.Project(
            user_id=profile.id,
            project_name="Smart Attendance System",
            techstack="Python, OpenCV, Deep Learning, Face Recognition",
            description="AI-powered attendance using OpenCV and deep learning for real-time face detection and recognition. Automated attendance marking reduces manual effort and increases accuracy.",
            project_url="https://github.com/vidhishah2209/Attendance-System"
        )
        db.add(proj1)
        
        # Project 2
        proj2 = models.Project(
            user_id=profile.id,
            project_name="Suspicious Activity Detection",
            techstack="Python, OpenCV, YOLO, Deep Learning",
            description="Real-time surveillance system using OpenCV, YOLO, and deep learning. Automated alerts reduced manual monitoring. Object detection and behavior analysis to detect anomalies.",
            project_url="https://github.com/vidhishah2209/Suspicious-activity-detection"
        )
        db.add(proj2)
        
        # Project 3
        proj3 = models.Project(
            user_id=profile.id,
            project_name="Smart Parking Scanner",
            techstack="Python, OpenCV, YOLO, Deep Learning",
            description="Real-time parking space detection using OpenCV, YOLO, and deep learning. Reduced parking search time and improved efficiency.",
            project_url="https://github.com/vidhishah2209/Innovative-Parking"
        )
        db.add(proj3)
        db.commit()
        print("✅ Created 3 projects")
        
        # DSA Topics - Updated with problems_solved instead of difficulty
        dsa_data = [
            ("Arrays", "Data Structure", "Two Sum, Best Time to Buy and Sell Stock, Maximum Subarray, Product of Array Except Self", "Fundamental data structure. Mastered array manipulation, sliding window, and prefix sum."),
            ("Linked Lists", "Data Structure", "Reverse Linked List, Linked List Cycle, Merge Two Sorted Lists, Remove Nth Node From End", "Linear data structure with nodes. Practiced singly, doubly linked lists and cycle detection."),
            ("Stacks", "Data Structure", "Valid Parentheses, Min Stack, Daily Temperatures, Evaluate Reverse Polish Notation", "LIFO data structure for expression evaluation, backtracking, and monotonic stack problems."),
            ("Queues", "Data Structure", "Implement Queue using Stacks, Moving Average from Data Stream, Number of Recent Calls", "FIFO data structure for BFS, task scheduling, and circular queue implementations."),
            ("Sorting Algorithms", "Algorithm", "Merge Sorted Array, Sort Colors, Kth Largest Element in an Array, Top K Frequent Elements", "Mastered Quick Sort, Merge Sort, and their applications in problem solving."),
            ("Two Pointers", "Concept", "Container With Most Water, 3Sum, Trapping Rain Water, Valid Palindrome", "Efficient technique for array problems like finding pairs and removing duplicates."),
            ("Recursion", "Concept", "Climbing Stairs, Generate Parentheses, Subsets, Permutations", "Problem-solving where a function calls itself. Applied in trees and backtracking."),
        ]
        
        for name, cat, problems, desc in dsa_data:
            topic = models.DSATopic(
                user_id=profile.id,
                topic_name=name,
                category=cat,
                description=desc,
                problems_solved=problems,
                resources="https://leetcode.com/u/vidhishah2209/"
            )
            db.add(topic)
        db.commit()
        print("✅ Created 7 DSA topics")
        
        # Certificate
        cert = models.Certificate(
            user_id=profile.id,
            title="100+ DSA Problems Solved",
            issuer="LeetCode",
            issue_date="2024",
            credential_url="https://leetcode.com/u/vidhishah2209/",
            description="Solved 100+ DSA problems covering arrays, linked lists, stacks, queues, sorting, two pointers, and recursion."
        )
        db.add(cert)
        db.commit()
        print("✅ Created 1 certificate")
        
        print("\n🎉 Database seeded with Vidhi's real data!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
