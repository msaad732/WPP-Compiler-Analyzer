from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import scanner
import parser_backend

app = FastAPI(title="W++ Compiler Suite")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/scanner")
async def run_scanner(file: UploadFile = File(...)):
    content = await file.read()
    results = scanner.run_token_analyzer(content.decode("utf-8"))

    # FIX 1: Convert tuple-keyed dicts to a clean list for JSON
    formatted_summary = []
    for (cat, t_type), qty in results["detailed_stats"].items():
        lines = sorted(list(set(results["detailed_lines"][(cat, t_type)])))
        formatted_summary.append({
            "category": cat,
            "token_type": t_type,
            "qty": qty,
            "lines": lines
        })
    results["formatted_summary"] = formatted_summary
    del results["detailed_stats"]
    del results["detailed_lines"]

    # FIX 2: line_distribution has integer keys — JSON only allows string keys
    results["line_distribution"] = {
        str(k): v for k, v in results["line_distribution"].items()
    }

    return {"filename": file.filename, "results": results}

@app.post("/api/parser")
async def run_parser(file: UploadFile = File(...)):
    content = await file.read()
    results = parser_backend.run_syntax_analyzer(content.decode("utf-8"))
    return {"filename": file.filename, "results": results}
