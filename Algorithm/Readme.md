# Maximum Flow Of Pipeline. 

## Data Transformation Post Scraping. 

- ``load.py`` : Methods to load the clean Dataset. 
- ``transform.py`` : Transform the data according to different parameters such as Time of Flights. Add Aircraft capacity data etc. Also filter values here which will be may be in applicable, Such as flights which are not reaching there before 

- ``capacities.json`` : Comes from the XLS Sheet provided by the TA + Airlines not included in that . 
- ``flow.py`` : Implementation of Edmund Karps's version of Ford Fulkerson's Max Flow Algorithm. 