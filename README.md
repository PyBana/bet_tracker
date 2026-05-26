# 🏋️‍♂️ 5kg Weight Loss Challenge Scoreboard

A full-stack, data-driven web application built to track a competitive weight loss challenge between friends. This app features a real-time progress tracker, dynamic burn-rate calculations, a private referee portal for secure logs, and a cloud-hosted database backend.

## 🚀 Live Demo
https://5kgbloodpact.streamlit.app/
---

## ✨ Features

* **Real-Time Leaderboard:** Instantly ranks competitors based on total weight lost, percentage of goal achieved, and remaining weight to target.
* **Dynamic Analytics:** Calculates the precise daily weight loss "burn rate" required for each participant to hit their 5kg target by the deadline.
* **Secure Referee Portal:** A password-protected administrative interface that allows authorized referees to add new weekly weight logs dynamically.
* **Automatic Database Syncing:** All entry logs are instantly calculated and pushed to a secure cloud database, making the data immutable across user sessions.

---

## 🛠️ The Tech Stack

* **Frontend Framework:** `Streamlit` (Python-based interactive web framework)
* **Data Processing:** `Pandas` (for structural sorting, math, and analytics generation)
* **Database Backend:** `Supabase` (Cloud-hosted PostgreSQL database)
* **Object-Relational Mapping (ORM):** `SQLAlchemy` & `psycopg2` (for secure Python-to-SQL communication)
* **Deployment:** `Streamlit Community Cloud` with `Supavisor Connection Pooling` (IPv4-to-IPv6 routing proxy)

---

## 🔒 Security Architecture

To protect production infrastructure and operational integrity, this repository utilizes industry-standard security protocols:
* **Separation of Concerns:** All database connection strings and master passwords are completely abstracted out of the frontend source code.
* **Environment Secrets:** Sensitive credentials are injected into runtime variables using Streamlit's secure encrypted `.secrets` vault.
* **Git Shielding:** Local configuration files (`.streamlit/secrets.toml`) and text-editor variables are explicitly sandboxed via a custom `.gitignore` file to ensure zero operational keys are committed to version control.
