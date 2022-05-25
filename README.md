# Command create venvn
´´´
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn
uvicorn main:app --reload
´´´
