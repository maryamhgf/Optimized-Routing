# Optimized-Routing
In this project, optimal routes between sources and destinations in a city district are found. It is a simplified version of applications that find routes and directions such as Google Maps and Waze. Given the map of a district and the source and the destination, it outputs the best route between the source and the destination in the district.
The project experiments were run in district 14 of Tehran, Iran. we defined 21 points on the map as important origins or destinations. The map was downloaded from Google Maps. These important points and other related information including latitude, longitude, neighbor points (those with a possible route to them), and neighbor weights (defined by the delay between two points) are stored in “information.csv” file. Note that we also have considered the one-way streets.
When running the program, you can see all these 21 points and type your planned origin and destination. The best route will be shown with a red line.

For implementation I modeld the problem like a Linear Problem and used linear solver of ortools library.

(The map was downloaded from Google Maps.)


