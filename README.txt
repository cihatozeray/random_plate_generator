#random_plate_generator
Generates random vehicle license plates in accordance with Turkish regulations
Takes arguments [test_time], [test_letters], [test_numbers] (all optional) to test cleaning efficiency 
or execution time

-------

Generating random vehicle license plates are probably a common practice among programming courses

-------

In this example I researched constraints for license plates and I came across www.gib.gov.tr/plaka-harf-grubu 
(Turkish Republic Tax Administration website) which publishes those constraints for different
provinces of Turkey

-------

urllib module has been used for web scraping, and mainly Pandas is used for data cleansing

-------

At first try it takes around 22 seconds to execute (also depends on the connection) since it connects
to web, then each plate takes around 0.0 seconds