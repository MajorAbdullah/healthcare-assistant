#!/usr/bin/env python3
"""
API Test Suite - Verify all endpoints work
Run this to test the FastAPI backend
"""

import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000/api/v1"

def print_test(name, success=True):
    icon = "✅" if success else "❌"
    print(f"{icon} {name}")

def test_api():
    print("\n" + "="*60)
    print("🧪 Testing Healthcare Assistant API")
    print("="*60 + "\n")
    
    # Test 1: Health Check
    try:
        r = requests.get("http://localhost:8000/health")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"
        print_test("Health Check")
    except Exception as e:
        print_test(f"Health Check: {e}", False)
        return
    
    # Test 2: Get Doctors
    try:
        r = requests.get(f"{BASE_URL}/doctors")
        data = r.json()
        assert data["success"] == True
        assert len(data["data"]) > 0
        print_test(f"Get Doctors ({len(data['data'])} found)")
        doctor_id = data["data"][0]["doctor_id"]
    except Exception as e:
        print_test(f"Get Doctors: {e}", False)
        return
    
    # Test 3: Doctor Login
    try:
        r = requests.post(f"{BASE_URL}/doctors/login", json={"doctor_id": doctor_id})
        data = r.json()
        assert data["success"] == True
        print_test(f"Doctor Login: {data['data']['name']}")
    except Exception as e:
        print_test(f"Doctor Login: {e}", False)
    
    # Test 4: Doctor Stats
    try:
        r = requests.get(f"{BASE_URL}/doctors/{doctor_id}/stats")
        data = r.json()
        assert data["success"] == True
        print_test(f"Doctor Stats (Patients: {data['data']['total_patients']})")
    except Exception as e:
        print_test(f"Doctor Stats: {e}", False)
    
    # Test 5: Doctor Availability
    try:
        tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        r = requests.get(f"{BASE_URL}/doctors/{doctor_id}/availability?date={tomorrow}")
        data = r.json()
        assert data["success"] == True
        slots = data["data"]["total_slots"]
        print_test(f"Doctor Availability ({slots} slots available)")
    except Exception as e:
        print_test(f"Doctor Availability: {e}", False)
    
    # Test 6: Register Patient
    try:
        r = requests.post(f"{BASE_URL}/patients/register", json={
            "name": "Test Patient API",
            "email": "test_api@example.com",
            "phone": "5551234567"
        })
        data = r.json()
        assert data["success"] == True
        user_id = data["data"]["user_id"]
        print_test(f"Register Patient (ID: {user_id})")
    except Exception as e:
        print_test(f"Register Patient: {e}", False)
        return
    
    # Test 7: Patient Login
    try:
        r = requests.post(f"{BASE_URL}/patients/login", json={
            "email": "test_api@example.com",
            "phone": "5551234567"
        })
        data = r.json()
        assert data["success"] == True
        print_test(f"Patient Login: {data['data']['name']}")
    except Exception as e:
        print_test(f"Patient Login: {e}", False)
    
    # Test 8: Get Patient Info
    try:
        r = requests.get(f"{BASE_URL}/patients/{user_id}")
        data = r.json()
        assert data["success"] == True
        print_test(f"Get Patient Info")
    except Exception as e:
        print_test(f"Get Patient Info: {e}", False)
    
    # Test 9: Patient Greeting
    try:
        r = requests.get(f"{BASE_URL}/patients/{user_id}/greeting")
        data = r.json()
        assert data["success"] == True
        print_test(f"Patient Greeting: {data['data']['greeting']}")
    except Exception as e:
        print_test(f"Patient Greeting: {e}", False)
    
    # Test 10: Book Appointment
    try:
        tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        r = requests.post(f"{BASE_URL}/appointments", json={
            "user_id": user_id,
            "doctor_id": doctor_id,
            "date": tomorrow,
            "time": "14:00",
            "reason": "API Test Appointment",
            "sync_calendar": False
        })
        data = r.json()
        assert data["success"] == True
        appointment_id = data["data"]["appointment_id"]
        print_test(f"Book Appointment (ID: {appointment_id})")
    except Exception as e:
        print_test(f"Book Appointment: {e}", False)
        return
    
    # Test 11: Get Patient Appointments
    try:
        r = requests.get(f"{BASE_URL}/appointments/{user_id}")
        data = r.json()
        assert data["success"] == True
        assert len(data["data"]) > 0
        print_test(f"Get Appointments ({len(data['data'])} found)")
    except Exception as e:
        print_test(f"Get Appointments: {e}", False)
    
    # Test 12: Get Doctor Appointments
    try:
        r = requests.get(f"{BASE_URL}/doctors/{doctor_id}/appointments?date=today")
        data = r.json()
        assert data["success"] == True
        print_test(f"Doctor Schedule ({len(data['data'])} appointments)")
    except Exception as e:
        print_test(f"Doctor Schedule: {e}", False)
    
    # Test 13: Add Medical Notes
    try:
        r = requests.post(f"{BASE_URL}/appointments/{appointment_id}/notes", json={
            "notes": "Test notes from API"
        })
        data = r.json()
        assert data["success"] == True
        print_test("Add Medical Notes")
    except Exception as e:
        print_test(f"Add Medical Notes: {e}", False)
    
    # Test 14: Get Doctor Patients
    try:
        r = requests.get(f"{BASE_URL}/doctors/{doctor_id}/patients")
        data = r.json()
        assert data["success"] == True
        print_test(f"Doctor Patients ({data['data']['total_count']} patients)")
    except Exception as e:
        print_test(f"Doctor Patients: {e}", False)
    
    # Test 15: Get Analytics
    try:
        start = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
        end = date.today().strftime("%Y-%m-%d")
        r = requests.get(f"{BASE_URL}/doctors/{doctor_id}/analytics?start_date={start}&end_date={end}")
        data = r.json()
        assert data["success"] == True
        print_test(f"Analytics (Completion: {data['data']['completion_rate']}%)")
    except Exception as e:
        print_test(f"Analytics: {e}", False)
    
    # Test 16: Update Patient Preferences
    try:
        r = requests.put(f"{BASE_URL}/patients/{user_id}/preferences", json={
            "email_notifications": True,
            "sms_reminders": True,
            "auto_sync_calendar": False
        })
        data = r.json()
        assert data["success"] == True
        print_test("Update Preferences")
    except Exception as e:
        print_test(f"Update Preferences: {e}", False)
    
    # Test 17: Cancel Appointment
    try:
        r = requests.put(f"{BASE_URL}/appointments/{appointment_id}/cancel")
        data = r.json()
        assert data["success"] == True
        print_test("Cancel Appointment")
    except Exception as e:
        print_test(f"Cancel Appointment: {e}", False)
    
    print("\n" + "="*60)
    print("✅ API Testing Complete!")
    print("="*60 + "\n")
    print("📡 API Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API server!")
        print("Make sure the server is running: cd api && python3 main.py")
        print("\n")
