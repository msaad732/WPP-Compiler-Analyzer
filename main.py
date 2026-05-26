from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import scanner
import parser_backend

# This line was missing! It creates the 'app' that Uvicorn runs.
app = FastAPI(title="W++ Compiler Suite")

# Serve the Frontend HTML
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# API Endpoint for the Scanner
@app.post("/api/scanner")
async def run_scanner(file: UploadFile = File(...)):
    content = await file.read()
    results = scanner.run_token_analyzer(content.decode("utf-8"))
    
    # --- FIX: JSON doesn't support Tuple keys ---
    # We convert detailed_stats and detailed_lines into a clean list of dictionaries
    formatted_summary = []
    for (cat, t_type), qty in results["detailed_stats"].items():
        lines = sorted(list(set(results["detailed_lines"][(cat, t_type)])))
        formatted_summary.append({
            "category": cat,
            "token_type": t_type,
            "qty": qty,
            "lines": lines
        })
    
    # Add the clean list and remove the problematic tuple-key dictionaries
    results["formatted_summary"] = formatted_summary
    del results["detailed_stats"]
    del results["detailed_lines"]
    
    return {"filename": file.filename, "results": results}

# API Endpoint for the Parser
@app.post("/api/parser")
async def run_parser(file: UploadFile = File(...)):
    content = await file.read()
    results = parser_backend.run_syntax_analyzer(content.decode("utf-8"))
    return {"filename": file.filename, "results": results}