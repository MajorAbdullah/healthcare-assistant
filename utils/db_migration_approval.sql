-- Migration: Add approval workflow to appointments
-- This adds a new status 'pending_approval' and email notification tracking

-- Add new status values to appointments
-- Update the status check constraint
-- Note: SQLite doesn't support ALTER TABLE to modify CHECK constraints
-- We'll handle the new 'pending_approval' status in the application logic

-- The status field now supports:
-- 'pending_approval' - waiting for doctor approval (NEW)
-- 'confirmed' - doctor approved
-- 'scheduled' - old confirmed status
-- 'cancelled' - appointment cancelled
-- 'completed' - appointment completed

-- Add column to track if notification email was sent
ALTER TABLE appointments ADD COLUMN approval_email_sent BOOLEAN DEFAULT 0;
ALTER TABLE appointments ADD COLUMN confirmation_email_sent BOOLEAN DEFAULT 0;
