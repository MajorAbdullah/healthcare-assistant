# 🎨 Frontend Development Prompts - Healthcare Assistant

## Project Overview
Build a modern, responsive web interface for a Healthcare Assistant system with two separate portals:
1. **Patient Portal** - For patients to book appointments, chat with AI, view history
2. **Doctor Portal** - For doctors to manage schedules, view patients, add notes

**Technology Stack:**
- **Framework**: Next.js 14 (App Router) + React 18 + TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components
- **Icons**: Lucide React
- **API Communication**: Fetch API / Axios (REST) + WebSocket (for chat)
- **State Management**: React Context / Zustand (lightweight)
- **Forms**: React Hook Form + Zod validation
- **Date/Time**: date-fns or Day.js
- **Charts**: Recharts (for doctor analytics)

**Design Requirements:**
- Mobile-first responsive design
- Clean, medical/healthcare aesthetic (blues, whites, greens)
- Accessibility compliant (WCAG AA)
- Loading states and error handling
- Toast notifications for actions
- No external dependencies (runs locally)

**API Base URL**: `http://localhost:8000/api/v1`

---

## 🏥 PATIENT PORTAL - 6 Screens

### SCREEN 1: Patient Login/Register Page
**Route**: `/patient/auth`

**Purpose**: Allow patients to login or create new account

**UI Components:**
- Logo and app name at top
- Tabbed interface (Login | Register)
- **Login Tab:**
  - Email input field
  - Phone number input field
  - "Login" button
  - Simple validation (email format, phone 10 digits)
- **Register Tab:**
  - Full Name input
  - Email input
  - Phone number input
  - Date of Birth (date picker)
  - Gender (dropdown: Male/Female/Other)
  - "Register" button
  - Form validation

**API Endpoints:**
- `POST /api/v1/patients/login` - Body: `{email, phone}` - Returns: `{user_id, name, token}`
- `POST /api/v1/patients/register` - Body: `{name, email, phone, dob, gender}` - Returns: `{user_id, message}`

**Design Notes:**
- Centered card layout
- Soft blue gradient background
- Clean form fields with floating labels
- Success message redirects to dashboard

---

### SCREEN 2: Patient Dashboard
**Route**: `/patient/dashboard`

**Purpose**: Home screen showing overview and quick actions

**UI Sections:**

1. **Header**:
   - Personalized greeting (e.g., "Good morning, John!")
   - User avatar/initials in top right
   - Logout button

2. **Upcoming Appointment Alert** (if exists):
   - Highlighted card with clock icon
   - "Your next appointment: Tomorrow at 11:30 AM with Dr. Aisha Khan"
   - "View Details" button

3. **Quick Action Cards** (3 columns on desktop, stack on mobile):
   - **Book Appointment** 📅
     - Icon: Calendar
     - Button: "Book Now" → `/patient/book`
   - **Ask Medical Questions** 💬
     - Icon: MessageCircle
     - Button: "Start Chat" → `/patient/chat`
   - **View Appointments** 📋
     - Icon: ClipboardList
     - Button: "See All" → `/patient/appointments`

4. **Recent Activity** (optional):
   - Last 2 appointments shown as small cards
   - Doctor name, date, status badge

**API Endpoints:**
- `GET /api/v1/patients/{user_id}/greeting` - Returns: `{greeting, upcoming_appointment}`
- `GET /api/v1/appointments/{user_id}?limit=2` - Returns: `[{id, doctor_name, date, time, status}]`

**Design Notes:**
- Spacious layout with cards
- Use blue accent color for primary actions
- Icons from Lucide React
- Smooth hover effects on cards

---

### SCREEN 3: Book Appointment (Multi-Step Flow)
**Route**: `/patient/book`

**Purpose**: Guide patient through booking process

**Step 1: Select Doctor**
- Grid/list of doctor cards (3 columns on desktop)
- Each card shows:
  - Doctor photo placeholder (initials in circle)
  - Name (e.g., "Dr. Aisha Khan")
  - Specialty (e.g., "Cardiologist")
  - Rating stars (can be static 4.5/5)
  - "Select Doctor" button
- Search/filter bar at top (by specialty)

**Step 2: Select Date**
- Calendar component (current month)
- Disable past dates
- Highlight available dates (dates with open slots)
- Show selected date clearly
- "Next" button to proceed

**Step 3: Select Time**
- Display available time slots as chips/buttons
- Group by time of day (Morning, Afternoon, Evening)
- Example: `09:00 AM`, `09:30 AM`, `10:00 AM`, etc.
- Show "No slots available" if date fully booked
- "Next" button after selecting time

