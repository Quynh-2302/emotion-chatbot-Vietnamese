# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:18:16 2016
@author: winpython
"""

import os
from flask import Flask, request, send_file, send_from_directory, session, render_template
from werkzeug import secure_filename
# belows include self-define libs and func
from AWWW_wav_to_spectro import wav2sep
from AWWW_wav_to_STT import input_filename
from AWWW_jiebaCut import func_cut
from AWWW_chatbot_response import Chat_with_Bot
from AWWW_pic_pred import pred
from file_del import pred_del


# aboves include self-define libs and func
import numpy as np
import json

#ans_test = pred_test()

#from chatbot import chatbot
#AkishinoProjectBot = chatbot.Chatbot()
#AkishinoProjectBot.main(['--modelTag', 'taiwa20170709', '--test', 'daemon'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['wave', 'wav'])




def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()



@app.route('/')
def index():
    return render_template('index.html')


@app.route("/res", methods=['get', 'POST'])
def res():
    if request.method == 'POST':
        file = request.files['file']
         
        if file and allowed_file(file.filename):
			#print(file)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',filename = filename))
			
			# Wave file to spectrogram 
            wav2sep(filename)
            # image file to digits server Recognition
            ans = pred()

			#Chatbot processing (jieba cut)
            
            
            # below decode json from nvidia digits output
            jsondec = json.loads(ans.decode('utf8'))
            jsondec = jsondec['predictions']
            jsondec = str(jsondec).replace("[", "")
            jsondec = str(jsondec).replace("]", "")
            jsondec = "{" + jsondec + "}"
            jsondec = jsondec.replace("',", "':")
            jsondec = jsondec.replace("'", '"')
            jsondec = json.loads(jsondec)  
            maxpred = (max(jsondec['happy'], jsondec['sad'], jsondec['calm'], jsondec['fearful'], jsondec['angry']))
            

            if maxpred == jsondec['happy']:
                emotion = "開心 = " + str(maxpred)                 
                print("開心 : " + str(jsondec['happy']))

            elif maxpred == jsondec['sad']:
                emotion = "傷心 = " + str(maxpred)                 
                print("傷心 : " + str(jsondec['sad']))

            elif maxpred == jsondec['calm']:
                emotion = "平靜 = " + str(maxpred) 
                print("平靜 : " + str(jsondec['calm']))

            elif maxpred == jsondec['fearful']:
                emotion = "害怕 = " + str(maxpred) 
                print("害怕 : " + str(jsondec['fearful']))

            elif maxpred == jsondec['angry']:
                emotion = "生氣 = " + str(maxpred)                 
                print("生氣 : " + str(jsondec['angry']))

            else:
                print("無法辨識")


            Happy = "Happy = " + str(jsondec['happy'])
            Sad = "Sad = " + str(jsondec['sad'])
            Calm = "Calm = " + str(jsondec['calm'])
            Fearful = "Fearful = " + str(jsondec['fearful'])
            Angry = "Angry = " + str(jsondec['angry'])



            from chatbot import chatbot
            AkishinoProjectBot = chatbot.Chatbot()

            if maxpred == (jsondec['happy']):
                AkishinoProjectBot.main(['--modelTag', 'positive', '--test', 'daemon'])
            elif maxpred == jsondec['sad']:
                AkishinoProjectBot.main(['--modelTag', 'negative', '--test', 'daemon'])
            elif maxpred == jsondec['calm']:
                AkishinoProjectBot.main(['--modelTag', 'positive', '--test', 'daemon'])
            elif maxpred == jsondec['fearful']:
                AkishinoProjectBot.main(['--modelTag', 'negative', '--test', 'daemon'])
            elif maxpred == jsondec['angry']:
                AkishinoProjectBot.main(['--modelTag', 'negative', '--test', 'daemon'])
            else:
                print("無法辨識")

            asking = str(input_filename(filename))
            print("asking = " + asking)
            if  asking == "None":
                responsing = Chat_with_Bot(asking, AkishinoProjectBot)
                asking = "無法辨識"
                print("chatbot_responsing asking = " + responsing)
            else:   
                asking = func_cut(input_filename(filename))
                responsing = Chat_with_Bot(asking, AkishinoProjectBot)
                print("chatbot_responsing asking_res = " + responsing)                
                if responsing == "":
                   responsing = "無法回應"
                   print("responsing = " + responsing)

            #Wave file & image file delete
            ans_del = pred_del(filename)


	        #shutdown web server(flask server)   
            shutdown()

            #print(ans.decode('utf8').replace("\n"," "))
            # return ans.decode('utf8')
            #reload = restart()

                # Render template
            return render_template('res.html', Happy = Happy, Sad = Sad, Calm = Calm, Fearful = Fearful, Angry = Angry, ask = asking , res = responsing)
            #return '<p>%s        response = %s </p>' % (ans.decode('utf8'), responsing)
            #return (ans.decode('utf8') + "|" + responsing)


def shutdown():
    shutdown_server()
    print("Server shutting down...")
    return 'Server shutting down...'



@app.route("/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#port 4000、4040、5000、5050 is OK to External connection
if __name__ == "__main__" :
    app.run(host='0.0.0.0',port=5000)
