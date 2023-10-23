Python >=3.8
Postman has been used to check the post request

#To install
pip install -r requirements.txt

#To run the python HTTP server at port 8888 :
python server.py

#To execute the post request :
- open postman, create and launch post request with adequate body :
    * change request from GET to POST
    * enter the url http://localhost:8888/productionplan
    * in Body, put the raw content of the json file and specified the type from Text to Json
    * you can manually save the answer

- OR run the following command in the repertory containing the json files and user.py
    * python user.py "path_to/filename.json"
    * the answer will be printed in the command line
    * the answer will be saved in a json file in the same path as the input json file