**Step 4: Confirmation**
- Summary card:
  - Doctor name and specialty
  - Date and time
  - Patient name
  - Option to add reason for visit (textarea)
  - Checkbox: "Sync to Google Calendar?"
- "Confirm Booking" button (primary)
- "Go Back" button (secondary)

**Step 5: Success**
- Success checkmark animation
- "Appointment booked successfully!"
- Appointment details displayed
- "Back to Dashboard" button
- "Add to Calendar" button (if not synced)

**API Endpoints:**
- `GET /api/v1/doctors` - Returns: `[{doctor_id, name, specialty, available_dates_count}]`
- `GET /api/v1/doctors/{doctor_id}/availability?date=YYYY-MM-DD` - Returns: `{available_slots: ['09:00', '09:30', ...]}`
- `POST /api/v1/appointments` - Body: `{user_id, doctor_id, date, time, reason, sync_calendar}` - Returns: `{appointment_id, message}`

**Design Notes:**
- Progress indicator at top (Step 1 of 4)
- Back/Next navigation buttons
- Smooth transitions between steps
- Mobile-responsive (stack on small screens)

---

### SCREEN 4: Medical Q&A Chat
**Route**: `/patient/chat`

**Purpose**: Real-time chat interface with AI medical assistant

**UI Layout:**

1. **Chat Header**:
   - "Medical Assistant" title
   - Status indicator (green dot = connected)
   - Close/minimize button

2. **Message Area** (scrollable):
   - Chat bubbles (WhatsApp-style)
   - User messages: Right-aligned, blue background
   - AI messages: Left-aligned, gray background
   - Timestamp below each message
   - Loading indicator (3 bouncing dots) while AI responds
   - Auto-scroll to bottom on new message

3. **Input Area** (bottom):
   - Text input field (grows with content, max 4 lines)
   - Send button (paper plane icon)
   - Placeholder: "Ask a medical question..."
   - Disable input while waiting for response

4. **Suggested Questions** (when chat is empty):
   - 3-4 quick question chips:
     - "What causes high blood pressure?"
     - "How to manage diabetes?"
     - "Symptoms of stroke?"
     - "Healthy diet tips?"

**API Endpoints:**
- **WebSocket**: `ws://localhost:8000/ws/chat/{user_id}` 
  - Send: `{message: "user question"}`
  - Receive: `{content: "AI response", timestamp: "..."}`
- **REST Alternative**: `POST /api/v1/chat` - Body: `{user_id, message}` - Returns: `{response, conversation_id}`

**Design Notes:**
- Full-height layout (minus header)
- Smooth message animations (slide in from bottom)
- Different colors for user vs AI messages
- Markdown support in AI responses (bold, lists, etc.)
- Copy button on AI messages

---

### SCREEN 5: Appointments List
**Route**: `/patient/appointments`

**Purpose**: View all appointments (past, upcoming, cancelled)

**UI Components:**

1. **Header**:
   - "My Appointments" title
   - Tab navigation: `All | Upcoming | Past | Cancelled`

2. **Appointment Cards** (list view):
   - Each card displays:
     - Doctor name and specialty
     - Date and time
     - Status badge (Scheduled/Completed/Cancelled)
     - Reason for visit (if provided)
     - Action buttons:
       - **Upcoming**: "Cancel" button, "View Details"
       - **Past**: "Book Again" button
       - **Cancelled**: "Book Again" button
   - Empty state: "No appointments found" with illustration

3. **Filters** (top right):
   - Sort by: Date (newest/oldest)
   - Filter by doctor (dropdown)

**API Endpoints:**
- `GET /api/v1/appointments/{user_id}` - Returns: `[{id, doctor_id, doctor_name, specialty, date, time, status, reason, notes}]`
- `PUT /api/v1/appointments/{appointment_id}/cancel` - Returns: `{message}`

**Design Notes:**
- Card-based layout with shadows
- Color-coded status badges (green=scheduled, gray=completed, red=cancelled)
- Responsive grid (1 column mobile, 2 desktop)
- Confirmation modal before cancelling

---

### SCREEN 6: Patient Profile
**Route**: `/patient/profile`

**Purpose**: View and edit personal information

**UI Sections:**

1. **Profile Header**:
   - Large avatar (initials or photo)
   - Patient name
   - "Edit Profile" button

2. **Personal Information** (read-only with edit mode):
   - Full Name
   - Email
   - Phone Number
   - Date of Birth
   - Gender
   - "Edit" button toggles to form inputs
   - "Save Changes" and "Cancel" buttons in edit mode

