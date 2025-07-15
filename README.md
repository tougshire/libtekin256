# libtekin
An inventory system of Technical Items for the Suffolk Public Library

# Features

The main unit in this system is the Article, which is a unique individual item such as a phone with a phone number assigned to person

There is a Make/Model (or Manufaturer/Model) class, called Mamodel, which include fields for the brand name and model name.  Articles have a foreign key to Mamodel 

Articles have predefined fields and 16 text fields which can be labeled as the admin sees fit.  The labels for these text fields are defined in settings and can be overridden by the Mamodel

This system allows for a unique ID to be defined and mated to another text field, such as serial number or asset number