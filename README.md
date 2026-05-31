# 🏦 ABC Bank Management System

A comprehensive desktop banking application built with Python and Tkinter, featuring customer account management, secure transactions, and admin controls.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Installation Guide](#installation-guide)
- [Executable Creation](#executable-creation)
- [Database Schema](#database-schema)
- [User Guide](#user-guide)
- [Module Documentation](#module-documentation)
- [Security Features](#security-features)
- [Error Handling](#error-handling)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The **ABC Bank Management System** is a feature-rich desktop application that simulates core banking operations. It provides separate interfaces for administrators and customers, enabling efficient account management, secure transactions, and real-time balance updates.

### Key Highlights
- ✅ **Dual Interface** - Separate dashboards for Admin & Customer
- ✅ **Secure Authentication** - Password protection with CAPTCHA verification  
- ✅ **Real-time Operations** - Deposit, Withdraw, Transfer functionality
- ✅ **Email Integration** - Automated notifications for account activities
- ✅ **OTP Verification** - Two-factor authentication for sensitive operations
- ✅ **Session Management** - Logout and timeout features
- ✅ **Standalone Executable** - Run without Python installation

## ✨ Features

### 👑 Admin Features
| Feature | Description |
|---------|-------------|
| **Create Account** | Open new bank accounts with auto-generated credentials |
| **View Account** | Search and display complete account details |
| **Close Account** | Delete accounts with OTP verification |
| **Email Notifications** | Automatic credential delivery via email |

### 👤 Customer Features
| Feature | Description |
|---------|-------------|
| **Show Details** | View personal account information |
| **Edit Details** | Update name, email, mobile, password |
| **Deposit Money** | Add funds to account |
| **Withdraw Money** | Withdraw funds with balance validation |
| **Transfer Funds** | Transfer money between accounts |
| **Forgot Password** | Recover password via OTP verification |

### 🔐 Security Features
- **CAPTCHA Verification** - Prevents automated login attempts
- **OTP Authentication** - Email-based OTP for password recovery & account closure
- **Password Hiding** - Masked password entry fields
- **Session Isolation** - Separate user sessions with proper cleanup

## 🛠 Technology Stack

```yaml
Frontend:
  - Tkinter: GUI framework
  - PIL/Pillow: Image processing
  - Custom Fonts: Comic Sans MS

Backend:
  - Python 3.8+
  - SQLite3: Database management

Security:
  - Custom CAPTCHA generator
  - OTP generation module
  - Email SMTP integration

Dependencies:
  - tkinter (built-in)
  - sqlite3 (built-in)
  - PIL (external)
  - smtplib (built-in)
  - auto-py-to-exe (for executable creation)
