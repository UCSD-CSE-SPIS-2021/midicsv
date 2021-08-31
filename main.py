import py_midicsv as pm
import pandas as pd
import csv
import random

import os
from flask import Flask, url_for, render_template, request

app = Flask(__name__)

def midicsv:
# Load the MIDI file and parse it into CSV format
    csv_string = pm.midi_to_csv("TheWeeknd-BlindingLights.mid")

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

    csv_string1 = pm.midi_to_csv("TheWeeknd-BlindingLights.mid")
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
    with open("blinding.mid", "wb") as output_file:
        midi_writer = pm.FileWriter(output_file)
        midi_writer.write(midi_object)

