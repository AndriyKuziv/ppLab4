1. After cloning repository, open command prompt
2. Using "cd" command go to project folder
3. Install/Update all dependencies using command "pip install -r requirements.txt"
4. Install flask: "pip flask install"
5. Install Waitress WSGI: "pip install waitress"
6. Launch Waitress server: "waitress-serve --port=5000 main:app"; 
   If server was launched successfully, then you will see message "INFO:waitress:Serving on http://0.0.0.0:5000"
7. Open browser and go to http://localhost:5000/api/v1/hello-world-2

Aaaand here we go! Now you have simple app in Flask that is totally useless