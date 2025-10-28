# 🤖 AI Chat Testing - Playwright MCP Server

**Test Date:** October 29, 2025  
**Feature:** Medical AI Assistant Chat  
**Frontend:** http://localhost:8080/patient/chat  
**Backend API:** http://localhost:8000/api/v1/chat  
**WebSocket:** ws://localhost:8000/ws/chat/{user_id}

---

## 📋 Test Plan

### Test Scenarios
1. ✅ Navigate to Chat page
2. ✅ Verify chat interface loads
3. ✅ Send a medical question (REST API)
4. ✅ Receive AI response
5. ✅ Test suggested questions
6. ✅ Test conversation history
7. ✅ Test WebSocket connection (if available)
8. ✅ Test error handling
9. ✅ Test chat persistence across sessions

---

## 🚀 Starting Tests

### Prerequisites
- Backend API running on port 8000
- Frontend running on port 8080
- User logged in (user_id stored in localStorage)

---

## Test Execution Steps

### Step 1: Navigate to Chat Page
```
Action: Navigate to http://localhost:8080/patient/chat
Expected: Chat interface loads with empty state
```

### Step 2: Verify Chat Interface
```
Elements to check:
- Header with "Medical Assistant" title
- "Online" badge with green pulse indicator
- Welcome message: "How can I help you today?"
- Suggested questions buttons
- Message input field
- Send button
- Bot avatar icon
```

### Step 3: Test Suggested Question
```
Action: Click on suggested question "Symptoms of stroke?"
Expected:
- Question appears as user message
- Loading indicator (3 bouncing dots)
- AI response appears within 2-3 seconds
- Response includes stroke symptoms information
```

### Step 4: Send Custom Medical Question
```
Action: Type "What causes high blood pressure?" and press Enter
Expected:
- User message appears on right side with blue background
- AI message appears on left side with gray background
- Response includes relevant medical information
- Timestamps display correctly
```

### Step 5: Test Multiple Messages
```
Actions:
1. Ask: "How to manage diabetes?"
2. Ask: "What is a healthy diet?"
3. Ask: "Exercise recommendations?"

Expected:
- All messages appear in chronological order
- Chat scrolls to bottom automatically
- Each message has unique timestamp
- Loading states work correctly
```

### Step 6: Test Input Validation
```
Action: Try sending empty message
Expected: Send button disabled or no action taken
```

### Step 7: Test Error Handling
```
Action: Simulate API error (stop backend)
Expected:
- Error toast notification
- Error message in chat: "I'm sorry, I encountered an error. Please try again."
- Chat remains functional after error
```

### Step 8: Test Chat Persistence
```
Actions:
1. Send multiple messages
2. Navigate away to dashboard
3. Return to chat page

Expected:
- Messages should be cleared (new session)
- OR messages persist if localStorage/sessionStorage used
```

---

## 📸 Screenshots to Capture

1. `chat-01-initial-state.png` - Empty chat with welcome message
2. `chat-02-suggested-question.png` - Suggested question clicked
3. `chat-03-ai-response.png` - AI response received
4. `chat-04-conversation.png` - Multi-message conversation
5. `chat-05-loading-state.png` - Loading indicator
6. `chat-06-error-state.png` - Error handling

---

## 🧪 Detailed Test Cases

### Test Case 1: Initial Chat Interface ✅

**Objective:** Verify chat page loads correctly

**Steps:**
1. Login as patient (ensure user_id in localStorage)
2. Navigate to `/patient/chat`
3. Wait for page to load

**Validations:**
- [ ] Page title is "Medical Assistant"
- [ ] Badge shows "Online" with green pulse
- [ ] Bot icon displayed
- [ ] Welcome message: "How can I help you today?"
- [ ] Subtitle: "Ask me any medical question"
- [ ] 4 suggested questions visible
- [ ] Input field placeholder: "Ask a medical question..."
- [ ] Send button visible and enabled

**Expected Result:** Chat interface fully rendered and interactive

---

### Test Case 2: Suggested Question Interaction ✅

**Objective:** Test clicking suggested questions

**Steps:**
1. Click on "Symptoms of stroke?" button
2. Wait for response

