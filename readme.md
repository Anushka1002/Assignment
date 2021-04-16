# COVID Bed Management

COVID hospital bed management system. 

## Assumptions
```
1. Indexes mentioned in assignment are bed numbers, 
which are starting from 0. 

2. Currently hospital has 12 beds in total.

3. Beds with bed number - 6, 8 and 10 are not functional.
```

## Installation
Unzip the project
```

## Install Requirements
pip install -r requirements

## Upload Fixture
python manage.py loaddata fixtures/beds.json
```

## To Run the Project
```
python manage.py runserver
```

## Note
```
To create beds as per following criterion, we can use algo defined in assignments.py 
shared earlier.

    1. general(50%) 	        index (all even number values) 
    
    2. semi-private(25%) 	index (starting from first odd vlues, e
                                very alt odd value) 
                                
    3. private(25%) 		index (starting from second odd vlues, e
                                very alt odd value) 
```

## Author
[ANUSHKA](verma.anusha10@gmail.com)
