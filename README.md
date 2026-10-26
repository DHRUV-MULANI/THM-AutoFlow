# THM-AutoFlow

**Automated TryHackMe Challenge Interaction & Submission Framework**

THM-AutoFlow is a Python-based automation framework designed for structured TryHackMe challenge interaction, task submission workflows, session management, and API-driven learning environments. Built for speed, organization, logging, and repeatable educational automation.

## Features

- **Automated Task Submission** - Streamlined workflow for submitting answers to TryHackMe challenges
- **Session Management** - Persistent session handling with authentication support
- **Request Automation** - Structured framework for interacting with TryHackMe APIs
- **Logging & Organization** - Comprehensive logging for tracking automation activities
- **Modular Architecture** - Extensible design for custom automation workflows

## Tech Stack

- **Language**: Python
- **Web Framework**: Flask
- **Automation**: Custom request handling framework

## Installation

```bash
# Clone the repository
git clone https://github.com/DHRUV-MULANI/THM-AutoFlow.git
cd THM-AutoFlow

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the Flask application
python flask_app.py

# Or use the automation scripts
python thm_streak_helper.py
```

## Files

- `flask_app.py` - Web interface for automation control
- `thm_new/` - Core automation modules
- `thm_streak_helper.py` - Streak maintenance automation
- `Dockerfile` - Containerized deployment configuration

## Disclaimer

This tool is intended for educational purposes and ethical automation within TryHackMe's terms of service. Please use responsibly and in accordance with TryHackMe's rules.

## Author

[Dhruv Mulani](https://github.com/DHRUV-MULANI)
