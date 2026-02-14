/**
 * Healthcare Assistant API Client
 * Centralized API communication layer for Frontend
 */

// API Configuration
const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000/api/v1';
const WS_BASE_URL = (import.meta as any).env?.VITE_WS_URL || 'ws://localhost:8000';

// Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface Patient {
  user_id: number;
  name: string;
  email: string;
  phone: string;
  date_of_birth?: string;
  gender?: string;
}

export interface Doctor {
  doctor_id: number;
  name: string;
  specialty: string;
  email?: string;
  phone?: string;
  rating?: number;
  calendar_id?: string;
  consultation_duration?: number;
}

export interface Appointment {
  appointment_id: number;
  user_id: number;
  doctor_id: number;
  appointment_date: string;
  start_time: string;
  end_time: string;
  reason?: string;
  status: 'scheduled' | 'confirmed' | 'pending_approval' | 'completed' | 'cancelled' | 'no-show';
  notes?: string;
  created_at: string;
  // Joined fields
  doctor_name?: string;
  doctor_specialty?: string;
  patient_name?: string;
}

export interface TimeSlot {
  start_time: string;
  end_time: string;
  duration: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface DoctorStats {
  total_patients: number;
  total_appointments: number;
  upcoming_appointments: number;
  completed_today: number;
}

export interface Analytics {
  total_appointments: number;
  new_patients: number;
  average_rating?: number;
  monthly_data?: any[];
}

// API Error Handler
class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function handleResponse<T>(response: Response): Promise<ApiResponse<T>> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: response.statusText }));
    throw new ApiError(response.status, error.message || 'API request failed');
  }
  return response.json();
}

// ============================================
// PATIENT ENDPOINTS
// ============================================

