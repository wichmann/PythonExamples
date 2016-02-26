#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# Name:        chatserver
# Usage:       - Start ChatServer with: ./chatserver.py
#              - Connect with browser to: http://127.0.0.1:5000/chatserver
#              - Start chatting...
#
# Author:      Christian Wichmann
#
# Created:     26.02.2016
# Copyright:   (c) Christian Wichmann 2016
# Licence:     GNU GPL
#-------------------------------------------------------------------------------

from flask import Flask
from flask import request
from flask import jsonify


# initialize Flask server
app = Flask(__name__)

# create template for HTML page
chatwindow = """
             <html><head>
             <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
             </head><body>
             <h1>Chat</h1>
             <p><textarea id="messagewindow" rows="40" cols="100"></textarea></p>
             <p><input type="text" size="60" id="newmessage" />
             <button type="button" id="sentbutton">Absenden</button></p>
             </body>
             <script type="text/javascript">
             var startmessage = "Neue Nachricht...";
             $("#newmessage").value = startmessage;
             $("#newmessage").bind("click", function() {
                 if ($("#newmessage").value == startmessage) {
                     $("#newmessage").value = "";
                 }
             }, false);
             
             $("#sentbutton").bind("click", function() {
                 var message = $("#newmessage").val();
                 $.post("chatserver/sentmessage", {message: message});
             }, false);
             
             function compileMessages(data) {
                 var allmessages = "ChatServer\\n";
                 for (d in data.data) {
                     allmessages += data.data[d]['sender'];
                     allmessages += ": ";
                     allmessages += data.data[d]['text'];
                     allmessages += "\\n";
                 }
                 return allmessages;
             }
             
             window.setInterval(function() {
                 $.getJSON("chatserver/getmessages", function(data) {
                     $("#messagewindow").val(compileMessages(data));
                 });
             }, 500);
             </script>
             </html>
             """

# create list for all messages that have been sent
all_messages = []


@app.route('/chatserver')
def chatserver():
    return chatwindow


@app.route('/chatserver/sentmessage', methods=['POST'])
def sent_messages():
    global all_messages
    all_messages.append({'sender': str(request.remote_addr), 'text': str(request.form['message'])})
    return ''


@app.route('/chatserver/getmessages', methods=['GET'])
def get_messages():
    global all_messages
    return jsonify(data=all_messages)


if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug = True)

