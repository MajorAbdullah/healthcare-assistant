# 📖 Healthcare Assistant - User Guide

**Version**: 1.0.0  
**Last Updated**: October 28, 2025  

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [User Flows](#user-flows)
3. [Feature Guides](#feature-guides)
4. [FAQ](#faq)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Getting Started

### Prerequisites

Before using the Healthcare Assistant, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ All dependencies installed (`pip install -r requirements.txt`)
- ✅ Environment variables configured (`.env` file)

### Launching the Application

**Option 1: Quick Start Menu**
```bash
python3 start.py
```
This shows all available options and demos.

**Option 2: Main Application**
```bash
python3 healthcare_assistant.py
```
This launches the full Healthcare Assistant.

---

## 👥 User Flows

### Flow 1: First-Time User - Complete Journey

**Scenario**: Sarah is a new patient who wants to learn about strokes and book an appointment.

#### Step 1: Launch & Login
```bash
python3 healthcare_assistant.py
```

**What you'll see:**
```
╔══════════════════════════════════════════════════════════════╗
║           🏥  HEALTHCARE ASSISTANT SYSTEM  🏥                ║
║     AI-Powered Medical Q&A + Appointment Scheduling          ║
╚══════════════════════════════════════════════════════════════╝

Welcome! Let's get you started.
```

**What to do:**
1. Enter your **name**: `Sarah Johnson`
2. Enter your **email**: `sarah@email.com`
3. Enter your **phone**: `555-1234` (optional)

**Result:**
```
👋 Welcome
Welcome, Sarah! I'm your healthcare assistant.
```

---

#### Step 2: Ask a Medical Question

**From the main menu, select:** `1` (Ask a medical question)

**Example questions you can ask:**
- "What are the warning signs of a stroke?"
- "How can I prevent a stroke?"
- "What should I do if someone is having a stroke?"
- "What is the recovery process after a stroke?"

**Sample Interaction:**
```
Your question: What are the warning signs of a stroke?

Searching medical knowledge base...

🤖 Answer:
Warning signs of a stroke include:

• Sudden numbness or weakness in face, arm, or leg [1]
• Sudden confusion or trouble speaking [1]
• Sudden trouble seeing in one or both eyes [2]
• Sudden trouble walking or loss of balance [1]
• Sudden severe headache with no known cause [2]

Remember the acronym BE-FAST:
- Balance: Loss of balance or coordination
- Eyes: Vision problems
- Face: Face drooping
- Arms: Arm weakness
- Speech: Speech difficulty
- Time: Time to call emergency services

Sources:
[1] WHO Stroke Fact Sheet - Symptoms
[2] Mayo Clinic Stroke Guide - Warning Signs
[3] CDC Stroke Prevention - Recognition
```

**What happens behind the scenes:**
- ✅ Your question is saved to conversation history
- ✅ AI searches medical knowledge base
- ✅ Answer is generated with citations
- ✅ Context is stored for future personalization

---

#### Step 3: Book an Appointment

**From the main menu, select:** `2` (Book an appointment)

**The booking process:**

**3a. Select a Doctor**
```
👨‍⚕️ Available Doctors
┌────┬───────────────────┬───────────────────────────────┬──────────┐
│ ID │ Name              │ Specialty                     │ Duration │
├────┼───────────────────┼───────────────────────────────┼──────────┤
│ 1  │ Dr. Sarah Johnson │ Neurology - Stroke Specialist │ 30 min   │
│ 2  │ Dr. Michael Chen  │ Emergency Medicine            │ 30 min   │
│ 3  │ Dr. Aisha Khan    │ Rehabilitation & Recovery     │ 30 min   │
└────┴───────────────────┴───────────────────────────────┴──────────┘

Select doctor ID: 1
```

**3b. Choose a Date**
```
Appointment date (YYYY-MM-DD) [2025-10-29]: 
Press Enter for tomorrow, or type a different date
```

**3c. Select a Time Slot**
```
🕐 Available Times - 2025-10-29
┌──────┬────────────────┬──────────┐
│ Slot │ Time           │ Duration │
├──────┼────────────────┼──────────┤
│  1   │ 09:00 - 09:30  │ 30 min   │
│  2   │ 09:30 - 10:00  │ 30 min   │
│  3   │ 10:00 - 10:30  │ 30 min   │
│  4   │ 10:30 - 11:00  │ 30 min   │
│  5   │ 11:00 - 11:30  │ 30 min   │
│  6   │ 11:30 - 12:00  │ 30 min   │
└──────┴────────────────┴──────────┘

💡 You prefer morning appointments

Select slot number: 2
```

**3d. Provide Reason**
```
Reason for appointment [Consultation]: Stroke prevention consultation
```

**3e. Confirm Booking**
```
📋 Confirmation

Doctor: Dr. Sarah Johnson (Neurology - Stroke Specialist)
Date: 2025-10-29
Time: 09:30 - 10:00
Duration: 30 minutes
Reason: Stroke prevention consultation

Confirm booking? [Y/n]: Y
```

**3f. Calendar Sync**
```
✓ Appointment booked successfully! (ID: 11)

Sync to Google Calendar? [Y/n]: Y

Syncing to calendar...

✓ Synced to Google Calendar!
```

**What you receive:**
- ✅ Appointment confirmation
- ✅ Google Calendar event created
- ✅ Email notification sent
- ✅ Reminder set (30 minutes before)
- ✅ Booking saved to your history

---

#### Step 4: View Your Appointments

**From the main menu, select:** `3` (View my appointments)

**What you'll see:**
```
📅 Upcoming Appointments
┌────┬────────────┬──────────────┬───────────────────┬───────────┐
│ ID │ Date       │ Time         │ Doctor            │ Status    │
├────┼────────────┼──────────────┼───────────────────┼───────────┤
│ 11 │ 2025-10-29 │ 09:30-10:00  │ Dr. Sarah Johnson │ SCHEDULED │
└────┴────────────┴──────────────┴───────────────────┴───────────┘

📜 Past Appointments
┌────────────┬───────────────────┬───────────┐
│ Date       │ Doctor            │ Status    │
├────────────┼───────────────────┼───────────┤
│ 2025-10-15 │ Dr. Michael Chen  │ COMPLETED │
└────────────┴───────────────────┴───────────┘
```

---

#### Step 5: Get Personalized Suggestions

**From the main menu, select:** `6` (Get personalized suggestions)

**What you'll see:**
```
Based on your history:

1. 💡 You usually see Dr. Sarah Johnson - would you like to book with them again?
2. ⏰ You prefer morning appointments - I can show you morning slots.
3. 📚 You've asked about: stroke, prevention - would you like to learn more?

📊 Insights

Your Appointment Patterns:
Total Appointments: 2
Preferred Time: Morning
Time Distribution: Morning: 2, Afternoon: 0, Evening: 0
```

---

### Flow 2: Returning User - Quick Appointment

**Scenario**: John is a returning patient who wants to quickly book a follow-up.

#### Step 1: Launch & Quick Login
```bash
python3 healthcare_assistant.py
```

**Enter your details:**
- Name: `John Smith`
- Email: `john@email.com`
- Phone: `555-9999`

**You'll see:**
```
👋 Welcome

Welcome back!
📅 Reminder: You have an appointment TOMORROW at 10:00 with Dr. Aisha Khan.
```

The system remembers:
- ✅ Your name and preferences
- ✅ Your upcoming appointments
- ✅ Your conversation history
- ✅ Your favorite doctors

#### Step 2: Quick Booking

**Select:** `2` (Book an appointment)

**System shows your preference:**
```
💡 You usually see Dr. Aisha Khan

Select doctor ID [3]: ← Just press Enter!
```

**System suggests your preferred time:**
```
💡 You prefer afternoon appointments

Available Times:
  1. 14:00 - 14:30 ← Afternoon slot highlighted
  2. 14:30 - 15:00
  3. 15:00 - 15:30
```

**Result:** Booked in under 1 minute! ⚡

---

### Flow 3: Research & Learning

**Scenario**: Maria wants to learn about stroke prevention before her appointment.

#### Step 1: Ask Multiple Questions

**Question 1:**
```
Your question: What causes strokes?

🤖 Answer:
Strokes are caused by:
• Blocked blood flow (ischemic stroke) [1]
• Burst blood vessels (hemorrhagic stroke) [2]
• Temporary blockages (TIA or mini-stroke) [1]
...
```

**Question 2:**
```
Your question: How can I prevent strokes?

🤖 Answer:
Prevention strategies include:
• Control blood pressure [1]
• Manage diabetes [2]
• Quit smoking [1]
• Exercise regularly [3]
...
```

#### Step 2: Review Conversation History

**Select:** `5` (View conversation history)

**What you'll see:**
```
💬 Recent Conversations
┌─────────────────┬─────────────┬──────────────────────────────────┐
│ Time            │ Role        │ Message                          │
├─────────────────┼─────────────┼──────────────────────────────────┤
│ 2025-10-28 14:30│ 🤖 assistant│ Prevention strategies include... │
│ 2025-10-28 14:30│ 👤 user     │ How can I prevent strokes?       │
│ 2025-10-28 14:25│ 🤖 assistant│ Strokes are caused by...         │
│ 2025-10-28 14:25│ 👤 user     │ What causes strokes?             │
└─────────────────┴─────────────┴──────────────────────────────────┘

Total: 8 conversations over 2 days
```

---

### Flow 4: Checking Doctor Availability

**Scenario**: You want to see when a specific doctor is free.

#### Step 1: Check Availability

**From main menu, select:** `4` (Check doctor availability)

**Select doctor:**
```
1. Dr. Sarah Johnson - Neurology - Stroke Specialist
2. Dr. Michael Chen - Emergency Medicine
3. Dr. Aisha Khan - Rehabilitation & Recovery

Select doctor ID: 1
```

**Choose date:**
```
Date (YYYY-MM-DD) [2025-10-29]: 2025-11-01
```

**View available slots:**
```
Checking availability...

✓ Found 14 available slots:

  1. 09:00 - 09:30
  2. 09:30 - 10:00
  3. 10:00 - 10:30
  4. 10:30 - 11:00
  5. 11:00 - 11:30
  6. 11:30 - 12:00
  7. 13:00 - 13:30
  8. 13:30 - 14:00
  9. 14:00 - 14:30
  10. 14:30 - 15:00
  11. 15:00 - 15:30
  12. 15:30 - 16:00
  13. 16:00 - 16:30
  14. 16:30 - 17:00
```

**Tip:** You can then go back to menu option 2 to book one of these slots!

---

### Flow 5: Profile Management

**Scenario**: View and update your profile information.

#### Step 1: View Profile

**From main menu, select:** `7` (View my profile)

**What you'll see:**
```
👤 My Profile

┌─────────────────────┬──────────────────────────┐
│ Name                │ Sarah Johnson            │
│ Email               │ sarah@email.com          │
│ Phone               │ 555-1234                 │
│ Member Since        │ 2025-10-27 14:30:00      │
│ Total Conversations │ 12                       │
└─────────────────────┴──────────────────────────┘

Preferences:
  Preferred Doctor: ID 1
  Preferred Time: Morning
  Health Interests: stroke, prevention, neurology
```

**What this shows:**
- Your contact information
- How long you've been using the system
- Your conversation activity
- Learned preferences

---

## 🎯 Feature Guides

### Medical Q&A Best Practices

**✅ DO:**
- Ask specific questions: "What are stroke symptoms?"
- Use medical terms when known: "What is ischemic stroke?"
- Ask follow-up questions for clarity
- Request sources: "Where did this information come from?"

**❌ DON'T:**
- Ask for diagnosis (this is educational only)
- Replace emergency services (call 911 for emergencies)
- Use for prescription advice
- Share sensitive medical records

**Example Good Questions:**
```
✓ "What are the warning signs of a stroke?"
✓ "How can I reduce my stroke risk?"
✓ "What is the difference between ischemic and hemorrhagic stroke?"
✓ "What should I do during a stroke emergency?"
✓ "What is stroke rehabilitation like?"
```

---

### Appointment Booking Tips

**🕐 Choosing the Best Time:**
- Morning slots: 9:00 AM - 12:00 PM
- Afternoon slots: 1:00 PM - 5:00 PM
- Consider your preference (system learns this!)

**👨‍⚕️ Selecting the Right Doctor:**
- **Dr. Sarah Johnson** (Neurology) - Stroke specialists, prevention
- **Dr. Michael Chen** (Emergency) - Urgent concerns, acute care
- **Dr. Aisha Khan** (Rehabilitation) - Recovery, therapy, follow-ups

**📅 Calendar Integration:**
- Always sync to Google Calendar for reminders
- You'll receive email notification
- 30-minute reminder before appointment
- Easy to reschedule from calendar

**📝 Reason for Visit:**
Be specific to help doctor prepare:
- ✅ "Stroke prevention consultation"
- ✅ "Follow-up after TIA"
- ✅ "Rehabilitation progress check"
- ❌ "Checkup" (too vague)

---

### Understanding Personalization

**The system learns:**

**After 1 visit:**
- Your preferred doctor
- Your chosen time slot
- Topics you asked about

**After 3 visits:**
- Time-of-day pattern (morning/afternoon/evening)
- Preferred days of week
- Appointment frequency

**After 5 visits:**
- Follow-up patterns (e.g., monthly check-ins)
- Health topics of interest
- Booking behavior

**You'll see personalization in:**
- 👋 Personalized greetings
- 💡 Smart suggestions
- ⏰ Pre-filled time preferences
- 👨‍⚕️ Doctor recommendations
- 📅 Follow-up reminders

---

### Conversation History

**What's tracked:**
- ✅ Every question you ask
- ✅ Every answer provided
- ✅ Appointment bookings
- ✅ Context and topics
- ✅ Timestamps

**How it helps:**
- Resume previous conversations
- Track your learning journey
- Build personalized responses
- Suggest related topics

**Example:**
```
If you asked about "stroke symptoms" last week,
and today ask "prevention tips",
the system remembers your interest in strokes
and tailors answers accordingly.
```

---

## ❓ FAQ

### General Questions

**Q: Is my data secure?**
A: Yes! All data is stored locally in SQLite database on your machine. Nothing is sent to external servers except Google Calendar sync (if you choose).

**Q: Can I use this on mobile?**
A: Currently CLI-only. Web interface is planned for future.

**Q: How accurate is the medical information?**
A: Information comes from WHO, Mayo Clinic, CDC sources. Always consult healthcare professionals for medical advice.

**Q: Can I share my account?**
A: Each user should have their own account for personalized experience and privacy.

---

### Appointment Questions

**Q: How do I cancel an appointment?**
A: Currently, cancel through your Google Calendar. Database cancellation feature coming soon.

**Q: Can I book multiple appointments at once?**
A: One at a time currently. Future updates will support batch booking.

**Q: What if my preferred time isn't available?**
A: System shows all available slots. Choose the next best option, or check a different date.

**Q: Do I get reminders?**
A: Yes! Email reminder and Google Calendar notification 30 minutes before.

---

### Technical Questions

**Q: What if I get an error?**
A: Check the [Troubleshooting](#troubleshooting) section. Most errors are related to environment configuration.

**Q: Can I export my data?**
A: Yes! Database is SQLite. You can export using:
```bash
sqlite3 data/healthcare.db .dump > backup.sql
```

**Q: How do I update to a new version?**
A: Pull latest code and run:
```bash
git pull
pip install -r requirements.txt --upgrade
```

---

## 🔧 Troubleshooting

### Common Issues

#### Issue 1: "RAG Engine Not Found"

**Symptoms:**
```
Error: Cannot load RAG engine
No module named 'chromadb'
```

**Solution:**
```bash
pip install chromadb
```

---

#### Issue 2: "Calendar Sync Failed"

**Symptoms:**
```
Calendar sync: Authentication failed
```

**Solution:**
1. Check `.env` file has correct credentials
2. Verify Pipedream project ID
3. Confirm Google Calendar is connected in Pipedream
4. Check EXTERNAL_USER_ID matches

---

#### Issue 3: "No Available Slots"

**Symptoms:**
```
No available slots for this date
```

**Solution:**
- Try a different date
- Check doctor's schedule (may be fully booked)
- Contact admin to add more availability

---

#### Issue 4: "Database Locked"

**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
```bash
# Close all instances of the application
# Then restart
python3 healthcare_assistant.py
```

---

### Getting Help

**For bugs or feature requests:**
1. Check existing documentation
2. Review error logs
3. Contact system administrator
4. Report issue with error details

**For medical questions:**
- Use the Q&A feature
- Contact healthcare provider
- Call emergency services if urgent

---

## 📞 Quick Reference

### Keyboard Shortcuts

- `Ctrl+C` - Exit application
- `Enter` - Accept default option
- `↑/↓` - Navigate history (in some terminals)

### Menu Options

```
1 - Ask medical question
2 - Book appointment
3 - View appointments
4 - Check availability
5 - Conversation history
6 - Get suggestions
7 - View profile
8 - Exit
```

### Important Files

```
healthcare_assistant.py    - Main application
start.py                   - Quick start menu
data/healthcare.db         - Your data
.env                       - Configuration
```

---

## 🎓 Tips & Best Practices

### For Best Experience:

1. **Use regularly** - System learns from your patterns
2. **Be specific** - Better questions = better answers
3. **Sync calendar** - Never miss appointments
4. **Review history** - Track your learning
5. **Check suggestions** - Smart recommendations
6. **Update preferences** - System adapts to you

### Medical Research Workflow:

```
1. Start with broad question: "What is a stroke?"
2. Dive deeper: "What are the types of strokes?"
3. Get specific: "What is ischemic stroke treatment?"
4. Learn prevention: "How can I prevent strokes?"
5. Take action: Book appointment with neurologist
```

---

## 🎯 Next Steps

**Now that you know how to use the system:**

1. ✅ Launch the application: `python3 healthcare_assistant.py`
2. ✅ Create your account
3. ✅ Ask a medical question
4. ✅ Book your first appointment
5. ✅ Explore personalization features

**Need more help?**
- Read: `HEALTHCARE_README.md` - Technical documentation
- Check: `COMPLETE.md` - Full project overview
- Run: `python3 start.py` - See all options

---

**🏥 Healthcare Assistant - Making healthcare accessible and intelligent! 🏥**

*User Guide v1.0.0 - October 28, 2025*