export const patientApi = {
  /**
   * Register a new patient
   */
  register: async (data: {
    name: string;
    email: string;
    phone: string;
    dob?: string;
    gender?: string;
  }): Promise<ApiResponse<{ user_id: number; name: string }>> => {
    const response = await fetch(`${API_BASE_URL}/patients/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * Login existing patient
   */
  login: async (data: {
    email: string;
    phone: string;
  }): Promise<ApiResponse<{ user_id: number; name: string; email: string; phone: string; token: string }>> => {
    const response = await fetch(`${API_BASE_URL}/patients/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * Get patient profile
   */
  getProfile: async (userId: number): Promise<ApiResponse<Patient>> => {
    const response = await fetch(`${API_BASE_URL}/patients/${userId}`);
    return handleResponse(response);
  },

  /**
   * Update patient profile
   */
  updateProfile: async (
    userId: number,
    data: Partial<Patient>
  ): Promise<ApiResponse<Patient>> => {
    const response = await fetch(`${API_BASE_URL}/patients/${userId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * Get personalized greeting
   */
  getGreeting: async (userId: number): Promise<ApiResponse<{ greeting: string }>> => {
    const response = await fetch(`${API_BASE_URL}/patients/${userId}/greeting`);
    return handleResponse(response);
  },

  /**
   * Get patient preferences
   */
  getPreferences: async (userId: number): Promise<ApiResponse<any>> => {
    const response = await fetch(`${API_BASE_URL}/patients/${userId}/preferences`);
    return handleResponse(response);
  },

  /**
   * Update patient preferences
   */
  updatePreferences: async (
    userId: number,
    preferences: {
      email_notifications?: boolean;
      sms_reminders?: boolean;
      auto_sync_calendar?: boolean;
    }
  ): Promise<ApiResponse<any>> => {
    const response = await fetch(`${API_BASE_URL}/patients/${userId}/preferences`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(preferences),
    });
    return handleResponse(response);
  },
};

// ============================================
// DOCTOR ENDPOINTS
// ============================================

export const doctorApi = {
  /**
   * Get all doctors
   */
  getAll: async (): Promise<ApiResponse<{ doctors: Doctor[] }>> => {
    const response = await fetch(`${API_BASE_URL}/doctors`);
    return handleResponse(response);
  },

  /**
   * Get doctor availability for a specific date
   */
  getAvailability: async (
    doctorId: number,
    date: string
  ): Promise<ApiResponse<{ available_slots: TimeSlot[]; booked_slots?: string[] }>> => {
    const response = await fetch(
      `${API_BASE_URL}/doctors/${doctorId}/availability?date=${date}`
    );
    return handleResponse(response);
  },

  /**
   * Register a new doctor
   */
  register: async (data: {
    name: string;
    email: string;
    phone: string;
    specialty: string;
    consultation_duration?: number;
  }): Promise<ApiResponse<{ doctor_id: number; name: string; specialty: string }>> => {
    const response = await fetch(`${API_BASE_URL}/doctors/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * Doctor login with email and phone
   */
  login: async (data: {
    email: string;
    phone: string;
  }): Promise<ApiResponse<{ doctor_id: number; name: string; specialty: string; token: string }>> => {
    const response = await fetch(`${API_BASE_URL}/doctors/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * Get doctor statistics
   */
  getStats: async (doctorId: number): Promise<ApiResponse<DoctorStats>> => {
    const response = await fetch(`${API_BASE_URL}/doctors/${doctorId}/stats`);
    return handleResponse(response);
  },

  /**
   * Get doctor appointments
   */
  getAppointments: async (
    doctorId: number,
    params?: {
      date?: string;
      status?: string;
      limit?: number;
    }
  ): Promise<ApiResponse<{ appointments: Appointment[] }>> => {
    const queryParams = new URLSearchParams();
    if (params?.date) queryParams.append('date', params.date);
    if (params?.status) queryParams.append('status', params.status);
    if (params?.limit) queryParams.append('limit', params.limit.toString());

    const response = await fetch(
      `${API_BASE_URL}/doctors/${doctorId}/appointments?${queryParams}`
    );
    return handleResponse(response);
  },

  /**
   * Get doctor's patients
   */
  getPatients: async (doctorId: number): Promise<ApiResponse<{ patients: any[] }>> => {
    const response = await fetch(`${API_BASE_URL}/doctors/${doctorId}/patients`);
    return handleResponse(response);
  },

  /**
   * Get doctor analytics
   */
  getAnalytics: async (
    doctorId: number,
    params?: {
      start_date?: string;
      end_date?: string;
    }
  ): Promise<ApiResponse<Analytics>> => {
    const queryParams = new URLSearchParams();
    if (params?.start_date) queryParams.append('start_date', params.start_date);
    if (params?.end_date) queryParams.append('end_date', params.end_date);

    const response = await fetch(
      `${API_BASE_URL}/doctors/${doctorId}/analytics?${queryParams}`
    );
    return handleResponse(response);
  },
};

// ============================================
// APPOINTMENT ENDPOINTS
// ============================================

export const appointmentApi = {
  /**
   * Book a new appointment
   */
  book: async (data: {
    user_id: number;
    doctor_id: number;
    date: string;
    time: string;
    reason?: string;
    sync_calendar?: boolean;
  }): Promise<ApiResponse<{ appointment_id: number; appointment: Appointment }>> => {
    const response = await fetch(`${API_BASE_URL}/appointments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * Get patient's appointments
   */
  getByPatient: async (
    userId: number,
    futureOnly: boolean = false
  ): Promise<ApiResponse<{ appointments: Appointment[] }>> => {
    const response = await fetch(
      `${API_BASE_URL}/appointments/${userId}?future_only=${futureOnly}`
    );
    return handleResponse(response);
  },

  /**
   * Cancel an appointment
   */
  cancel: async (appointmentId: number): Promise<ApiResponse<any>> => {
    const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}/cancel`, {
      method: 'PUT',
    });
    return handleResponse(response);
  },

  /**
   * Approve an appointment (doctor only)
   */
  approve: async (appointmentId: number): Promise<ApiResponse<any>> => {
    const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}/approve`, {
      method: 'PUT',
    });
    return handleResponse(response);
  },

  /**
   * Reject an appointment (doctor only)
   */
  reject: async (appointmentId: number): Promise<ApiResponse<any>> => {
    const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}/reject`, {
      method: 'PUT',
    });
    return handleResponse(response);
  },

  /**
   * Add notes to appointment (doctor only)
   */
  addNotes: async (
    appointmentId: number,
    notes: string
  ): Promise<ApiResponse<any>> => {
    const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes }),
    });
    return handleResponse(response);
  },

  /**
   * Update appointment notes
   */
  updateNotes: async (
    appointmentId: number,
    notes: string
  ): Promise<ApiResponse<any>> => {
    const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}/notes`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes }),
    });
    return handleResponse(response);
  },

  /**
   * Update appointment status
   */
  updateStatus: async (
    appointmentId: number,
    status: 'scheduled' | 'completed' | 'cancelled' | 'no-show'
  ): Promise<ApiResponse<any>> => {
    const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    return handleResponse(response);
  },

  /**
   * Get patient appointment history (for doctors)
   */
  getPatientHistory: async (
    patientId: number
  ): Promise<ApiResponse<{ appointments: Appointment[] }>> => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/appointments`);
    return handleResponse(response);
  },
};

// ============================================
// CHAT ENDPOINTS
// ============================================

export const chatApi = {
  /**
   * Send a message to medical AI assistant
   */
  sendMessage: async (
    userId: number,
    message: string
  ): Promise<ApiResponse<{ answer: string; sources?: string[] }>> => {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, message }),
    });
    return handleResponse(response);
  },

  /**
   * Create WebSocket connection for real-time chat
   */
  connectWebSocket: (userId: number, onMessage: (data: any) => void) => {
    const ws = new WebSocket(`${WS_BASE_URL}/api/v1/ws/chat/${userId}`);

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return {
      send: (message: string) => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ message }));
        }
      },
      close: () => ws.close(),
    };
  },
};

// ============================================
// SYSTEM ENDPOINTS
// ============================================

export const systemApi = {
  /**
   * Health check
   */
  health: async (): Promise<ApiResponse<any>> => {
    const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/health`);
    return handleResponse(response);
  },

  /**
   * Get API info
   */
  info: async (): Promise<ApiResponse<any>> => {
    const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/`);
    return handleResponse(response);
  },
};

// Export default API client
export default {
  patient: patientApi,
  doctor: doctorApi,
  appointment: appointmentApi,
  chat: chatApi,
  system: systemApi,
};
