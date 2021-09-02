import py_midicsv as pm
#import pandas as pd
import csv
import random
import requests


from werkzeug.utils import secure_filename
import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file


global_file = None
app = Flask(__name__)

@app.route('/')
def render_main():

    return render_template('home.html')

print(os.path.dirname(os.path.abspath(__file__)))


UPLOAD_FOLDER = '/home/runner/midicsv/templates/user_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 25*1000*1000
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mid'}

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print ("LINE 19")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print ("LINE 29")
            filename = secure_filename(file.filename)
            global global_file
            global_file = filename
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    
    return render_template('upload.html')





@app.route('/midi_csv')
def render_midi_csv():
    try:

        

        midi_csv()

        return send_file("ringtone.mid", as_attachment = True)

    except ValueError:

        return "Sorry: something went wrong."

    #return render_template('midi_csv.html')




        

def midi_csv():
# Load the MIDI file and parse it into CSV format
    #call download_link()
    print(global_file)
    #name_file_without_ext = global_file.rsplit('.', 1)[0]
    csv_string = pm.midi_to_csv("./templates/user_uploads/"+ global_file)
    
    notes_list = []

    with open("example_converted.csv", "w") as f:
        f.writelines(csv_string)



    with open("example_converted.csv") as a:
        data = csv.reader(a)
        for line in data:
            #print (line)
            if (line[2]== " Note_on_c"):
                notes_list.append(int(line[4]))



    chain = {}  
    n_notes = len(notes_list)  
    for i, key1 in enumerate(notes_list):  
        if n_notes > i + 2:
            key2 = notes_list[i + 1]
            note = notes_list[i + 2]
            if (key1, key2) not in chain:
                chain[(key1, key2)] = [note]
        
            chain[(key1, key2)].append(note)

    for (a,b) in chain:
        if (len(chain[(a,b)])) == 1:
            del chain[(a,b)]
    



    markov_new_notes = []


    key= random.choice(list(chain.keys()))
    #key = (notes_list[0], notes_list[1])
    print(key)
    j = 0

    doesnt_work = True
    while j < len(notes_list)-1:
    
        markov_new_notes.append(key[0])
        markov_new_notes.append(key[1])
        while doesnt_work:
            try:

                key = (key[1], random.choice(list(chain[key])))
            except KeyError:
                key = (key[1], random.choice(list(chain[key])))
            doesnt_work = False
        j+=1
    #print(markov_new_notes)

    csv_string1 = pm.midi_to_csv("./templates/user_uploads/" +global_file)
    with open("example_converted1.csv", "w") as f:
        f.writelines(csv_string1)

    c = 0
    #print (markov_new_notes)
    new_val_list = []
    with open("example_converted1.csv") as b:
        data = csv.reader(b)
        #midi_writer = pm.FileWriter(b)
        #writer = csv.writer(b)
        for line in data:
            if (line[2]==" Note_on_c"):

                line[4] = str(markov_new_notes[c])
                c+=1
                #new_val_list.append(new_row)
                #print(line)
        
            new_val_list.append(line)
            #midi_writer.write(b)
            #writer.writerow(line)
    
        b.close()
            #writer.writerow(line) 
        #for line in data:
            #print(line)
    #with open("example_converted1.csv", 

        
    with open("example_converted1.csv", "w") as z:
        writer = csv.writer(z)
        writer.writerows(new_val_list)
        z.close()


    # Parse the CSV output of the previous command back into a MIDI file
    midi_object = pm.csv_to_midi("example_converted1.csv")

    # Save the parsed MIDI file to disk
    with open("ringtone.mid", "wb") as output_file:
        midi_writer = pm.FileWriter(output_file)
        midi_writer.write(midi_object)

    
if __name__ == "__main__":

   app.run(host='0.0.0.0', debug=True)