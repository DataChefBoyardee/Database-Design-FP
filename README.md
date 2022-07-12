# Database-Design-FP

This is basically just a knock-off version of Steam, 
however the data that can be used with it is ripped 
straight from Steam thanks to SteamSpy and the fantastic
API and libraries created by Sergey Galyonkin. This project
was made possible by the folks who created psycopg2 which 
allows our code to interact with databases directly. Big
thanks to them, and if you're interested in making anything
that uses PostgreSQL in Python, check them out! The GUI was
created using PyQt5, which is built off of the Qt framework.
Big thanks to the developers at Qt for making their GUI tools
open source! Now, on to the program.

This program requires PostgreSQL, and pgAdmin to create
the initial database. You can download both here:

https://www.postgresql.org/

In order for psycopg2 to work, only Python version 3.9 and earlier can be used, 
until any compatibility issues are finally resolved.

To begin, create a database in pgAdmin called "steam", without the quotes.
The backup file, "steam.backup", can then be used to restore the schema created,
along with any views and triggers contained within the actual database.

In the pgAdmin menu, right-click the newly created database, and click restore.
Choose "steam.backup" as the restore file.

To populate the database, run the script "top100in2weeks_insert.py". As the name
implies, the database will be populated with the top 100 games on Steam in the 
last 2 weeks.

To start the program, run the script "main.py" with the other files contained in
the folder "GUI".

And that's it! Feel free to leave feedback, and thank you for taking an interest!


  