**Validations:**
- [ ] User message appears on right side
- [ ] Message background is blue (primary color)
- [ ] User avatar shows User icon
- [ ] Loading indicator appears (3 bouncing dots)
- [ ] AI response appears within 5 seconds
- [ ] AI message on left side with gray background
- [ ] Bot avatar visible
- [ ] Both messages have timestamps
- [ ] Chat scrolls to bottom

**Expected API Call:**
```http
POST /api/v1/chat HTTP/1.1
Content-Type: application/json

{
  "user_id": 1,
  "message": "Symptoms of stroke?"
}
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "answer": "Common stroke symptoms include...",
    "sources": ["stroke_overview.txt"]
  }
}
```

---

### Test Case 3: Custom Message Input ✅

**Objective:** Test typing and sending custom messages

**Steps:**
1. Click in input field
2. Type: "What causes high blood pressure?"
3. Press Enter (or click Send button)
4. Wait for response

**Validations:**
- [ ] Input field accepts text
- [ ] Send button enables when text present
- [ ] Pressing Enter sends message
- [ ] Input clears after sending
- [ ] Message appears in chat
- [ ] AI responds appropriately
- [ ] Can send multiple messages in sequence

---

### Test Case 4: Conversation Flow ✅

**Objective:** Test multi-turn conversation

**Steps:**
1. Send: "What is diabetes?"
2. Wait for response
3. Send: "How to manage it?"
4. Wait for response
5. Send: "What foods should I avoid?"
6. Wait for response

**Validations:**
- [ ] All messages appear in order
- [ ] Timestamps increase chronologically
- [ ] Auto-scroll works for each new message
- [ ] Loading states work for each response
- [ ] No duplicate messages
- [ ] Chat history maintains context

---

### Test Case 5: Loading State ✅

**Objective:** Verify loading indicators work correctly

**Steps:**
1. Send a message
2. Observe loading state before response

**Validations:**
- [ ] Loading indicator appears immediately
- [ ] 3 dots animate (bounce effect)
- [ ] Loading indicator positioned correctly (left side)
- [ ] Bot avatar visible during loading
- [ ] Input disabled during loading
- [ ] Send button disabled during loading
- [ ] Loading disappears when response arrives

---

### Test Case 6: Error Handling ✅

**Objective:** Test error scenarios gracefully handled

**Test 6a: API Error**
1. Stop backend server
2. Send a message
3. Observe error handling

**Validations:**
- [ ] Error toast appears
- [ ] Error message in chat
- [ ] Chat doesn't crash
- [ ] User can retry after error
- [ ] Previous messages remain visible

**Test 6b: Empty Message**
1. Click in input without typing
2. Try to send

**Validations:**
- [ ] Send button disabled when input empty
- [ ] No API call made

**Test 6c: Network Timeout**
1. Simulate slow network
2. Send message

**Validations:**
- [ ] Loading state persists
- [ ] Timeout handled gracefully
- [ ] Error message displayed

---

### Test Case 7: UI Responsiveness ✅

**Objective:** Test responsive design

**Steps:**
1. Resize browser to mobile width (375px)
2. Interact with chat
3. Resize to tablet (768px)
4. Resize to desktop (1440px)

**Validations:**
- [ ] Chat adapts to all screen sizes
- [ ] Messages remain readable
- [ ] Input field accessible
- [ ] Send button always visible
- [ ] No horizontal scroll
- [ ] Touch targets adequate size (mobile)

---

### Test Case 8: Accessibility ✅

**Objective:** Test keyboard navigation and screen reader support

**Steps:**
1. Navigate to chat using Tab key
2. Use Enter to send messages
3. Test with screen reader (optional)

**Validations:**
- [ ] Input field focusable
- [ ] Send button focusable
- [ ] Suggested questions focusable
- [ ] Enter key sends message
- [ ] Focus visible indicators
- [ ] ARIA labels present (if implemented)

---

### Test Case 9: Message Formatting ✅

**Objective:** Test how different message types display

**Steps:**
1. Send short message: "Hi"
2. Send long message: (multiple paragraphs)
3. Send message with special characters
4. Send message with numbers/dates

