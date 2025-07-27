# CONFIGURE sqlite3
# STEP 1 DONWLOAD sqlite3 (https://www.sqlite.org/download.html)
Precompiled Binaries for Windows FILE THAT INCLUDING THIS
(1) THE command-line shell, 
(2) sqldiff.exe,
(3) sqlite3_analyzer.exe, and 
(4) sqlite3_rsync.exe. 64-bit

# STEP 2 EXTRACT AND COPY THE THE FILE TO WINDOWS OS AS ROOT FILE AND REMAME THE FOLDER sqlite3( C:\sqlite3)

# STEP 3 COPY THE PATH AND ADD THIS TO ENVIRONMENT FILE PATHE 
# FROM THE SYSTEM VARIABLES FIND PATH AND EDIT -> THEN NEW 
# PASTE THE FILE PAHT OF THE sqlite3 , C:\sqlite3
# STEP 4 DONE THE  C:\sqlite3 MUST WORK AND YOU CAN TRY OPEN CMD THEN TYPE  sqlite3


<!--  -->
# TO SWITCH TODOS DATABASE
sqlite3 .\todos.db
sqlite3 .\todosApp.db
# TO SHOW ALL SCHEMA
.schema


# INSERT QUERY
<!--
 INSERT INTO todos (title, description, priority, completed) VALUES ('Buy groceries', 'Milk, Eggs, Bread', 2, FALSE);
INSERT INTO todos (title, description, priority, completed) VALUES ('Walk the dog', 'Take the dog for a walk in the park', 1, FALSE);
INSERT INTO todos (title, description, priority, completed) VALUES ('Finish project report', 'Complete the final report for the project', 3, FALSE);
INSERT INTO todos (title, description, priority, completed) VALUES ('Attend meeting', 'Weekly team meeting at 10 AM', 1, FALSE);
INSERT INTO todos (title, description, priority, completed) VALUES ('Read a book', 'Finish reading "The Great Gatsby"', 2, TRUE);
INSERT INTO todos (title, description, priority, completed) VALUES ('Exercise', 'Go for a run or hit the gym', 2, FALSE);
INSERT INTO todos (title, description, priority, completed) VALUES ('Call mom', 'Check in with mom', 1, FALSE);
INSERT INTO todos (title, description, priority, completed) VALUES ('Plan vacation', 'Research destinations for summer vacation', 3, FALSE);
INSERT INTO todos (title, description, priority, completed) VALUES ('Clean the house', 'Dust and vacuum all rooms', 2, FALSE);
INSERT INTO todos (title, description, priority, completed) VALUES ('Grocery shopping', 'Buy fruits and vegetables', 2, FALSE);

 -->
# TO SEE TABLE VIEW MODE
.mode column
or 
.mode markdown

or 
.mode box

or
.mode table


 # SELECT QUERY
 SELECT * FROM todos;
 SELECT * FROM todos WHERE id = 3;

 # UPDATE QUERY BY ID 
 UPDATE todos SET completed = TRUE WHERE id = 1;

 # DELETE QUERY BY ID

 DELETE FROM todos  where id = 3;