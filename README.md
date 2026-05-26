# 🚀 W++ Compiler Analyzer

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26.svg?logo=html5&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC.svg?logo=tailwind-css&logoColor=white)
![Academic](https://img.shields.io/badge/CS--310-Compiler_Construction-8A2BE2.svg)

A modern, high-performance web-based compiler suite for the custom **W++** programming language. Developed as part of the CS-310 Compiler Construction course (Spring 2K26). 

This suite features a robust **Lexical Analyzer (Scanner)** and a **Recursive Descent Syntax Analyzer (Parser)**, wrapped in a sleek, responsive FastAPI + Tailwind CSS frontend.

---

## ✨ Features

### 🔍 Task 1: Lexical Analyzer (Scanner)
- **Comprehensive Tokenization:** Identifies and categorizes keywords, separators, operators, identifiers, and literals.
- **Detailed Statistical Breakdown:** Calculates occurrences, percentages, and exact line number tracking for every token.
- **Ignored Entities:** Properly handles and ignores single-line (`//`), multi-line (`/* */`) comments, and whitespace.

### 🏗️ Task 2: Syntax Analyzer (Parser)
- **Recursive Descent Parsing:** Validates grammatical structure including nested loops (`for`, `while`), conditional blocks (`if/else`), and math expressions.
- **Panic-Mode Error Recovery:** Does not crash on the first error! The parser smartly syncs to the next safe token (like `;` or `}`) to catch and report **multiple syntax errors** in a single pass.
- **Scope Tracking:** Accurately counts `{` and `}` to report missing end-of-file closures.
- **Pinpoint Accuracy:** Reports the exact line number of missing terminators rather than bleeding into subsequent lines.

### 🖥️ User Interface
- **Premium Web Dashboard:** Built with Vanilla HTML, JS, and Tailwind CSS.
- **Drag & Drop Upload:** Instantly upload `.wpp` source files for processing.
- **Interactive Data Tables:** View token analytics across multiple tabs with animated metric counters.

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn (ASGI Server)
- **Frontend:** HTML5, JavaScript, Tailwind CSS (via CDN)
- **Data Parsing:** Pydantic, Python-Multipart

---

## 🚀 Installation & Setup

Follow these steps to run the compiler suite locally on your machine.

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/wpp-compiler-suite.git](https://github.com/your-username/wpp-compiler-suite.git)
cd wpp-compiler-suite

```

### 2. Install dependencies

Ensure you have Python 3.8+ installed. Install the required backend libraries using pip:

```bash
pip install fastapi uvicorn python-multipart

```

### 3. Run the Local Server

Launch the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload

```

### 4. Open the App

Open your web browser and navigate to:

```text
http://localhost:8000

```

---

## 📂 Project Structure

```text
📦 wpp-compiler-suite
 ┣ 📜 main.py              # FastAPI server, routing, and JSON formatting
 ┣ 📜 index.html           # Frontend dashboard (Tailwind CSS + JS)
 ┣ 📜 scanner.py           # Task 1: Token generator and stats calculator
 ┣ 📜 parser_backend.py    # Task 2: Recursive descent syntax parser
 ┣ 📜 README.md            # Project documentation
 ┗ 📂 test_files           # Directory containing valid and broken .wpp files

```

---

## 🧪 Testing the Compiler

The repository includes several `.wpp` test files to demonstrate the compiler's capabilities:

* `test_stress.wpp`: A completely valid program testing deeply nested scopes and complex math.
* `test_errors.wpp`: A file with 8 distinct syntax errors to demonstrate the parser's panic-mode recovery.
* `test_sneaky.wpp`: Tests edge cases like invalid operator sequences and reserved keyword misuse.

To test, simply drag and drop one of these files into the web dashboard!

---

## 👥 Project Team

This project was developed for **Spring 2K26 - Task #2** by:

| Name | Registration Number | Role |
| --- | --- | --- |
| **Eman Khaliq** | `23-CS-01` | Core Logic / UI Integration |
| **Muhammad Saad** | `23-CS-31` | Parser Development & Error Recovery |
| **Syed Noor ul Hassan** | `23-CS-85` | Scanner Architecture & Regex |

---

*Note: This is an academic project built for educational purposes regarding compiler design, lexical analysis, and syntax parsing.*

```

```
