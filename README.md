<div align="center">
  <img width="100%" alt="W++ Compiler Suite Home" src="https://github.com/user-attachments/assets/f3365516-605b-4777-bdf4-d223a6315b6b" />
</div>

<br>

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
The Lexical Analyzer reads `.wpp` source code and breaks it down into a stream of logical tokens, calculating occurrences, percentages, and exact line number tracking.

<div align="center">
  <img width="100%" alt="Scanner Upload" src="https://github.com/user-attachments/assets/b4fa4fc6-f194-43c8-9d9c-ea2a1dbdef99" />
  <br><br>
  <img width="100%" alt="Token Summary" src="https://github.com/user-attachments/assets/4230bc51-5249-46dd-8bd0-ad21d20aef1c" />
</div>

- **Comprehensive Tokenization:** Identifies and categorizes keywords, separators, operators, identifiers, and literals.
- **Interactive Data Tables:** View token analytics across multiple tabs with animated metric counters for Identifiers, Literals, and Category Breakdowns.

<div align="center">
  <img width="100%" alt="ID and Literals" src="https://github.com/user-attachments/assets/9c5ffc24-1b7a-4eef-8faa-af87d4fed226" />
  <br><br>
  <img width="100%" alt="Analytics" src="https://github.com/user-attachments/assets/fe5642e8-a3ad-4384-a486-d3d9ae3f6108" />
</div>

---

### 🏗️ Task 2: Syntax Analyzer (Parser)
The Syntax Analyzer validates grammatical structure including nested loops (`for`, `while`), conditional blocks (`if/else`), and mathematical expressions.

<div align="center">
  <img width="100%" alt="Parser Upload" src="https://github.com/user-attachments/assets/785c97c7-426c-43b4-8166-ad9d83fe829f" />
</div>

- **Panic-Mode Error Recovery:** Does not crash on the first error! The parser smartly syncs to the next safe token (like `;` or `}`) to catch and report **multiple syntax errors** in a single compilation pass.
- **Pinpoint Accuracy:** Reports the exact line number of missing terminators rather than bleeding into subsequent lines.

<div align="center">
  <img width="100%" alt="Parser Errors 1-3" src="https://github.com/user-attachments/assets/4389d2b1-fa38-4ae0-8e64-5770fd7c3390" />
  <br><br>
  <img width="100%" alt="Source Code Viewer" src="https://github.com/user-attachments/assets/c294a69a-2cb5-43ee-bc28-a29a4b81e1ac" />
" />
</div>

---
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
git clone [https://github.com/msaad732/WPP-Compiler-Analyzer.git](https://github.com/msaad732/WPP-Compiler-Analyzer.git)
cd WPP-Compiler-Analyzer

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

* `test1.wpp:` A comprehensive test file containing variable declarations, math operations, conditionals, loops, and string manipulations to verify token generation.
* `error.wpp:` A file specifically designed to test the parser's error recovery, containing deliberate mistakes like missing semicolons, mismatched parentheses, and invalid assignments.
* `error2.wpp:` A "stress test" file that includes nested scopes, complex expressions, and I/O operations to ensure the parser can handle more complex logic without failing.
* `error3.wpp:` A file containing "sneaky errors," such as missing parentheses around conditions, double math operators, and using a reserved keyword as a variable name.
  
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