3. **Account Statistics** (cards):
   - Total Appointments: 12
   - Upcoming Appointments: 2
   - Completed Appointments: 10
   - Member Since: Jan 2024

4. **Preferences** (toggles):
   - Email notifications
   - SMS reminders
   - Calendar sync by default

5. **Danger Zone**:
   - "Delete Account" button (red, with confirmation)

**API Endpoints:**
- `GET /api/v1/patients/{user_id}` - Returns: `{name, email, phone, dob, gender, created_at, stats}`
- `PUT /api/v1/patients/{user_id}` - Body: `{name, email, phone, dob, gender}` - Returns: `{message}`
- `GET /api/v1/patients/{user_id}/preferences` - Returns: `{email_notifications, sms_reminders, auto_sync_calendar}`
- `PUT /api/v1/patients/{user_id}/preferences` - Body: `{...preferences}` - Returns: `{message}`

**Design Notes:**
- Clean card-based layout
- Form validation on edit
- Success toast on save
- Confirmation modal for dangerous actions

---

---

## 👨‍⚕️ DOCTOR PORTAL - 6 Screens

### SCREEN 7: Doctor Login
**Route**: `/doctor/auth`

**Purpose**: Simple doctor authentication

**UI Components:**
- Logo and "Doctor Portal" title
- **Doctor Selection**:
  - Dropdown or card selection showing all doctors
  - Each option shows: Name, Specialty, ID
  - Example: "Dr. Aisha Khan - Cardiologist (ID: 1)"
- "Login" button
- (Future: Add password/PIN field)

**API Endpoints:**
- `GET /api/v1/doctors` - Returns: `[{doctor_id, name, specialty}]`
- `POST /api/v1/doctors/login` - Body: `{doctor_id}` - Returns: `{doctor_id, name, specialty, token}`

**Design Notes:**
- Professional blue/teal color scheme
- Large, clear doctor cards
- Simple one-click login for prototype

---

### SCREEN 8: Doctor Dashboard
**Route**: `/doctor/dashboard`

**Purpose**: Overview of today's schedule and quick stats

**UI Sections:**

1. **Header**:
   - "Welcome back, Dr. Khan"
   - Current date and time
   - Logout button

2. **Statistics Cards** (4 cards in row):
   - **Today's Appointments**: 8
   - **Total Patients**: 127
   - **This Week**: 32 appointments
   - **Completion Rate**: 95%

3. **Today's Schedule** (timeline view):
   - List of today's appointments:
     - Time (e.g., "09:00 AM")
     - Patient name
     - Reason for visit
     - Status (Scheduled/Completed)
     - "View Details" button
     - "Add Notes" button
   - Empty state: "No appointments today"

4. **Quick Actions** (floating buttons or sidebar):
   - View Full Calendar
   - Patient Directory
   - Analytics

**API Endpoints:**
- `GET /api/v1/doctors/{doctor_id}/stats` - Returns: `{today_count, total_patients, week_count, completion_rate}`
- `GET /api/v1/doctors/{doctor_id}/appointments?date=today` - Returns: `[{appointment_id, time, patient_name, patient_id, reason, status}]`

**Design Notes:**
- Clean, professional layout
- Timeline component for schedule
- Color-coded status indicators
- Quick access to common actions

---

### SCREEN 9: Full Calendar View
**Route**: `/doctor/calendar`

**Purpose**: Visual calendar showing all appointments

**UI Components:**

1. **Calendar Controls**:
   - Month/Week/Day view toggle
   - Previous/Next navigation arrows
   - "Today" button to jump to current date
   - Date range display (e.g., "October 2025")

2. **Calendar Grid**:
   - Month view: Small cells with appointment counts
   - Week view: Columns for each day, rows for time slots
   - Day view: Detailed hourly timeline
   - Appointments shown as colored blocks
   - Click appointment to see details modal

3. **Legend**:
   - Color coding: Scheduled (blue), Completed (green), Cancelled (red)

4. **Appointment Detail Modal** (on click):
   - Patient name and photo
   - Date and time
   - Reason for visit
   - Status
   - "Add Notes" button
   - "Mark Complete" / "Cancel" buttons

**API Endpoints:**
- `GET /api/v1/doctors/{doctor_id}/appointments?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` - Returns: `[{appointment_id, patient_name, date, time, status, reason}]`
- `PUT /api/v1/appointments/{appointment_id}/status` - Body: `{status: 'completed'}` - Returns: `{message}`

