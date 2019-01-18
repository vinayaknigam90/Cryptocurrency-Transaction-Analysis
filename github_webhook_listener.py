from flask import Flask, request
import json
from subprocess import call
import os

app = Flask(__name__)

@app.route('/',methods=['POST'])
def deploy_docker():
   os.system('source ~/.bash_profile')
   os.system('./docker_stop_script.sh')
   os.system('docker build --no-cache -t bitcoin_transaction_analysis .')
   os.system('source ~/.bash_profile')
   os.system('docker run --rm -it -p 4000:4000 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY bitcoin_transaction_analysis')
#    call(["sudo","./docker_stop_script.sh"])
#    call(["sudo","docker","build","--no-cache","-t","bitcoin_transaction_analysis","."])
#    call(["sudo","docker","run", "--rm","-it","-p","4000:4000","-e","AWS_ACCESS_KEY_ID","=",",$AWS_ACCESS_KEY_ID","-e","AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY","bitcoin_transaction_analysis"])
   return "OK"

if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0', port=8081)