Backend --install /projects
check for python version. if not, download python latest.

> pip install openai fastapi uvicorn python-multipart
> pip install -r requirements.txt
> python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

After running this, in your command prompt 
>ipconfig
In Windows
check for iP4 address copy and paste in frontend, backend url
In Mac
ipconfig getifaddr en0;
