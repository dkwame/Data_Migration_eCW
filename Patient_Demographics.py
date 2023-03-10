# -*- coding: utf-8 -*-
"""Copy of Data_Migration.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZacCSfXbKuomuee91zp3sKTVGL2cUqIe
"""
from csv import writer
import os
import pandas as pd
import numpy as np
import bs4
from bs4 import BeautifulSoup



def patient_demographics(files):
  with open(files) as doc:
    soup = BeautifulSoup(doc, 'html.parser')
  patient_info = []
  #patient chart number
  patient_info.append(int(soup.clinicaldocument.recordtarget.id['extension']))


  #Names
  #New system wants [First, Last, M] old system was [Last, First, M]
  names = [soup.clinicaldocument.recordtarget.patient.get_text(',')]
  names = [x.split(',') for x in names][0]

  if len(names) == 2:
    patient_info.append(names[1])
    patient_info.append(names[0])
    patient_info.append("")
  elif len(names) > 2:
    patient_info.append(names[1])
    patient_info.append(names[0])
    patient_info.append(names[2])


  #DOB
  patient_info.append(int(soup.clinicaldocument.recordtarget.patient.birthtime['value']))



  #Gender
  try:
    gender_code = soup.clinicaldocument.recordtarget.patient.administrativegendercode['code']
    if gender_code == 'F':
      patient_info.append('F')
    elif gender_code == 'M':
      patient_info.append('M')
    elif gender_code != 'F' and gender_code != 'M':
      patient_info.append('U')
  except Exception:
    patient_info.append('U')


  #SSN (Not collected)
  patient_info.append(0)

  #Address
  #Address 1
  addr = [soup.clinicaldocument.recordtarget.addr.get_text(',')]
  addr = [x.split(',') for x in addr][0]
  #number of items (does not go from (0,4))
  if len(addr) == 5:
  #Address 1
    patient_info.append(addr[1])
    #Address 2 (We have to put something here even if there is nothing)
    patient_info.append("")
    #City
    patient_info.append(addr[0])
    #State
    patient_info.append(addr[2])
    #Zip code
    patient_info.append(int(addr[4][:5]))
  elif len(addr) > 5:
    #Address 1
    patient_info.append(addr[1])
    #Address 2
    patient_info.append(addr[2])
    #City
    patient_info.append(addr[0])
    #State
    patient_info.append(addr[3])
    #Zip code
    try:
      patient_info.append(int(addr[5][:5]))
    except Exception:
      #This accounts for user inputting error...hopefully
      patient_info.append(int(soup.clinicaldocument.recordtarget.addr.postalcode.get_text()[:5]))


  #Contact information
  #Home phone
  home_num = soup.clinicaldocument.recordtarget.findAll(attrs={"use":"HP"})
  if len(home_num) == 1:
    patient_info.append(int(home_num[0]['value'].strip('tel:').replace('-','')))
  elif len(home_num) == 0:
    patient_info.append(int(0000000000))
  #Mobile Cell
  cell_num = soup.clinicaldocument.recordtarget.findAll(attrs={"use":"MC"})
  if len(cell_num) == 1:
    patient_info.append(int(cell_num[0]['value'].strip('tel:').replace('-','')))
  elif len(cell_num) == 0:
    patient_info.append(int(0000000000))
  #Work Phone
  work_num = soup.clinicaldocument.recordtarget.findAll(attrs={"use":"WP"})
  if len(work_num) == 1:
    patient_info.append(int(work_num[0]['value'].strip('tel:').replace('-','')))
  elif len(work_num) == 0:
    patient_info.append(int(0000000000))

  #Email
  if len(home_num + cell_num + work_num) < len(soup.clinicaldocument.recordtarget.findAll("telecom")):
    try:
      patient_info.append(soup.clinicaldocument.recordtarget.findAll("telecom")[-1]['value'].replace('mailto:',''))
    except Exception:
      patient_info.append("No Email")
  elif len(home_num + cell_num + work_num) == len(soup.clinicaldocument.recordtarget.findAll("telecom")):
    patient_info.append("No Email")


  #Employment Status
  #We don't grab this info so it's going to be U for 'Unknown'
  patient_info.append('U')


  #Marital Status (Too hairy, hence the exceptions lol) (We'll figure this out SQL side)
  try:
    patient_info.append(soup.clinicaldocument.recordtarget.maritalstatuscode['code'])
  except Exception:
    patient_info.append('')



  #************************Responsible Party Information**********************
  #Some of this might be repeitive as the responsible party might be the patient



  #Responsible Party Name
  rp_names = [soup.clinicaldocument.participant.associatedperson.get_text(',')]
  rp_names = [x.split(',') for x in rp_names][0]

  if len(rp_names) == 2:
    patient_info.append(rp_names[0])
    patient_info.append(rp_names[1])
    patient_info.append("")
  elif len(rp_names) > 2:
    patient_info.append(rp_names[0])
    patient_info.append(rp_names[1])
    patient_info.append(rp_names[2])


  #Responsible Party Address
  try:
    rp_addr = [soup.clinicaldocument.participant.addr.get_text(',')]
    rp_addr = [x.split(',') for x in rp_addr][0]
  #number of items (does not go from (0,4))
    if len(rp_addr) == 5:
      #Address 1
      patient_info.append(rp_addr[0])
      #Address 2 (We have to put something here even if there is nothing)
      patient_info.append("")
      #City
      patient_info.append(rp_addr[1])
      #State
      patient_info.append(rp_addr[2])
      #Zip code
      patient_info.append(int(soup.clinicaldocument.participant.addr.postalcode.get_text()[:5]))
    elif len(rp_addr) > 5:
      #Address 1
      patient_info.append(rp_addr[0])
      #Address 2
      patient_info.append(rp_addr[1])
      #City
      patient_info.append(rp_addr[2])
      #State
      patient_info.append(rp_addr[3])
      #Zip code
      patient_info.append(int(rp_addr[4][:5]))
  except Exception:
    #I'm sure there's a more efficient way of handling blank information but I've been at the office for 12 hours lol
    patient_info.append('')
    patient_info.append('')
    patient_info.append('')
    patient_info.append('')
    patient_info.append('')

  #Responsible Party Contact information
  #Only one number alotted and no email
  rp_comm = soup.clinicaldocument.participant.findAll("telecom")
  if len(rp_comm) >= 1:
    patient_info.append(int(rp_comm[0]['value'].strip('tel:').replace('-','')))
  elif len(rp_comm) == 0:
    patient_info.append(int(0000000000))

  return patient_info



#Create dataset for patients
pd.DataFrame(patient_info,columns=patient_cols).set_index('patient_chart').to_csv(r"______\patient_tables.csv", sep=',')
patient_cols = ['patient_chart','first_name','last_name','middle_init','dob','gender','ssn','Address_1','Addres_2','City',
        'State','Zip_code','HP','MC' ,'WP','Email','Employment_Status',
        'Marital_status','rp_first_name', 'rp_last_name','rp_middle_init','rp_Address_1','rp_Address_2','rp_City',
        'rp_State','rp_Zip_code','rp_HP']
patient_info=[]


#Send information from files to patient dataframe
for files in os.listdir(r"___________"):
  file_input = r"_______"+files

  with open(r"________", 'a', newline='') as pt_objects:
    writer(pt_objects).writerow(patient_demographics(file_input))
    pt_objects.close()
