# Solairam P - MAPIMS HRMS Enterprise Portal & Management Suite

A modern, responsive, and full-featured HRMS suite built from live data and client architectures extracted from `https://mapims-hrms.tecvinesolutions.com`.

---

## 🌟 Integrated Pages & Modules (All 13 Pages)

### 👤 Section 1: Employee Self-Service (ESS)
1. **Overview Dashboard**: High-level KPIs, biometric in/out punches for today, work hours, 6-month net pay chart, and 1-click access to all modules.
2. **My Attendance & Timesheet**: 31-day salary cycle (25-Oct to 24-Nov), biometric punch timestamps (ESSL), status filtering.
3. **Staff Attendance Lookup (by Reg No) [NEW]**:
   - Lookup attendance timesheet for ANY of the 1,056 employees by Registration Number / Employee Code (e.g. `60493`, `10001`, `40173`, `21494`, etc.).
   - Full biometric punch details: Exact Check-In punch time, Check-Out punch time, total work duration (hours & minutes), punctuality (early / late), shift schedule, and biometric machine scanner ID.
   - Monthly performance metrics: Present days, total hours logged, average daily work duration, week-offs, and late logins.
   - Filter pills: All, Present, Week Off, Scheduled.
   - One-click CSV export of the employee's timesheet.
4. **Leaves & On-Duty**: Casual Leave (3/4 left), On-Duty (30/30 left), application logs, interactive "Apply Leave" modal.
5. **Payroll & Payslips**: October 2026 itemized pay advice (₹42k gross, ₹39,114 net), deductions (PF, ESI, PT), direct print to PDF.
6. **My Profile & Digital ID Badge**: Full personal, contact, family, banking, statutory details, and flippable corporate ID card.

### 🏢 Section 2: Administration & Management Suite
6. **User Management (`/users`)**: 
   - User table with search, role labels, department, designation, and status indicators.
   - Interactive **Invite User** modal with employee mapping, role assignments, and Super Admin privileges.
   - User actions: Edit, Resend Invite, Cancel Invite, Toggle Active/Inactive status.
   - Export User Directory to CSV.
7. **Role & Permissions Master (`/role_master`)**: 
   - Directory of all 10 platform roles (Employee, Admin, Super Admin, HR Manager, Department Head, etc.).
   - Permission key breakdown across 80 system modules (`HRATT`, `HREMP`, `HRPAY`, `HRUSER`, etc.).
8. **Organization Employee Directory (`/employee`)**: 
   - **All 1,056 Employee Census Records** fully mined from the backend API.
   - Enriched with all 52 hospital and academic departments (Nursing: 322, Housekeeping: 82, Operations: 61, Central Lab: 53, Maintenance: 42, Ophthalmology: 34, Radiology: 32, Electrical: 27, Anaesthesiology: 27, IT: 9, etc.).
   - Instant search across Employee Name, Code (`#60493`), Department, Designation, and Record ID.
   - Department filter dropdown with live record counts.
   - Status filtering (Active / Pending Onboarding).
   - Configurable pagination (10, 25, 50, 100, 250, All 1,056).
   - Instant CSV Export of the entire 1,056 dataset (`mapims_all_1056_employees.csv`).
   - Employee Census Detail modal for deep inspection.
9. **Shift Allocation & Roster (`/shift`)**: 
   - Catalog of 35 operational shifts (NG2, Week-Off, Morning, Evening, Night Rosters).
   - Biometric punch buffer (60 mins) and grace timing rules.
10. **Transport & Fleet Logistics (`/transport`)**: 
    - Staff bus routes (Route 1: Kanchipuram, Route 2: Cheyyur), bus vehicle numbers, drivers, departure/return schedules.
11. **Campus Accommodations (`/accommodation`)**: 
    - 14 residential hostel blocks (Blocks A through N), staff quarters inventory.
12. **Statutory & Compliance Reports (`/report`)**: 
    - EPF ECR Filing report, ESIC Monthly Returns, Loss of Pay (LOP) audit ledger.
13. **System & Company Policies (`/company-policy`)**: 
    - Non-Teaching payroll policy settings, salary cycle dates (25th start, 24th cut-off), PF calculation basis (Basic + DA).

---

## 🚀 Running the Portal

The local server is running at:
👉 **[http://localhost:3000](http://localhost:3000)**

To launch manually if restarted:
```bash
python server.py
```
Or open [`index.html`](file:///c:/Users/P%20S%20RAM/Desktop/hrms/index.html) directly in any browser.

---

## 🔄 Re-Sync with Live HRMS
Click the **"Sync Live"** button in the header or run:
```bash
python sync_hrms.py 7200504251 Solai@123
```
To run the full multi-module miner:
```bash
python fetch_everything.py
```
