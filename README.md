
**MPG Calculation Logic**<br>
MPG is calculated using the formula:<br>
MPG=Distance Traveled (in miles)Fuel Used (in gallons)MPG = \frac{\text{Distance Traveled (in miles)}}{\text{Fuel Used (in gallons)}}MPG=Fuel Used (in gallons)<br>Distance Traveled (in miles)​<br>
To determine the distance traveled, the bot calculates <br>the difference between odometer readings from two <br>consecutive fuel entries.

**Interaction Structure with the Bot**<br>
*Main Menu:*<br>
Add Fuel Entry.<br>
View MPG Calculations.<br>
Export Data.<br>
Help.<br>

*Add Fuel Entry:*<br>
The user provides:<br>
Fueling Date.<br>
Fuel Volume (in gallons).<br>
Odometer Reading (in miles).<br>
Fueling Location (optional).<br>
The bot saves the data in a database (Postrgesql).

**MPG Calculation:**<br>
The bot retrieves the last two odometer entries.<br>
Divides the distance by the fuel volume <br>.
Displays the MPG result to the user.<br>

**View Calculations:**<br>
The bot provides a list of all MPG calculations with <br>dates, odometer readings, and locations.<br>
Users can request data for a specific time period.<br>

**Export Data:**<br>
Generates a report (CSV/Excel) containing fuel entries <br>and MPG calculations.<br>
Sends the file to the user.<br>

**Help:**<br>
Explains how MPG calculation works.<br>
Answers frequently asked questions.<br>

*Example Interaction*<br>
User: Press the button 'Add Fuel Entry'.<br>
Bot: Enter the fuel volume (in gallons).<br>
User: 120.<br>
Bot: Enter the current odometer reading (in miles).<br>
User: 3200.<br>
Bot: Enter the fueling date (DD.MM.YYYY).<br>
User: 12.01.2025.<br>
Bot: Enter the location (optional).<br>
User: Truck Stop 24, TX.<br>
Bot: Fuel entry saved!<br>
User: Calculate MPG.<br>


***How to Run a Project via Docker***<br>
Clone the project repository

```
git clone https://github.com/saikal12/mpg.git
```
Build and run containers

```
docker-compose up --build
```
Check the service is running
After the containers are running, check the status with the command:
```
docker-compose ps
```