**Design Notes:**
- Use a calendar library (react-big-calendar or fullcalendar)
- Responsive (stack on mobile)
- Interactive hover states
- Smooth modal animations

---

### SCREEN 10: Patient Directory
**Route**: `/doctor/patients`

**Purpose**: View all patients with search and filtering

**UI Components:**

1. **Search Bar**:
   - Search by name, email, or phone
   - Real-time search (debounced)

2. **Filters** (top bar):
   - Sort by: Name, Last Visit, Total Visits
   - Filter by: All / Active / Inactive

3. **Patient Table/Cards**:
   - **Table Columns** (desktop):
     - Patient Name
     - Email
     - Phone
     - Total Visits
     - Last Visit Date
     - Actions (View Details button)
   - **Cards** (mobile):
     - Stacked cards with same info

4. **Pagination**:
   - Show 20 patients per page
   - Page numbers and Next/Previous

**API Endpoints:**
- `GET /api/v1/doctors/{doctor_id}/patients?search=...&sort=...&page=1` - Returns: `{patients: [{patient_id, name, email, phone, total_visits, last_visit}], total_count, pages}`

**Design Notes:**
- Clean table design
- Alternating row colors
- Sticky header on scroll
- Responsive to mobile

---

### SCREEN 11: Patient Detail / History
**Route**: `/doctor/patients/{patient_id}`

**Purpose**: View complete patient history and add notes

**UI Sections:**

1. **Patient Profile Card** (top):
   - Photo/avatar
   - Name, Age, Gender
   - Contact: Email, Phone
   - Total Visits: 5

2. **Appointment History** (timeline):
   - Chronological list of all appointments
   - Each entry shows:
     - Date and time
     - Status
     - Reason for visit
     - Medical notes (if added)
     - "Add/Edit Notes" button
   - Empty state: "No previous appointments"

3. **Add Notes Modal/Form**:
   - Select appointment (dropdown if multiple)
   - Textarea for notes
   - "Save Notes" button
   - Auto-save indicator

4. **Statistics** (sidebar):
   - Missed appointments: 0
   - Completed: 5
   - Cancelled: 0

**API Endpoints:**
- `GET /api/v1/patients/{patient_id}` - Returns: `{name, email, phone, dob, gender, total_visits}`
- `GET /api/v1/patients/{patient_id}/appointments` - Returns: `[{appointment_id, date, time, status, reason, notes}]`
- `POST /api/v1/appointments/{appointment_id}/notes` - Body: `{notes: "..."}` - Returns: `{message}`
- `PUT /api/v1/appointments/{appointment_id}/notes` - Body: `{notes: "..."}` - Returns: `{message}`

**Design Notes:**
- Two-column layout (profile left, history right)
- Expandable note sections
- Print-friendly view option
- Smooth transitions

---

### SCREEN 12: Analytics Dashboard
**Route**: `/doctor/analytics`

**Purpose**: Visual statistics and insights

**UI Components:**

1. **Date Range Selector**:
   - Presets: Last 7 days, Last 30 days, Last 3 months, Custom
   - Date range picker

2. **Charts** (grid layout):

   **Chart 1: Appointment Trends** (Line chart)
   - X-axis: Dates
   - Y-axis: Number of appointments
   - Show scheduled vs completed

   **Chart 2: Completion Rate** (Donut/Pie chart)
   - Completed: 95%
   - Cancelled: 3%
   - No-shows: 2%

   **Chart 3: Busiest Days** (Bar chart)
   - X-axis: Days of week
   - Y-axis: Appointment count
   - Highlight busiest day

   **Chart 4: Patient Growth** (Area chart)
   - New patients over time
   - Total patients trend

3. **Summary Cards** (top row):
   - Total Appointments (selected period)
   - Total Patients
   - Average Daily Appointments
   - Cancellation Rate

**API Endpoints:**
- `GET /api/v1/doctors/{doctor_id}/analytics?start_date=...&end_date=...` - Returns: `{total_appointments, total_patients, completion_rate, daily_breakdown: [{date, count}], weekly_breakdown: {...}, patient_growth: [...]}`

**Design Notes:**
- Use Recharts library
- Responsive charts (stack on mobile)
- Interactive tooltips
- Export data button (CSV)
- Professional color scheme

---

---

## 🎨 Design System Guidelines

### Colors:
```css
Primary: #3B82F6 (Blue)
Secondary: #10B981 (Green)
Accent: #8B5CF6 (Purple)
Danger: #EF4444 (Red)
Warning: #F59E0B (Amber)
Gray Scale: Tailwind default
Background: #F9FAFB
Text: #111827
```

