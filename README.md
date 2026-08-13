<div align="center">
  <img src="https://via.placeholder.com/150x150.png?text=BugPilot" alt="BugPilot Logo" width="150" />
  <h1>BugPilot CLI</h1>
  <p><strong>Next-Generation AI-Powered Autonomous Penetration Testing Agent</strong></p>

  [![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)](https://github.com/l3tchupkt/BugPilot)
  [![Status](https://img.shields.io/badge/status-Production_Ready-success.svg)](https://github.com/l3tchupkt/BugPilot)
  [![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
</div>

<hr/>

## 🚀 Overview

**BugPilot CLI** is an advanced, AI-driven command-line agent designed for security researchers, penetration testers, and ethical hackers. Unlike standard AI wrappers, BugPilot acts as an **autonomous agent** capable of executing background tasks, intelligently managing its own context window, dynamically parsing tools on your system, and executing complex, multi-stage attacks or audits without constant supervision.

Whether you need to quickly look up a CVE, analyze OWASP vectors, or unleash a fully autonomous pentesting loop on a target, BugPilot is your AI red-teaming copilot.

---

## ✨ Key Features

### 🤖 Intelligent Autonomous Agent (Hacker Mode)
- **Unlimited Sessions**: No more arbitrary loop limits. BugPilot can run indefinitely until the target is compromised or the audit is complete.
- **Dynamic Context Management**: Automatically tracks real-time token usage and intelligently truncates older history via a rolling context window (up to ~32k tokens) so the agent never crashes from memory overflow.
- **Asynchronous Execution**: The LLM can launch long-running commands (like `nmap` or `ffuf`) in the background, continue reasoning or performing other tasks, and automatically receive notifications when background jobs finish.

### 🔌 Universal LLM Connectors
Seamlessly connect to the world's most powerful reasoning models via an interactive Terminal UI (`/connect`):
- **DeepSeek** (DeepSeek-Coder)
- **OpenRouter** (Access to Mistral, Cohere, xAI, TogetherAI, etc.)
- **Nvidia NIM** (Meta Llama 3 70B Instruct)
- **Anthropic Claude**, **OpenAI GPT-4**, **Google Gemini**, **Groq**, and local **Ollama** models.

### 🛠️ Built-in Security Knowledge Base
- **CVE Database Lookup**: Instantly search for CVEs, affected products, and severity vectors.
- **OWASP Top 10 Integration**: Pull detailed insights into standard vulnerabilities directly into the CLI.
- **Dynamic Tool Discovery**: BugPilot automatically detects which security tools (e.g., `nmap`, `nuclei`, `sqlmap`) are installed on your host OS and informs the LLM.

### 💻 Beautiful Terminal UI
- **Interactive Settings**: Use arrow keys to navigate beautiful `prompt_toolkit` powered menus for API keys, models, and limits.
- **Rich Markdown Outputs**: Syntax-highlighted code blocks, tables, and colored logs powered by `rich`.
- **7 Built-in Themes**: Customize the hacker aesthetic to your preference.

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/l3tchupkt/BugPilot.git
cd BugPilot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch BugPilot
python -m bugpilot
```

---

## 🎯 Quick Start

Upon launching BugPilot for the first time:

1. **Connect a Provider**: Type `/connect` (or `/settings`) to interactively select your preferred LLM provider (e.g., OpenRouter, DeepSeek) and enter your API key securely.
2. **Select Mode**: Use `/mode hacker` to give the AI autonomous control, or `/mode forge` for a standard Q&A assistant.
3. **Set a Target**: Type your instructions, for example:
   > *"Run a background nmap scan on 127.0.0.1, check for open ports, and search the CVE database for any outdated services you find."*

### Available Commands
| Command | Description |
|---|---|
| `/connect` | Quickly connect a new LLM provider via interactive dropdowns. |
| `/settings` | Open the comprehensive settings TUI. |
| `/mode [name]`| Switch operating modes (`hacker`, `forge`). |
| `/cve [query]`| Look up CVE information (e.g. `/cve CVE-2021-44228` or `/cve search apache`). |
| `/owasp [ID]` | Get OWASP Top 10 info (e.g. `/owasp A03`). |
| `/update` | Check and install the latest updates for BugPilot. |
| `/clear` | Clear the terminal screen. |
| `/help` | Show all available commands. |

---

## 📜 Changelog

### v1.4.0 (Latest)
- **Major Architecture Upgrade**: Implemented asynchronous tool calling (`background: true`) and a `wait_for_job` tool for the LLM.
- **Unlimited Sessions**: Removed hardcoded loop limits in Hacker Mode.
- **Context Rolling Window**: Built a dynamic token counter that intelligently truncates old history when approaching 32k tokens.
- **New UI**: Upgraded all settings menus to interactive `prompt_toolkit` dialogs.
- **Expanded Connectors**: Added native support for DeepSeek, OpenRouter, and Nvidia NIM.

### v1.3.5
- Added robust CVE and OWASP lookup tools.
- Integrated `rich` for enhanced terminal formatting.
- Added foundational local LLM support via Ollama.

---

## 🔮 Upcoming Features (Roadmap)

- [ ] **Multi-Agent Orchestration**: Spin up specialized sub-agents (e.g., an OSINT agent and an Exploitation agent) that communicate to solve complex red-teaming scenarios.
- [ ] **Web GUI Dashboard**: A localized web interface to view session trees, background tasks, and exported PDF reports in real-time.
- [ ] **RAG for Exploits**: Integrate a local vector database allowing BugPilot to ingest and retrieve thousands of PoC exploits automatically.
- [ ] **Plugin Marketplace**: A standardized format for the community to write and share custom Python skills for the agent.

---

## 🛡️ Security Policy
Please review our [SECURITY.md](SECURITY.md) for information on supported versions and responsible disclosure guidelines. 

---

## 🤝 Contributing
Contributions are highly encouraged! 
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Ensure all tests pass (`python -m pytest tests/unit/`).
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5. Push to the branch (`git push origin feature/AmazingFeature`).
6. Open a Pull Request.

---
<div align="center">
  <b>Developed by LAKSHMIKANTHAN K (letchupkt)</b><br/>
  <i>Happy Hunting!</i>
</div>
