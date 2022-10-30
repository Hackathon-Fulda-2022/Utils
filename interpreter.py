from datetime import datetime
import nltk
import copy
import random

#dictionary for vitality information
vitals_dict = {
    'vitType': '',
    'vitValue': '',
    'vitDateTime': '',
    'patientName': '',
    'employeeName': '',
    'vitReleased': ''
}

#dictionary for prescribed medications
medication_dict = {
    'medNumber': '',
    'patientName': '',
    'employeeName': '',
    'medName': '',
    'dose': '',
    'form': '',
    'dateTime': '',
    'note': '',
    'reason': '',
    'medReleased': ''
}

dict
patientcondition_dict = {
    'pcId': '',
    'pcPatientName': '',
    'pcDateTime': '',
    'pcType': '',
    'pcText': '',
    'pcEmployeeName': '',
    'pcReleased': '',
}

patientRequest_dict = {
    'patientName': '',
    'pRStartDateTime': "",
    'pREmployee': '',
    'pREndDateTime': '',
    'pRText': '',
    'pRPrio': '',
}


vit_array = []
med_array = []
con_array = []
pre_array = []


keys_patient = ["Patienten", "Patientenname", "Patient"]
keys_nurse = ["Pfleger", "Pflegername"]
key_ende = ["Ende", "Ende."]

keys_vit = [["Herzfrequenz", "Puls", "Pulsfrequenz"],
            ["Blutdruck", "Gefäßdruck", "systolisch", "Oberdruck"],
            ["Blutdruck", "Gefäßdruck", "diastolisch", "Unterdruck"],
            ["Körpertemperatur", "Temperatur"],
            ["Gewicht", "Köpergewicht", "wiegen", "wiegt"],
            ["Atemfrequenz"],
            ["Sauerstoffsättigung"],
            ["Blutzucker"],
            ["Erythrozyten"],
            ["Leukozyten"],
            ["Thrombozyten"],
            ["Hämatokrit"],
            ["Hämoglobin"],
            ["Cholesterin"],
            ["Schmerzempfinden", "Schmerzen"], 
            ["Bradenscore"],
            ["Brassindex"],
            ["Biensteinskala"],
            ["Stuhlausscheidung", "Stuhl", "Stuhlgang"],
            ["Flüssigkeitsaufnahme"],
            ["Größe", "Körperhöhe"],
            ["Stürze"]]

keys_med = [["Medikament"],
            ["Dosis", "Menge"],
            ["Form"],
            ["Notiz", "Anhang", "Anmerkung"],
            ["Grund", "Begründung"]]

keys_con = [["Schwere"],
            ["Beschreibung", "Status", "Situation"]]

keys_pre = [["große", "hilfe", "schnell", "dringend", "sofort"],
            ["kann", "brauche"],
            ["könnte", "bräuchte"]]