### Typography:
- Headings: Inter or Poppins (Bold)
- Body: Inter or Open Sans (Regular)
- Font sizes: Tailwind defaults (text-sm, text-base, text-lg, etc.)

### Spacing:
- Container: `max-w-7xl mx-auto px-4`
- Card padding: `p-6`
- Section spacing: `mb-8`

### Components:
- Buttons: Rounded (`rounded-lg`), shadow on hover
- Cards: White background, subtle shadow (`shadow-md`)
- Inputs: Border, focus ring, rounded corners
- Status badges: Small, rounded-full, colored background

### Responsive Breakpoints:
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

---

## 📡 API Response Formats

### Success Response:
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response:
```json
{
  "success": false,
  "error": "Error message here",
  "code": "ERROR_CODE"
}
```

### Authentication:
- For now: Store `user_id` or `doctor_id` in localStorage
- Future: JWT token in Authorization header

---

## 🚀 Getting Started Instructions

1. **Create Next.js Project**:
```bash
npx create-next-app@latest healthcare-frontend --typescript --tailwind --app
cd healthcare-frontend
```

2. **Install Dependencies**:
```bash
npm install lucide-react axios date-fns recharts
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input label select textarea tabs badge avatar calendar
```

3. **Project Structure**:
```
app/
  patient/
    auth/page.tsx
    dashboard/page.tsx
    book/page.tsx
    chat/page.tsx
    appointments/page.tsx
    profile/page.tsx
  doctor/
    auth/page.tsx
    dashboard/page.tsx
    calendar/page.tsx
    patients/
      page.tsx
      [id]/page.tsx
    analytics/page.tsx
  layout.tsx
  page.tsx

components/
  patient/
    AppointmentCard.tsx
    DoctorCard.tsx
    ChatBubble.tsx
  doctor/
    ScheduleTimeline.tsx
    PatientTable.tsx
    StatsCard.tsx
  ui/ (shadcn components)

lib/
  api.ts (API client functions)
  utils.ts (helper functions)
```

4. **API Client Setup** (`lib/api.ts`):
```typescript
const API_BASE = 'http://localhost:8000/api/v1';

export const api = {
  // Patient endpoints
  patient: {
    login: (email: string, phone: string) => 
      fetch(`${API_BASE}/patients/login`, {...}),
    register: (data: RegisterData) => 
      fetch(`${API_BASE}/patients/register`, {...}),
    // ... more endpoints
  },
  // Doctor endpoints
  doctor: {
    login: (doctorId: number) => 
      fetch(`${API_BASE}/doctors/login`, {...}),
    // ... more endpoints
  },
};
```

---

## ✅ Development Checklist

### Patient Portal:
- [ ] Auth page (login/register tabs)
- [ ] Dashboard with greeting and quick actions
- [ ] Book appointment (4-step flow)
- [ ] Chat interface (WebSocket or polling)
- [ ] Appointments list with filters
- [ ] Profile page with edit mode

### Doctor Portal:
- [ ] Login page (doctor selection)
- [ ] Dashboard with stats and today's schedule
- [ ] Full calendar view (month/week/day)
- [ ] Patient directory with search
- [ ] Patient detail with history
- [ ] Analytics with charts

### Common:
- [ ] Responsive design (mobile-first)
- [ ] Loading states (spinners/skeletons)
- [ ] Error handling (toast notifications)
- [ ] Form validation
- [ ] Navigation (sidebar/header)
- [ ] Logout functionality

---

## 🎯 Priority Order

**Phase 1** (MVP - Week 1):
1. Patient auth page
2. Patient dashboard
3. Book appointment flow
4. Doctor login
5. Doctor dashboard

**Phase 2** (Week 2):
6. Patient appointments list
7. Doctor calendar view
8. Patient directory
9. Patient detail/history

**Phase 3** (Week 3):
10. Chat interface
11. Analytics dashboard
12. Profile pages
13. Polish and responsive fixes

---

## 📝 Notes

- All pages should have loading skeletons while fetching data
- Use optimistic UI updates where possible
- Add confirmation dialogs for destructive actions (cancel appointment, delete account)
- Include empty states with illustrations
- Make sure all forms have proper validation
- Add success/error toast notifications using shadcn Toast
- Keep the UI clean and medical-professional looking
- Ensure accessibility (keyboard navigation, screen readers, ARIA labels)

---

**Backend will be ready at**: `http://localhost:8000`
**API Documentation (Swagger)**: `http://localhost:8000/docs`

This file provides everything needed to build the complete frontend! 🚀
