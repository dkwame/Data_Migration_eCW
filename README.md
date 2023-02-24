# Data_Migration
In this project, my client, a physician's office, was migrating data from their current EMR (Electronic Medical Record) system, eClinicalWorks, to a new EMR system, Kareo. 

#Problem
All patient data was received from eClinicalWorks as CCDA data (i.e. written in HTML/CSS and exported using .xml) which could not be cleanly inputted into the new system. After requesting information from both Kareo and eClinicalWorks as well as doing some of my own reading, it seems CCDA data is not standardized and the formatting within this file can change from practice to practice and EMR system to EMR system. 

#Solution 
I am using the Python libraries BeautifulSoup and Pandas to scrape the CCDA files for important patient information and then exporting the data into multiple datasets such as patient_demographics, medical history, problems list, medication, etc... all tables will be linked using the patient chart number. (Prescriptions linked using NDC codes) 