def interpreter (text):

    vitals_dict['vitType'] = ''
    vitals_dict['vitValue'] = ''
    vitals_dict['vitDateTime'] = datetime.timestamp(datetime.now())
    vitals_dict['patientName'] = ''
    vitals_dict['employeeName'] = ''
    vitals_dict['vitReleased'] = ''

    medication_dict['medNumber'] = ''
    medication_dict['patientName'] = ''
    medication_dict['employeeName'] = ''
    medication_dict['medName'] = ''
    medication_dict['dose'] = ''
    medication_dict['form'] = ''
    medication_dict['dateTime'] = datetime.timestamp(datetime.now())
    medication_dict['note'] = ''
    medication_dict['reason'] = ''
    medication_dict['medReleased'] = ''

    patientcondition_dict['pcId'] = ''
    patientcondition_dict['pcPatientName'] = ''
    patientcondition_dict['pcDateTime'] = datetime.timestamp(datetime.now())
    patientcondition_dict['pcType'] = ''
    patientcondition_dict['pcText'] = ''
    patientcondition_dict['pcEmployeeName']= ''
    patientcondition_dict['pcReleased'] = ''

    patientRequest_dict['patientName'] = ''
    patientRequest_dict['pRStartDateTime'] = datetime.timestamp(datetime.now())
    patientRequest_dict['pREmployee'] = ''
    patientRequest_dict['pREndDateTime'] = ''
    patientRequest_dict['pRText'] = ''
    patientRequest_dict['pRPrio'] = ''


    text = text.replace(".", "")
    text = text.replace(",", ".")
    text = text.split()
    
    #check if not patient request
    if text[0][:1] != '#':
    
        get_patient_name(text)
        get_employee_name(text)
        
        #interpret vitality parameter
        for x in range(len(keys_vit)):
            pos = find_position(text, keys_vit[x])
            if pos != -1: get_vit_value(text, pos, x)
        
        #count number of prescribed medications
        values = []
        for idx, value in enumerate(text):
            if value == "medikament":
                values.append(idx)
        values.append(len(text))
        
        #interpret and save medication parameter
        for i in range(len(values)):
            if i == len(values) - 1:
                break
            medication_dict['medName'] = get_next_string(text, values[i], 1)[0]
            medication_dict['medNumber'] = random.randint(0,1000)
            pos = find_position(text[values[i]:values[i + 1]], keys_med[1])
            if pos != -1: medication_dict['dose'] = get_next_value(text[values[i]:values[i + 1]], pos)
            pos = find_position(text[values[i]:values[i + 1]], keys_med[2])
            #get form
            pos = find_position(text[values[i]:values[i + 1]], keys_med[3])
            end = find_position(text[pos + values[i]:values[i + 1]], key_ende)
            if pos != -1: medication_dict['note'] = get_string(text[pos + 1 + values[i]:pos + end + values[i]])
            pos = find_position(text[values[i]:values[i + 1]], keys_med[4])
            end = find_position(text[pos + values[i]:values[i + 1]], key_ende)
            if pos != -1: medication_dict['reason'] = get_string(text[pos + 1 + values[i]:pos + end + values[i]])
            
            med_array.append(copy.deepcopy(medication_dict))
        
        #counts number of incidences concerning patient condition
        values = []
        for s in keys_con[0]:
            for idx, value in enumerate(text):
                if value == s:
                    values.append(idx)
        values.append(len(text))
        
        #interpret and save patient condition parameters
        for i in range(len(values)):
            if i == len(values) - 1:
                break
            patientcondition_dict['pcType'] = get_next_value(text[values[i]:values[i + 1]], 0)
            pos = find_position(text[values[i]:values[i + 1]], keys_con[1])
            end = find_position(text[pos + values[i]:values[i + 1]], key_ende)
            if pos != -1: patientcondition_dict['pcText'] = get_string(text[pos + 1 + values[i]:pos + end + values[i]])
            
            con_array.append(copy.deepcopy(patientcondition_dict))
        
    #attend to patient reguests
    else:
        
        #searching for keywords and evaluate them
        text[0] = text[0].replace('#', '')
        grade = 0
        values = []
        for x in keys_pre[0]:
            for idx, value in enumerate(text):
                if value == x:
                    values.append(idx)
        grade = grade + len(values)
        values = []
        for x in keys_pre[1]:
            for idx, value in enumerate(text):
                if value == x:
                    values.append(idx)
        grade = grade
        values = []
        for x in keys_pre[2]:
            for idx, value in enumerate(text):
                if value == x:
                    values.append(idx)
        grade = grade - len(values)
        
        #interpret and save patient request
        if grade < -2: patientRequest_dict['pRPrio'] = 'niedrig'
        if grade < 3: patientRequest_dict['pRPrio'] = 'mittel'
        if grade > 2: patientRequest_dict['pRPrio'] = 'hoch'
        
        patientRequest_dict['pRText'] = get_string(text)
        
        pre_array.append(patientRequest_dict)
        
    #return arrays
    return vit_array , med_array , con_array , pre_array
    
    
    
#returns next int or double
def get_next_value(text, pos):
    for x in range(pos, len(text)):
        try:
            value = float(text[x])
            return value
        except:
            pass

#returns a spezified number of following strings
def get_next_string(text, pos, length):
    value = []
    for x in range(pos, pos + length):
        try:
            value.append(text[x + 1])
        except:
            pass
    return value

#concerts array to string and returns it
def get_string(text):
    value = ""
    for x in text:
        value = value + " " + x
    return value
    
#compares an array of text and an array of keywords and returns the closest and first position in array
def find_position(text, arr):
    value = -1
    bd = 3
    for s in arr:
        for i in range(len(text)):
            d = nltk.edit_distance(text[i], s)
            if d < bd:
                bd = d
                value = i
    return value

#saves vitality values in dict_array
def get_vit_value(text, pos, index):
    vitals_dict['vitType'] = index + 1
    vitals_dict['vitValue'] = get_next_value(text, pos)
    vit_array.append(copy.deepcopy(vitals_dict))

#saves patient name in all arrays
def get_patient_name(text):
    pos = find_position(text, keys_patient)
    val = (get_next_string(text, pos, 2))
    if pos != -1:
        vitals_dict['patientName'] = (val[0] + " " + val[1]).replace('.', '')
        medication_dict['patientName'] = (val[0] + " " + val[1]).replace('.', '')
        patientcondition_dict['pcPatientName'] = (val[0] + " " + val[1]).replace('.', '')

#saves employee name in all arrays
def get_employee_name(text):
    pos = find_position(text, keys_nurse)
    val = (get_next_string(text, pos, 2))
    if pos != -1:
        vitals_dict['employeeName'] = (val[0] + " " + val[1]).replace('.', '')
        medication_dict['employeeName'] = (val[0] + " " + val[1]).replace('.', '')
        patientcondition_dict['pcEmployeeName'] = (val[0] + " " + val[1]).replace('.', '')
