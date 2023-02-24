# Data_Migration
In this project, my client, a physician's office, was migrating data from their current EMR (Electronic Medical Record) system, eClinicalWorks, to a new EMR system, Kareo. 

#Problem
All patient data was received from eClinicalWorks as CCDA data (i.e. written in HTML/CSS and exported using .xml) which could not be cleanly inputted into the new system. After requesting information from both Kareo and eClinicalWorks as well as doing some of my own reading, it seems CCDA data is not standardized and the formatting within this file can change from practice to practice and EMR system to EMR system. 

#Solution 
I am using the Python libraries BeautifulSoup and Pandas to scrape the CCDA files for important patient information and then exporting the data into multiple datasets such as patient_demographics, medical history, problems list, medication, etc... all tables will be linked using the patient chart number. (Prescriptions linked using NDC codes). Hopefully, this can be used as tool so someone in the future does not have to struggle with this as I have. 

#Reflection 
There is probably an easier method of extracting information from HTML/CSS formats and exporting en masse into .csv tables, however, because this is my first project working with those formats.  By  the end of this project, I definitely will be proficient in reading and navigating HTML/CSS and not by choice lol! 
