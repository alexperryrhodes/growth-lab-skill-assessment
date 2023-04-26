# Back-End Developer Skills Test

This repo contains my solution to the challenge posed by Harvard's Growth Lab.

This repo has two folders: the problem folder and my solution to the problem. 

The solution folder contains three separate python files, each of which solves one of the assigned tasks:

- task-1.py: Produces a csv file containing aggregated census data
  - To run in terminal:
    1. clone repo
    2. cd solution 
    3. python task-1.py
  - Output file will be created in the same folder as "aggregated_migration.csv"
- task-2.py:
  - To run in terminal: 
    1. clone repo
    2. cd solution
    3. python task-2.py
  - Output file will be created in the same folder as "nc_migration.csv"
- task-3.py:
  - To run in terminal:
    1. clone repo
    2. cd solution
    3. flask --app task-3 run. 
    4. Data can be accessed at localhost with the following endpoints
    - /previous_state/`<id>`/
    - /previous_state/`<id>`/`<year>`/
    - /previous_division/`<id>`/
    - /previous_division/`<id>`/`<year>`/

In addition, the solution folder contains a helper function file which is required to support all three task files. 