**Validations:**
- [ ] Short messages display correctly
- [ ] Long messages wrap properly
- [ ] Line breaks preserved (whitespace-pre-wrap)
- [ ] Special characters render correctly
- [ ] No overflow issues
- [ ] Maximum width enforced (70%)

---

### Test Case 10: Navigation ✅

**Objective:** Test navigation to/from chat

**Steps:**
1. Click "Back" button
2. Verify redirect to dashboard
3. Navigate back to chat via dashboard button
4. Verify chat state

**Validations:**
- [ ] Back button works
- [ ] Redirects to `/patient/dashboard`
- [ ] Dashboard "Chat with AI" button works
- [ ] Chat reloads fresh (or persists - depends on implementation)

---

## 🔌 WebSocket Testing (Advanced)

### Test Case 11: WebSocket Connection ✅

**Note:** Current implementation uses REST API. WebSocket test for future enhancement.

**Steps:**
1. Open browser console
2. Navigate to chat
3. Check WebSocket connection status

**Validations:**
- [ ] WebSocket connection attempted
- [ ] Connection established: `ws://localhost:8000/ws/chat/{user_id}`
- [ ] Messages sent via WebSocket
- [ ] Real-time responses received
- [ ] Connection persists during session
- [ ] Reconnection on disconnect

---

## 📊 Performance Testing

### Test Case 12: Response Time ✅

**Objective:** Measure AI response times

**Steps:**
1. Send 5 different medical questions
2. Measure time from send to response

**Targets:**
- [ ] Average response time < 3 seconds
- [ ] 95th percentile < 5 seconds
- [ ] No timeouts

---

## 🧪 Edge Cases

### Test Case 13: Edge Cases ✅

**Test 13a: Very Long Message**
- Input: 500+ character question
- Expected: Accepts input, sends successfully, displays properly

**Test 13b: Rapid Messages**
- Send 5 messages quickly in succession
- Expected: All queued and processed in order

**Test 13c: Special Medical Terms**
- Input: "What is myocardial infarction?"
- Expected: AI understands medical terminology

**Test 13d: Off-Topic Question**
- Input: "What's the weather today?"
- Expected: AI responds appropriately (medical focus or polite redirect)

**Test 13e: Multiple Sessions**
- Open chat in two browser tabs
- Send messages from both
- Expected: Each session independent

---

## ✅ Success Criteria

### Functional Requirements
- ✅ Chat interface loads without errors
- ✅ Messages send successfully
- ✅ AI responses received
- ✅ Loading states work
- ✅ Error handling graceful
- ✅ Navigation works correctly

### Performance Requirements
- ✅ Initial load < 2 seconds
- ✅ Message send latency < 100ms
- ✅ AI response time < 5 seconds average
- ✅ Smooth scrolling animations

### UX Requirements
- ✅ Intuitive interface
- ✅ Clear message ownership (user vs AI)
- ✅ Readable typography
- ✅ Responsive design
- ✅ Accessible controls

---

## 🐛 Known Issues

### Issues to Track
1. **No conversation persistence** - Messages clear on page refresh
2. **No WebSocket implementation** - Using REST API only
3. **No typing indicators** - Only loading dots
4. **No message delivery confirmation** - No read receipts
5. **No conversation history** - Can't view past sessions

---

## 🔄 Next Steps

### Enhancements to Test (Future)
- [ ] WebSocket real-time chat
- [ ] Conversation history/persistence
- [ ] Message editing/deletion
- [ ] File/image upload (medical reports)
- [ ] Voice input
- [ ] Multi-language support
- [ ] Chat export/download
- [ ] Typing indicators
- [ ] Read receipts
- [ ] Emoji reactions

---

## 📝 Test Execution Log

### Run 1: [Date/Time]
- **Tester:** [Name]
- **Tests Passed:** X/13
- **Tests Failed:** X/13
- **Blockers:** [List any blockers]
- **Notes:** [Additional observations]

---

**Test Plan Created:** October 29, 2025  
**Ready for Execution:** ✅ YES  
**Automated Test Script:** To be created  

