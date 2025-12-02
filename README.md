# Scheduling Agreement Automation in SAP (ME38)

Automating the process of maintaining **Scheduling Agreements** in SAP using transaction **ME38**, driven by a **React** frontend and a **Flask** backend that leverages **SAP GUI Scripting** on Windows.  

This project is intended to reduce manual effort when updating schedule lines (dates and quantities) for multiple scheduling agreements based on a structured input file (CSV).

---

## 🔧 Tech Stack

- **Frontend**
  - React
  - HTML / CSS / JavaScript

- **Backend**
  - Python (Flask)
  - `pywin32` / SAP GUI Scripting
  - CSV handling (e.g. `pandas` / `csv`)

- **SAP**
  - SAP GUI for Windows
  - SAP MM – Scheduling Agreement (T-code **ME38**)
  - SAP GUI Scripting enabled on client & server

---

## 🧩 What This Project Does

- Takes input from a **CSV file** (`ME38.csv` is provided as an example template in the repo).
- The backend uses **SAP GUI Scripting** to:
  - Open transaction **ME38**.
  - Locate the relevant Scheduling Agreement and item.
  - Navigate through **Delivery Schedule** lines.
  - Read GRN / existing quantities (where required).
  - Update schedule quantities and dates based on the CSV.
  - Save the document and capture SAP status messages.
- The React frontend provides a simple UI to:
  - Upload the CSV file.
  - Trigger processing.
  - Show progress / result messages returned by the backend.

---

## 📁 Repository Structure

```text
Scheduling-Agreement-Automation-in-SAP/
├── backend/      # Flask backend + SAP GUI scripting logic
├── frontend/     # React frontend
├── ME38.csv      # Sample / template CSV for schedule data
└── .gitignore
```
## ⚙️ Prerequisites
OS & SAP

Windows machine (required for SAP GUI Automation).

SAP GUI for Windows installed.

SAP GUI Scripting:

Enabled on client (SAP GUI Options → Accessibility & Scripting).

Enabled on server by your SAP Basis team.

Backend

Python 3.x installed

Recommended: virtual environment

Frontend

Node.js (preferably v18+)

npm or yarn

## 🚀 Getting Started
### 1️⃣ Clone the repository
git clone https://github.com/sAdityas/Scheduling-Agreement-Automation-in-SAP.git
cd Scheduling-Agreement-Automation-in-SAP

### 2️⃣ Backend Setup (Flask + SAP Scripting)
cd backend

# (optional but recommended)
python -m venv venv
venv\Scripts\activate  # on Windows

# Install dependencies (adjust file name if different)
pip install -r requirements.txt


Configure any required environment values (for example, SAP system / client / language if your code uses them).
The backend typically:

Exposes an endpoint to accept CSV upload.

Starts the Flask server on some port (e.g. http://localhost:5000).

Example (if your entry file is app.py):

python app.py


Check your backend file name and run accordingly.

### 3️⃣ Frontend Setup (React)

In a new terminal:

cd ../frontend

# Install dependencies
npm install

# Start dev server
or npm start


By default, React will run on something like http://localhost:3000.

Make sure the frontend is configured to call the backend API URL
(e.g. http://localhost:5000/api/...). If needed, adjust:

A config file (e.g. src/config.js)

Or environment variables (e.g. .env for Vite/CRA)

### 🔄 Typical Workflow

Prepare Input

Download or open ME38.csv.

Fill in the necessary fields for each schedule line (e.g. scheduling agreement, item, date, quantity, etc. depending on your implementation).

Start Services

Ensure SAP GUI is installed and you are able to log in manually.

Run the Flask backend.

Run the React frontend.

Use the UI

Open the frontend in your browser.

Select / upload the ME38.csv file.

Click the Process / Submit button.

Automation in SAP

Backend receives the file.

For each row, SAP GUI scripting:

Opens ME38.

Navigates to the correct Scheduling Agreement.

Updates schedule lines as per file.

Saves and logs any errors / success messages.

Review Results

View success / error messages on the frontend.

Validate a few agreements manually in SAP to confirm expected changes.

## ⚠️ Important Notes / Limitations

This automation runs on the client machine where:

SAP GUI is installed.

Python + pywin32 are running.

Session locking:

Only one automation run should control a given SAP GUI session instance at a time.

Always test in a non-production environment first.

Handle sensitive data (e.g. SAP credentials) securely. Avoid hard-coding usernames/passwords.

## 🛠️ Possible Improvements (To-Do)

Add proper logging UI for:

Row-level success/failure details.

Exportable logs (CSV/Excel).

Add authentication on the web app (e.g. simple login or SSO).

Add configuration page:

Default SAP client, language, and system.

Mapping of CSV columns → SAP fields.

Introduce dry-run mode (simulate without posting changes).

Dockerize backend (still requires Windows + SAP GUI inside host for scripting).

## 🤝 Contributing

Feel free to fork this repository and adapt it for your own plant / business rules.
Pull requests for:

Bug fixes

Better error handling

Additional examples of CSV formats

…are always welcome.

# 📄 License

This project is intended as a learning / internal automation tool.
You can apply any license you prefer; if you add one, mention it here.

# 👤 Author

## Built by Aditya Sarkale (@sAdityas)
## Automation for Scheduling Agreement ME38 with React + Flask + SAP GUI Scripting.
