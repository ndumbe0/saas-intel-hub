param([string]$mode="dev")
if ($mode -eq "dev") {
  Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; uvicorn app.main:app --reload --port 8004"
  Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
}
