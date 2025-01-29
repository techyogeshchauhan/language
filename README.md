# 🌐 Advanced Language Detection App 

A powerful multilingual text analysis tool built with Streamlit and Lingua

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red)
![Lingua](https://img.shields.io/badge/Lingua-1.3.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Supported Languages](#-supported-languages)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

## 🔍 Overview

The Advanced Language Detection App is a web-based tool that accurately identifies the language of input text across 26 different languages. It provides confidence scores, maintains a detection history, and offers a user-friendly interface for language analysis.

<antArtifact identifier="system-flow" type="application/vnd.ant.mermaid" title="System Flow Diagram">
flowchart LR
    A[User Input] --> B[Text Processing]
    B --> C[Language Detection]
    C --> D[Confidence Scoring]
    D --> E[Results Display]
    E --> F[History Storage]
    
    style A fill:#f0f8ff,stroke:#333,stroke-width:2px
    style B fill:#f0f8ff,stroke:#333,stroke-width:2px
    style C fill:#f0f8ff,stroke:#333,stroke-width:2px
    style D fill:#f0f8ff,stroke:#333,stroke-width:2px
    style E fill:#f0f8ff,stroke:#333,stroke-width:2px
    style F fill:#f0f8ff,stroke:#333,stroke-width:2px
