# Problem Statement. 

You  are  tasked  with  the  **computation  of  the  capacity**  of  a simplified model of the National Airspace System (NAS), **between** 

    Source:  Los  Angeles  (LAX)  and  
    Destina-tion:  New  York  City  (JFK)

**on  January  6,  2020,  in  a  24  hour  time  period,  starting  at  12:00AM  and  ending at  11:59  PM.** 

Apart from these two airports, our simplified NAS consists of the following airports (codes) as well 
- Phoenix (PHX), 
- Seattle (SEA),
- Denver (DEN),
- Atlanta (ATL),
- Chicago (ORD),
- Boston (BOS) 
- Washington DC (IAD). 
- San Francisco (SFO), 

Furthermore, you can assume that our simplified NAS consists ofthree airlines: 
- American Airlines (AA), 
- Delta Airlines (DL)
- United Airlines (UA)


# Problem Conststriants 

To compute the capacity of the NAS on that day, you should consider the following 
1. all direct (non-stop) flights between LAX and NYC, 

2. multi-stop flights between the two cities,provided the stops are airports in the list above.  
    - If the stops are not airports mentioned in the list above, you can discard that itinerary. 
    - For instance,you can discard LAX to MIA to NYC, since Miami airport (MIA) is not in our model.   
    - You can include instances like 
        - a non stop flight from LAX to NYC, 
        - a multi-stop flight which could take youfrom LAX to SFO to ATL to NYC.
        - While considering the above two scenarios, please keep in the mind the following: 
            - only consider flights which depart LAX on 01/06/2020 and arrive at NYC on the same day.
            - **For multi-stop flights, the flight departing LAX may not be the same flight which arrives at NYC.**

3. For the computation of capacity of such a system, you must satisfy the following             
    - A passenger can only travel from LAX to NYC on January 6th, 2020.
    - For multi-stop itineraries, a passenger can take any of the 3 airlines to travel between two cities(one itinerary may have all the three airlines).
    - For multi-stop itineraries, the arrival time of a flight at an intermediate stop must be less than the departing time of the next flight from that very same intermediate stop.



