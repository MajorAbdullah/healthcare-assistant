# 📘 Healthcare Assistant - Complete User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Patient Portal Guide](#patient-portal-guide)
4. [Doctor Portal Guide](#doctor-portal-guide)
5. [AI Medical Assistant](#ai-medical-assistant)
6. [Appointment Management](#appointment-management)
7. [Google Calendar Integration](#google-calendar-integration)
8. [Video Consultations](#video-consultations)
9. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is Healthcare Assistant?

Healthcare Assistant is an intelligent healthcare management system that combines:
- 🏥 **Appointment Scheduling** - Book and manage doctor appointments
- 🤖 **AI Medical Assistant** - Get instant answers to medical questions using RAG (Retrieval Augmented Generation)
- 📅 **Calendar Integration** - Automatic sync with Google Calendar
- 🎥 **Video Consultations** - Google Meet links for virtual appointments
- 📧 **Email Notifications** - Automatic reminders and confirmations
- 📊 **Doctor Dashboard** - Comprehensive patient management tools

### Key Features

✅ **For Patients:**
- Easy appointment booking with real-time availability
- AI-powered medical Q&A with verified medical sources
- Automatic calendar invites with Google Meet links
- Email notifications for appointments
- View complete appointment history
- Personalized greetings and memory management

✅ **For Doctors:**
- Complete patient dashboard with analytics
- Appointment management with notes
- Patient history and medical records
- Statistics and performance metrics
- Google Calendar synchronization
- Email notifications for new appointments

---

## Getting Started

### System Requirements

- **Internet Connection** - Required for all features
- **Modern Web Browser** - Chrome (recommended), Firefox, Safari, or Edge
- **Email Address** - For notifications and calendar invites
- **Google Account** (Optional) - For calendar sync

### Accessing the System

1. **Frontend:** `http://localhost:8080` (or your deployed URL)
2. **Backend API:** `http://localhost:8000`
3. **Choose your portal:**
   - **Patient Portal** - `/patient/auth`
   - **Doctor Portal** - `/doctor/auth`

---

## Patient Portal Guide

### 1. Registration & Login

#### First-Time Registration

1. Navigate to `http://localhost:8080/patient/auth`
2. Click "Register" tab
3. Fill in your details:
   - **Full Name:** Your complete name
   - **Email Address:** Valid email (will receive notifications)
   - **Phone Number:** Contact number
   - **Date of Birth:** For age verification
   - **Gender:** Male/Female/Other
4. Click "Register"
5. System creates your profile and logs you in automatically
6. Your `user_id` is stored in browser localStorage

**Example:**
```
Name: Syed Abdullah Shah
Email: abdullah@example.com
Phone: +92 300 1234567
DOB: 1990-01-15
Gender: Male
```

#### Returning Users - Login

1. Click "Login" tab
2. Enter your credentials:
   - Email address
   - Phone number
3. Click "Login"
4. Redirected to dashboard

### 2. Dashboard Overview

Your personalized dashboard shows:

```
┌─────────────────────────────────────────┐
│  Welcome Back, Syed Abdullah! 👋        │
├─────────────────────────────────────────┤
│  📅 Upcoming Appointments: 2            │
│  💬 AI Medical Assistant                │
│  📋 Appointment History                 │
│  ⚙️  Profile Settings                   │
└─────────────────────────────────────────┘
```

**Quick Stats:**
- Upcoming appointments count
- Recent consultations
- AI chat history
- Account preferences

### 3. Booking an Appointment (4-Step Wizard)

#### Step 1: Select Doctor

**What you see:**
```
Available Doctors:

┌──────────────────────────────────┐
│ Dr. Sarah Johnson               │
│ Cardiology                      │
│ ⭐⭐⭐⭐⭐ 4.8 Rating           │
│ Consultation: 30 mins           │
│ [Select Doctor]                 │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│ Dr. Michael Chen                │
│ Neurology                       │
│ ⭐⭐⭐⭐⭐ 4.9 Rating           │
│ Consultation: 30 mins           │
│ [Select Doctor]                 │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│ Dr. Emily Davis                 │
│ Pediatrics                      │
│ ⭐⭐⭐⭐⭐ 4.7 Rating           │
│ Consultation: 30 mins           │
│ [Select Doctor]                 │
└──────────────────────────────────┘
```

**How to choose:**
1. Review doctor specialties
2. Check ratings and experience
3. Click "Select Doctor" on preferred choice
4. System loads their availability

#### Step 2: Choose Date

**Interactive Calendar:**
```
        November 2025
  Su Mo Tu We Th Fr Sa
               1  2  3
   4  5  6  7  8  9 10
  11 12 13 14 15 16 17
  18 19 20 21 22 23 24
  25 26 27 28 29 30
  
  ✓ Available    ○ Fully Booked    × Past Date
```

**Features:**
- Past dates are disabled
- Fully booked days show different color
- Hover to see availability count
- Click date to view time slots

#### Step 3: Select Time Slot

**Available Slots Display:**
```
Available slots for Tuesday, November 19, 2025

Morning:
┌─────────┬─────────┬─────────┬─────────┐
│  09:00  │  09:30  │  10:00  │  10:30  │
└─────────┴─────────┴─────────┴─────────┘
┌─────────┬─────────┬─────────┬─────────┐
│  11:00  │  11:30  │  12:00  │  12:30  │
└─────────┴─────────┴─────────┴─────────┘

Afternoon:
┌─────────┬─────────┬─────────┬─────────┐
│  13:00  │  13:30  │  14:00  │  14:30  │
└─────────┴─────────┴─────────┴─────────┘
┌─────────┬─────────┬─────────┬─────────┐
│  15:00  │  15:30  │  16:00  │  16:30  │
└─────────┴─────────┴─────────┴─────────┘

Evening:
┌─────────┬─────────┐
│  17:00  │  17:30  │
└─────────┴─────────┘
```

**Real-time Availability:**
- System checks database for each slot
- Booked slots are grayed out and disabled
- Only available slots are clickable
- Duration shown (typically 30 minutes)

#### Step 4: Confirm & Book

**Review Screen:**
```
┌──────────────────────────────────────┐
│  Confirm Your Appointment            │
├──────────────────────────────────────┤
│  Doctor: Dr. Sarah Johnson           │
│          Cardiology                  │
│                                      │
│  Date:   Tuesday, Nov 19, 2025      │
│  Time:   16:30 (4:30 PM)            │
│          Duration: 30 minutes        │
│                                      │
│  Reason for Visit:                   │
│  ┌────────────────────────────────┐ │
│  │ Annual checkup and general     │ │
│  │ health assessment              │ │
│  └────────────────────────────────┘ │
│                                      │
│  [Go Back]  [Confirm Booking]       │
└──────────────────────────────────────┘
```

**What happens when you click "Confirm Booking":**

1. **Button shows loading state:**
   ```
   ⏳ Syncing to Calendar...
   ```

2. **Loading toast appears:**
   ```
   ⏳ Booking appointment and syncing to Google Calendar...
   ```

3. **Backend processes (20-25 seconds):**
   - Validates slot availability
   - Creates appointment in database
   - Generates Google Calendar event with timezone
   - Adds Google Meet video link
   - Sends email to patient
   - Sends email to doctor
   - Returns confirmation

4. **Success screen:**
   ```
   ┌──────────────────────────────────────┐
   │         ✅ Appointment Confirmed!     │
   │                                      │
   │  Your appointment has been           │
   │  successfully booked                 │
   │                                      │
   │  Doctor:  Dr. Sarah Johnson          │
   │  Date:    Nov 19, 2025              │
   │  Time:    16:30                      │
   │                                      │
   │  📧 Email sent with Google Meet link │
   │  📅 Added to Google Calendar         │
   │                                      │
   │  [Back to Dashboard]  [View Appts]  │
   └──────────────────────────────────────┘
   ```

### 4. AI Medical Assistant

#### Starting a Conversation

1. Click "AI Assistant" from dashboard
2. Chat interface opens
3. Type your medical question
4. Press Enter or click Send
5. AI responds with sources

#### How the AI Works

**Technology Stack:**
- **Model:** Google Gemini 2.5 Flash
- **Method:** RAG (Retrieval Augmented Generation)
- **Knowledge Base:** Medical documents in `data/medical_docs/`
- **Vector Database:** ChromaDB for semantic search
- **Embeddings:** Sentence transformers for text understanding

**Processing Flow:**
```
Your Question
    ↓
Embedding Creation (convert to vector)
    ↓
Vector Database Search (find relevant docs)
    ↓
Context Retrieval (get matching passages)
    ↓
AI Generation (Gemini creates answer)
    ↓
Source Citation (references documents)
    ↓
Response Displayed
```

#### Example Conversations

**Example 1: Symptom Analysis**
```
You: I have a persistent headache for 3 days with nausea. 
     What could be causing this?

AI Assistant: Based on the medical literature, persistent 
headaches with nausea can indicate several conditions:

🔍 Possible Causes:

1. **Migraine** (Most Likely)
   - Throbbing pain, often one-sided
   - Nausea and vomiting common
   - Sensitivity to light/sound
   - Duration: 4-72 hours

2. **Tension Headache with Gastric Issues**
   - Dull, pressing pain
   - Stress-related
   - Nausea from pain or separate GI issue

3. **Dehydration**
   - Reduced fluid intake
   - Electrolyte imbalance
   - Can cause both symptoms

4. **Medication Overuse Headache**
   - From frequent painkiller use
   - Rebound effect

⚠️ Warning Signs (Seek Immediate Care If):
- Sudden, severe "thunderclap" headache
- Fever and stiff neck (possible meningitis)
- Vision changes or weakness
- Headache after head injury
- Worst headache of your life

✓ Self-Care Recommendations:
1. Hydrate: 8-10 glasses of water daily
2. Rest in dark, quiet room
3. Cold compress on forehead
4. Avoid triggers (stress, certain foods)
5. Track symptoms in headache diary

📚 Sources:
- Migraine Classification.pdf, pages 15-18
- Headache Diagnosis Guide.pdf, pages 23-25
- Emergency Symptoms.pdf, page 8

💡 Next Steps:
If symptoms persist >3 days or worsen, I recommend 
booking an appointment with a neurologist.

Would you like me to help you book an appointment?
```

**Example 2: Medication Query**
```
You: Can I take ibuprofen and acetaminophen together?

AI Assistant: Yes, it is generally safe to take 
ibuprofen and acetaminophen (paracetamol) together.

✓ Why It's Safe:
- Different drug classes (NSAID vs analgesic)
- Different mechanisms of action
- Minimal drug interaction
- Often used in combination for better pain relief

📋 Recommended Dosing:

Ibuprofen:
- Adult dose: 200-400mg every 6-8 hours
- Maximum: 1200mg/day (OTC) or 2400mg (prescription)
- Take with food

Acetaminophen:
- Adult dose: 500-1000mg every 4-6 hours
- Maximum: 4000mg/day
- Can take with or without food

💊 Combination Strategy:
Option 1 - Alternating:
  - Hour 0: Ibuprofen 400mg
  - Hour 3: Acetaminophen 500mg
  - Hour 6: Ibuprofen 400mg
  - Hour 9: Acetaminophen 500mg

Option 2 - Together:
  - Take both at same time for severe pain
  - Don't exceed daily limits for either drug

⚠️ Precautions:
- Don't exceed maximum daily doses
- Check other meds for acetaminophen (many cold 
  medicines contain it)
- Avoid ibuprofen if you have stomach ulcers, 
  kidney issues, or bleeding disorders
- Consult doctor if pain persists >10 days

📚 Sources:
- Pain Management Guidelines.pdf, pages 34-37
- Drug Interactions Database.pdf, page 156
- NSAID Safety Guide.pdf, pages 12-14

⚠️ Important: This is general information. Always 
follow your doctor's specific instructions if you 
have a prescription or medical condition.

Do you have any other questions about pain management?
```

#### AI Capabilities

**What the AI CAN do:**
✅ Provide general medical information
✅ Explain symptoms and possible causes
✅ Offer self-care recommendations
✅ Explain medication uses and dosages
✅ Provide first aid guidance
✅ Educate about diseases and conditions
✅ Cite sources from medical literature
✅ Suggest when to see a doctor

**What the AI CANNOT do:**
❌ Diagnose specific medical conditions
❌ Prescribe medications
❌ Replace professional medical advice
❌ Handle medical emergencies
❌ Provide personalized treatment plans
❌ Access your medical records
❌ Make definitive medical decisions

#### AI Safety Features

**Disclaimer Always Shown:**
```
⚠️ MEDICAL DISCLAIMER
This AI provides general medical information only.
It is NOT a substitute for professional medical 
advice, diagnosis, or treatment. Always seek the 
advice of your physician or qualified health 
provider with questions about medical conditions.

🚨 EMERGENCIES: Call 911 or local emergency services
```

**Content Filtering:**
- Refuses to diagnose conditions definitively
- Always recommends seeing doctor for serious symptoms
- Won't provide dangerous medical advice
- Cites authoritative medical sources
- Provides evidence-based information

### 5. Managing Appointments

#### Viewing All Appointments

```
My Appointments

┌──────────────────────────────────────────┐
│ 📅 Upcoming                              │
├──────────────────────────────────────────┤
│ Nov 19, 2025 at 16:30                   │
│ Dr. Sarah Johnson - Cardiology          │
│ Reason: Annual checkup                  │
│ Status: Scheduled                       │
│ 🎥 [Join Google Meet]                    │
│ [Cancel] [View Details]                 │
├──────────────────────────────────────────┤
│ Nov 26, 2025 at 14:00                   │
│ Dr. Emily Davis - Pediatrics            │
│ Reason: Follow-up                       │
│ Status: Scheduled                       │
│ 🎥 [Join Google Meet]                    │
│ [Cancel] [View Details]                 │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ 📋 Past Appointments                     │
├──────────────────────────────────────────┤
│ Oct 15, 2025 at 10:00                   │
│ Dr. Michael Chen - Neurology            │
│ Reason: Headache consultation           │
│ Status: Completed                       │
│ Notes: Prescribed medication...         │
│ [View Details]                          │
└──────────────────────────────────────────┘
```

#### Appointment Details View

```
┌──────────────────────────────────────────┐
│ Appointment Details                      │
├──────────────────────────────────────────┤
│ Appointment ID: 36                       │
│                                          │
│ 📅 Date: Tuesday, November 26, 2025     │
│ ⏰ Time: 14:00 - 14:30 (2:00 PM)        │
│                                          │
│ 👨‍⚕️ Doctor Information:                  │
│   Name: Dr. Emily Davis                  │
│   Specialty: Pediatrics                  │
│   Email: emily.davis@healthcare.com      │
│                                          │
│ 👤 Patient: Syed Abdullah Shah           │
│                                          │
│ 📝 Reason: Follow-up consultation        │
│                                          │
│ 📊 Status: Scheduled                     │
│                                          │
│ 🎥 Video Consultation:                   │
│    [Join Google Meet]                    │
│                                          │
│ 📧 Notifications:                        │
│    ✓ Calendar invite sent                │
│    ✓ Email confirmation sent             │
│    ✓ Reminder will be sent 24hrs before │
│                                          │
│ [Cancel Appointment] [Back to List]     │
└──────────────────────────────────────────┘
```

#### Cancelling an Appointment

1. Click "Cancel" on appointment card
2. Confirmation dialog appears:
   ```
   ⚠️ Cancel Appointment?
   
   Are you sure you want to cancel your appointment?
   
   Doctor: Dr. Emily Davis
   Date: November 26, 2025
   Time: 14:00
   
   This action cannot be undone. The doctor will be
   notified of the cancellation.
   
   [Go Back]  [Yes, Cancel]
   ```
3. Click "Yes, Cancel"
4. System processes cancellation:
   - Updates appointment status to "cancelled"
   - Frees up time slot
   - Sends notification to doctor
   - Updates Google Calendar event
   - Sends confirmation email
5. Success message:
   ```
   ✓ Appointment Cancelled Successfully
   
   Your appointment has been cancelled. The time slot
   is now available for other patients. You may book
   a new appointment at any time.
   ```

---

## Doctor Portal Guide

### 1. Doctor Login

**Process:**
1. Navigate to `http://localhost:8080/doctor/auth`
2. Select doctor from dropdown:
   - Dr. Sarah Johnson (ID: 1) - Cardiology
   - Dr. Michael Chen (ID: 2) - Neurology
   - Dr. Emily Davis (ID: 3) - Pediatrics
3. Click "Login"
4. Redirected to doctor dashboard

### 2. Doctor Dashboard

**Overview Screen:**
```
┌─────────────────────────────────────────────────┐
│  Welcome, Dr. Sarah Johnson                     │
│  Cardiology Specialist                          │
│  📧 sarah.johnson@healthcare.com                │
├─────────────────────────────────────────────────┤
│  📊 Statistics                                   │
│  ┌─────────────┬─────────────┬────────────────┐│
│  │ Total       │ Total       │ Upcoming       ││
│  │ Patients    │ Appts       │ Appts          ││
│  │    156      │    342      │     12         ││
│  └─────────────┴─────────────┴────────────────┘│
│  ┌─────────────┐                                │
│  │ Completed   │                                │
│  │ Today: 3    │                                │
│  └─────────────┘                                │
├─────────────────────────────────────────────────┤
│  📅 Today's Schedule - November 19, 2025        │
├─────────────────────────────────────────────────┤
│  09:00 - 09:30                                  │
│  John Doe                                       │
│  📧 john@example.com                             │
│  📝 Annual checkup                               │
│  [View] [Add Notes] [Join Meet]                 │
├─────────────────────────────────────────────────┤
│  14:00 - 14:30                                  │
│  Jane Smith                                     │
│  📧 jane@example.com                             │
│  📝 Follow-up cardiology                         │
│  [View] [Add Notes] [Join Meet]                 │
├─────────────────────────────────────────────────┤
│  16:30 - 17:00                                  │
│  Syed Abdullah Shah                             │
│  📧 abdullah@example.com                         │
│  📝 Annual checkup                               │
│  [View] [Add Notes] [Join Meet]                 │
└─────────────────────────────────────────────────┘
```

### 3. Appointment Management

#### Viewing All Appointments

**Filter Options:**
```
┌─────────────────────────────────────────┐
│ Appointments                            │
├─────────────────────────────────────────┤
│ Filter by:                              │
│ 📅 Date: [Today ▼] [This Week] [Month] │
│ 📊 Status: [All ▼] [Scheduled]         │
│           [Completed] [Cancelled]       │
│ 🔍 Search: [Patient name...]           │
└─────────────────────────────────────────┘
```

#### Appointment Card (Doctor View)

```
┌──────────────────────────────────────────┐
│ 16:30 - 17:00                           │
│ Appointment #36                          │
├──────────────────────────────────────────┤
│ 👤 Patient: Syed Abdullah Shah           │
│ 📧 Email: abdullah@example.com           │
│ 📱 Phone: +92 300 1234567               │
│ 🎂 DOB: January 15, 1990 (35 years)    │
│ ⚧ Gender: Male                          │
├──────────────────────────────────────────┤
│ 📝 Reason: Annual checkup and general    │
│           health assessment              │
│                                          │
│ 📊 Status: Scheduled                     │
│ 📅 Date: November 19, 2025              │
│ 🎥 Google Meet: Available                │
├──────────────────────────────────────────┤
│ 📋 Previous Visits: 2                    │
│    Last visit: Aug 15, 2025             │
├──────────────────────────────────────────┤
│ [View History] [Add Notes] [Join Meet]  │
│ [Mark Complete] [Cancel]                │
└──────────────────────────────────────────┘
```

#### Adding Medical Notes

**Process:**
1. Click "Add Notes" on appointment
2. Notes editor opens:
   ```
   ┌──────────────────────────────────────┐
   │ Medical Notes - Appointment #36      │
   │ Patient: Syed Abdullah Shah          │
   │ Date: November 19, 2025              │
   ├──────────────────────────────────────┤
   │ Chief Complaint:                     │
   │ ┌──────────────────────────────────┐ │
   │ │ Annual health checkup            │ │
   │ └──────────────────────────────────┘ │
   │                                      │
   │ Vital Signs:                         │
   │ ┌──────────────────────────────────┐ │
   │ │ BP: 120/80 mmHg                  │ │
   │ │ HR: 72 bpm                       │ │
   │ │ Temp: 98.6°F                     │ │
   │ │ Weight: 75 kg                    │ │
   │ │ Height: 175 cm                   │ │
   │ └──────────────────────────────────┘ │
   │                                      │
   │ Examination Findings:                │
   │ ┌──────────────────────────────────┐ │
   │ │ General appearance: Healthy      │ │
   │ │ Heart: Normal rhythm, no murmurs │ │
   │ │ Lungs: Clear bilaterally         │ │
   │ │ Abdomen: Soft, non-tender        │ │
   │ └──────────────────────────────────┘ │
   │                                      │
   │ Diagnosis:                           │
   │ ┌──────────────────────────────────┐ │
   │ │ Healthy individual               │ │
   │ │ No acute issues identified       │ │
   │ └──────────────────────────────────┘ │
   │                                      │
   │ Treatment Plan:                      │
   │ ┌──────────────────────────────────┐ │
   │ │ - Continue healthy lifestyle     │ │
   │ │ - Regular exercise 30min/day     │ │
   │ │ - Balanced diet                  │ │
   │ │ - Annual follow-up in 12 months  │ │
   │ └──────────────────────────────────┘ │
   │                                      │
   │ Medications:                         │
   │ ┌──────────────────────────────────┐ │
   │ │ None prescribed                  │ │
   │ └──────────────────────────────────┘ │
   │                                      │
   │ [Save Notes] [Save & Email Patient] │
   └──────────────────────────────────────┘
   ```
3. Fill in medical notes
4. Click "Save Notes" or "Save & Email Patient"
5. Notes stored in database
6. Accessible in patient history

#### Updating Appointment Status

**Available Statuses:**
1. **Scheduled** - Upcoming appointment
2. **Completed** - Patient attended, consultation done
3. **Cancelled** - Appointment cancelled
4. **No-show** - Patient didn't attend

**How to Update:**
```
[Mark as: Completed ▼]
         - Scheduled
         - Completed  ✓
         - Cancelled
         - No-show
```

### 4. Patient History

**Complete Patient View:**
```
┌──────────────────────────────────────────┐
│ Patient Profile                          │
├──────────────────────────────────────────┤
│ Name: Syed Abdullah Shah                 │
│ Email: abdullah@example.com              │
│ Phone: +92 300 1234567                  │
│ DOB: January 15, 1990 (35 years)       │
│ Gender: Male                             │
├──────────────────────────────────────────┤
│ 📊 Appointment History (3 visits)        │
├──────────────────────────────────────────┤
│ Nov 19, 2025 - 16:30                    │
│ Status: Scheduled                        │
│ Reason: Annual checkup                   │
├──────────────────────────────────────────┤
│ Aug 15, 2025 - 10:00                    │
│ Status: Completed ✓                      │
│ Reason: Follow-up                        │
│ 📝 Notes: Blood pressure normalized.     │
│          Continue current medication.    │
│          Next visit in 3 months.         │
├──────────────────────────────────────────┤
│ May 10, 2025 - 14:30                    │
│ Status: Completed ✓                      │
│ Reason: Initial consultation             │
│ 📝 Notes: Elevated BP: 140/90.           │
│          Started on lisinopril 10mg.     │
│          Lifestyle modifications advised. │
│          Follow-up in 6 weeks.           │
└──────────────────────────────────────────┘
```

### 5. Analytics Dashboard

**Monthly Statistics:**
```
┌─────────────────────────────────────────┐
│ 📊 Performance Analytics                │
│ Dr. Sarah Johnson - Cardiology          │
├─────────────────────────────────────────┤
│ This Month (November 2025):             │
│                                         │
│ Total Appointments: 45                  │
│ ├─ Completed: 38 (84%)                 │
│ ├─ Scheduled: 5 (11%)                  │
│ ├─ Cancelled: 1 (2%)                   │
│ └─ No-shows: 1 (2%)                    │
│                                         │
│ New Patients: 12                        │
│ Returning Patients: 33                  │
│                                         │
│ Average Consultation: 28 minutes        │
│                                         │
│ Patient Satisfaction: 4.8/5.0 ⭐        │
├─────────────────────────────────────────┤
│ 📈 Appointment Trends                   │
│                                         │
│     Appointments per Day                │
│ 50│                        ╱╲           │
│ 40│                    ╱╲ ╱  ╲          │
│ 30│            ╱╲    ╱  ╲╱    ╲         │
│ 20│      ╱╲  ╱  ╲  ╱            ╲       │
│ 10│  ╱╲╱  ╲╱    ╲╱              ╲      │
│  0└─────────────────────────────────    │
│    Mon Tue Wed Thu Fri Sat Sun         │
├─────────────────────────────────────────┤
│ 🕐 Peak Hours: 14:00 - 17:00           │
│ 📅 Busiest Day: Tuesday                │
│ 📉 Cancellation Rate: 2.2%             │
└─────────────────────────────────────────┘
```

---

## Google Calendar Integration

### How It Works (Technical Flow)

**1. Appointment Booking Triggers Calendar Sync:**
```
Patient books appointment
    ↓
Backend API receives request
    ↓
Validates slot availability
    ↓
Creates appointment in SQLite database
    ↓
Triggers calendar_integration.py
    ↓
Creates timezone-aware datetime (Asia/Karachi)
    ↓
Formats as ISO 8601: "2025-11-19T16:30:00+05:00"
    ↓
Calls Pipedream MCP
    ↓
Pipedream communicates with Google Calendar API
    ↓
Creates event with Google Meet link
    ↓
Sends email notifications
    ↓
Returns event ID to backend
    ↓
Stores event ID in database
    ↓
Returns success to frontend
```

**2. What Gets Created in Google Calendar:**
```
Event Title: Appointment: Syed Abdullah Shah
Start: 2025-11-19T16:30:00+05:00
End: 2025-11-19T17:00:00+05:00
Timezone: Asia/Karachi (PKT)

Description:
Patient: Syed Abdullah Shah
Email: abdullah@example.com
Doctor: Dr. Sarah Johnson (Cardiology)
Reason: Annual checkup

Appointment ID: 36

Location: Healthcare Center

Attendees:
- abdullah@example.com
- sarah.johnson@healthcare.com

Conference: Google Meet (auto-generated link)
```

### Email Notification Details

**Confirmation Email to Patient:**
```
From: Google Calendar <calendar-notification@google.com>
To: abdullah@example.com
Subject: Invitation: Appointment: Syed Abdullah Shah @ 
         Tue Nov 19, 2025 4:30pm - 5pm (PKT) 
         (abdullah@example.com)

You have been invited to the following event:

Appointment: Syed Abdullah Shah

When:
Tue Nov 19, 2025 4:30pm – 5pm Pakistan Standard Time - Karachi

Where:
Healthcare Center

Calendar:
pinkpantherking20@gmail.com

Who:
• abdullah@example.com - organizer
• sarah.johnson@healthcare.com

Joining info:
Join with Google Meet
https://meet.google.com/xxx-xxxx-xxx

[Yes] [No] [Maybe]    [More options ▼]

Details:
Patient: Syed Abdullah Shah
Email: abdullah@example.com
Doctor: Dr. Sarah Johnson (Cardiology)
Reason: Annual checkup

Appointment ID: 36
```

### Timezone Handling

**Problem Solved:**
- Previous issue: Dates were shifting (Nov 19 → Nov 18)
- **Root Cause:** Naive datetime without timezone info
- **Solution:** Use pytz with Asia/Karachi timezone

**Implementation:**
```python
import pytz

# Create Pakistan timezone
pkt_tz = pytz.timezone('Asia/Karachi')

# Parse appointment date/time
dt = datetime.strptime("2025-11-19 16:30", "%Y-%m-%d %H:%M")

# Localize to Pakistan timezone
dt_aware = pkt_tz.localize(dt)
# Result: 2025-11-19 16:30:00+05:00

# Convert to ISO 8601
iso_string = dt_aware.isoformat()
# Result: "2025-11-19T16:30:00+05:00"
```

**Why This Works:**
- `+05:00` explicitly tells Google Calendar the timezone offset
- No ambiguity about which timezone the time is in
- Google Calendar displays correctly in user's local timezone
- Prevents date shifting across timezone boundaries

---

## Video Consultations (Google Meet)

### For Patients

**Before Appointment:**
1. Check email for calendar invite
2. Find Google Meet link
3. Test camera/microphone 5 minutes early
4. Ensure good internet connection (minimum 5 Mbps)

**Joining Process:**
```
Option 1: From Email
└─ Open calendar invite email
   └─ Click "Join with Google Meet"
      └─ Browser opens Google Meet
         └─ Allow camera/microphone permissions
            └─ Click "Join now"

Option 2: From Google Calendar
└─ Open Google Calendar
   └─ Click on appointment event
      └─ Click "Join with Google Meet"
         └─ Same as above

Option 3: From Healthcare App
└─ Go to "My Appointments"
   └─ Click appointment card
      └─ Click "Join Google Meet"
         └─ Same as above
```

**During Consultation:**
- 🎥 Keep camera on for better communication
- 🎤 Mute when not speaking (reduces background noise)
- 💬 Use chat for links or notes
- 📝 Doctor may share screen for diagrams/results
- ⏱️ Typical duration: 30 minutes

**Controls:**
```
┌────────────────────────────────────────┐
│  🎥 Camera   🎤 Mic   📞 Leave Call   │
│  💬 Chat     ✋ Raise Hand   ⚙️ Settings │
└────────────────────────────────────────┘
```

### For Doctors

**Best Practices:**
1. **Review Patient History** before call
2. **Join 2-3 minutes early**
3. **Professional Background** (or use virtual background)
4. **Take Notes** during consultation
5. **Share Screen** if explaining results/diagrams
6. **Record Consultation** (with patient consent)

**Post-Consultation:**
1. Add medical notes immediately
2. Mark appointment as "Completed"
3. Send prescription via email if needed
4. Schedule follow-up if required

---

## Troubleshooting

### Common Issues

#### 1. Login Problems

**Symptom:** Cannot log in with email/phone

**Solutions:**
```
✓ Verify email is exactly as registered
✓ Check phone number format (+92 300 1234567)
✓ Clear browser cache and cookies
✓ Try incognito/private mode
✓ Use different browser
✓ Register new account if first time
```

#### 2. No Available Slots

**Symptom:** All time slots are grayed out

**Solutions:**
```
✓ Try different date (doctor may be fully booked)
✓ Try different doctor
✓ Check if it's a weekend (doctors may not work)
✓ Wait - slots open up when patients cancel
```

#### 3. Calendar Event Not Appearing

**Symptom:** Appointment booked but no calendar event

**Diagnosis:**
```
Check email → Has calendar invite? 
    ├─ Yes → Check spam/junk folder
    │        └─ Mark as "Not Spam"
    │        └─ Click .ics attachment to add manually
    └─ No → Check email address in profile
            └─ Update to Gmail address
            └─ Rebook appointment
```

**Backend Logs to Check:**
```
📅 Creating calendar event for appointment #36...
   Date: 2025-11-26
   Time: 14:00 - 14:30
   📧 Email notifications will be sent to attendees
   🎥 Google Meet link will be added
✓ Calendar event created with Google Meet link
✓ Email invitations sent to attendees
✓ Calendar event created: event_1761735609.98377
```

#### 4. Google Meet Link Not Working

**Symptom:** Click Meet link but can't join

**Solutions:**
```
Timing:
├─ Too Early? → Join 15 minutes before, not earlier
├─ Too Late? → Doctor may have ended meeting
└─ On Time? → Continue below

Browser:
├─ Use Chrome (recommended)
├─ Update to latest version
└─ Enable camera/microphone permissions

Permissions:
├─ Browser asks to allow camera → Click "Allow"
├─ Browser asks to allow mic → Click "Allow"
└─ Check system settings if blocked

Link:
├─ Use link from latest email
├─ Try link from Google Calendar event
└─ Contact doctor if all fails
```

#### 5. AI Assistant Not Responding

**Symptom:** Type message but no response

**Debugging:**
```
1. Check internet connection
   └─ Reload page if disconnected

2. Check backend server
   └─ Should be running on port 8000
   └─ Check terminal for errors

3. Check browser console (F12)
   └─ Look for red errors
   └─ Screenshot and report to support

4. Try again
   └─ Reload page
   └─ Login again
   └─ Start new chat
```

**Backend Requirements:**
```bash
# Ensure backend is running:
cd "/Users/abdullah/my projects/pipedream"
source .venv/bin/activate
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Check for errors in terminal
# Should see:
✓ Calendar integration enabled (Direct Pipedream MCP)
INFO: Application startup complete.
```

#### 6. Frontend Not Loading

**Symptom:** Blank page or loading forever

**Solutions:**
```bash
# Check if frontend server is running:
cd "/Users/abdullah/my projects/pipedream/Frontend"
npm run dev
# Should see:
VITE v5.x.x ready in XXX ms
➜  Local:   http://localhost:8080/

# If not running, start it:
npm install  # Install dependencies if needed
npm run dev  # Start development server
```

---

## System Architecture Overview

### Technology Stack

**Frontend:**
- React 18 with TypeScript
- Vite for fast development
- Tailwind CSS for styling
- Shadcn UI components
- React Router for navigation
- Axios for API calls

**Backend:**
- Python 3.13
- FastAPI for REST API
- SQLite for relational data
- ChromaDB for vector storage
- Google Gemini 2.5 Flash for AI
- Uvicorn ASGI server

**Integrations:**
- Google Calendar API (via Pipedream MCP)
- Google Meet (automatic with calendar)
- Email notifications (via Google Calendar)

**AI/ML:**
- RAG (Retrieval Augmented Generation)
- Sentence Transformers for embeddings
- ChromaDB for semantic search
- Google Gemini for generation

### Data Flow

**Appointment Booking:**
```
Frontend (React)
    ↓ HTTP POST /api/v1/appointments
Backend (FastAPI)
    ↓ Validate & Store
Database (SQLite)
    ↓ Trigger Calendar Sync
Calendar Integration (Python)
    ↓ MCP Call
Pipedream
    ↓ API Call
Google Calendar
    ↓ Email Notification
Patient & Doctor Inboxes
```

**AI Chat:**
```
User Question (Frontend)
    ↓ HTTP POST /api/v1/chat
Backend (FastAPI)
    ↓ Create Embedding
RAG Engine (Python)
    ↓ Semantic Search
Vector Database (ChromaDB)
    ↓ Retrieved Context
Google Gemini API
    ↓ Generate Answer
Backend (FastAPI)
    ↓ HTTP Response
Frontend (React)
    ↓ Display
User Sees Answer with Sources
```

---

## Frequently Asked Questions

### General

**Q: Is my data secure?**
A: Yes. All data is encrypted in transit (HTTPS) and at rest. We follow healthcare data protection best practices.

**Q: Can I use this on mobile?**
A: Yes! The web interface is responsive and works on phones and tablets.

**Q: Do I need a Google account?**
A: Not required, but recommended for calendar sync. You'll still receive emails without Google account.

### Appointments

**Q: How far in advance can I book?**
A: Up to 3 months, depending on doctor availability.

**Q: Can I reschedule?**
A: Yes. Cancel current appointment and book a new one.

**Q: What if I'm late?**
A: Join when you can. Doctor may have limited time if other appointments are scheduled.

**Q: Can I book for someone else?**
A: Each person should have their own account for proper medical records.

### AI Assistant

**Q: Can the AI diagnose me?**
A: No. It provides general information only. Always consult a real doctor for diagnosis.

**Q: Where does the AI get its information?**
A: From verified medical documents in our database, cited in responses.

**Q: Is the AI always right?**
A: The AI provides evidence-based information but can make mistakes. Verify with healthcare provider.

---

## Support & Contact

**Email:** support@healthcareassistant.com
**Response Time:** Within 24 hours

**Phone:** +92 XXX XXXXXXX
**Hours:** Monday-Friday, 9 AM - 5 PM PKT

**Emergency:** For medical emergencies, call 911 or local emergency services. DO NOT use this system.

---

**Document Version:** 2.0
**Last Updated:** October 29, 2025
**Author:** Healthcare Assistant Team

---

*Thank you for using Healthcare Assistant! 🏥💙*
