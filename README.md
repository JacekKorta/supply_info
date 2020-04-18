# supply_info (django)

### Case:

- Create a simple web application to share information about availability, prices and descriptions of products from the distributor’s warehouse. 
- Unregistered users should see only basic (inexact) information about machine’s availability.
Registered users will be able to see full information about availability, prices and descriptions of products from the distributor’s warehouse. 
- Database updates can be done in two ways. First: API and the integrator based on ODBC and Pervasive db from the one user computer. Because only one user can connect to the source db (Pervasive db) the second way is to fill in the web form based on text raport from Symfonia Handel. 

# serial_numbers (django)

### Case:

The manufacturer requires from the distributor a full record of the sold machines. For each request from the manufacturer the distributor is obligated to deliver information about when and to which shop the machine was sold. The machine tracking is based on the machine’s serial number. Each machine has a unique serial number. The serial number won’t duplicate even between different machine models. 
For each delivery to the distributor the manufacturer delivers information about delivered models and serial numbers. The information is delivered by adding delivery information to one (always the same) bulk .csv file.
The distributor’s warehouse has a manual barcode reader to read serial numbers from machine boxes. 

### Solution:

Because it is not possible to install any additional software on warehouse computers, the application is a web application. 
- Registering machines in the distributor’s warehouse is based on the information from the manufacturer. For a maximum simplification of the manual registration process, the data are pasted to a web form and saved in the db. 
- Each shipment to the shop is based on the delivery note document. The distributor’s warehouse chooses the shop's name from the db, fills in the variable part of the delivery note number and uses a barcode reader to fill in the form with the data from the machine boxes. For each machine the registration date, the serial number, the shipment date and the delivery note number are stored. 

# warranty_parts (django)

### Case: 

The company is a wholesaler of household appliances. As a part of its business, the company gives a 3-6 year warranty on its products. Under the warranty independent tech services report a request to the sales department. Once the request is approved, the sales department gives an exchange order to the warehouse. The warehouse exchanges the defective part for the new one and gives the defective part to the sales department, which then blocks the part in the ERP system. Once a month the sales department sends a report on all of the exchanged parts to the manufacturer. Then the manufacturer examines which parts shall be exchanged under the warranty. All of the rejected parts shall be taken from the warehouse (and from the ERP system) with the RW document. The parts accepted by the manufacturer, depending on the producing factory, are exchanged accordingly after: 60-90 days, 90-120 days or 120-150 days. At the manufacturer’s request some parts may be sent back to the factory. 

### Solution:

The concept was to create an app that helps to make the whole process more transparent and the most automated possible.


## Requirements: 
- coverage==5.0.3
- Django==2.2.7
- djangorestframework==3.11.0
- googletrans==2.4.0
- Markdown==3.2.1
- reportlab==3.5.34