
# SQL Homework


```python
from sqlalchemy import create_engine
import pandas as pd
from warnings import filterwarnings
import pymysql
filterwarnings('ignore', category=pymysql.Warning)
import os
engine = create_engine('mysql+pymysql://root:kcmo1728@localhost/sakila') 
```

1a. Display the first and last names of all actors from the table actor.


```python
actor = pd.read_sql_query('select first_name, last_name from actor', engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>PENELOPE</td>
      <td>GUINESS</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NICK</td>
      <td>WAHLBERG</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ED</td>
      <td>CHASE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>JENNIFER</td>
      <td>DAVIS</td>
    </tr>
    <tr>
      <th>4</th>
      <td>JOHNNY</td>
      <td>LOLLOBRIGIDA</td>
    </tr>
  </tbody>
</table>
</div>



1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.


```python
actor = pd.read_sql_query('select concat(ucase(first_name)," ", ucase(last_name)) as "Actor Name" from actor', engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Actor Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>PENELOPE GUINESS</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NICK WAHLBERG</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ED CHASE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>JENNIFER DAVIS</td>
    </tr>
    <tr>
      <th>4</th>
      <td>JOHNNY LOLLOBRIGIDA</td>
    </tr>
  </tbody>
</table>
</div>



2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?


```python
actor = pd.read_sql_query('select actor_id, first_name, last_name from actor where first_name="Joe"', engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>9</td>
      <td>JOE</td>
      <td>SWANK</td>
    </tr>
  </tbody>
</table>
</div>



2b. Find all actors whose last name contain the letters GEN:


```python
actor = pd.read_sql_query('select * from actor where last_name like "%%GEN%%"', engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>14</td>
      <td>VIVIEN</td>
      <td>BERGEN</td>
      <td>2006-02-15 04:34:33</td>
    </tr>
    <tr>
      <th>1</th>
      <td>41</td>
      <td>JODIE</td>
      <td>DEGENERES</td>
      <td>2006-02-15 04:34:33</td>
    </tr>
    <tr>
      <th>2</th>
      <td>107</td>
      <td>GINA</td>
      <td>DEGENERES</td>
      <td>2006-02-15 04:34:33</td>
    </tr>
    <tr>
      <th>3</th>
      <td>166</td>
      <td>NICK</td>
      <td>DEGENERES</td>
      <td>2006-02-15 04:34:33</td>
    </tr>
  </tbody>
</table>
</div>



2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:


```python
actor = pd.read_sql_query('select last_name, first_name from actor \
                           where last_name like "%%LI%%" \
                           order by last_name, first_name', engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>last_name</th>
      <th>first_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CHAPLIN</td>
      <td>GREG</td>
    </tr>
    <tr>
      <th>1</th>
      <td>JOLIE</td>
      <td>WOODY</td>
    </tr>
    <tr>
      <th>2</th>
      <td>OLIVIER</td>
      <td>AUDREY</td>
    </tr>
    <tr>
      <th>3</th>
      <td>OLIVIER</td>
      <td>CUBA</td>
    </tr>
    <tr>
      <th>4</th>
      <td>WILLIAMS</td>
      <td>GROUCHO</td>
    </tr>
  </tbody>
</table>
</div>



2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:


```python
actor = pd.read_sql_query('select * from country where country in ("Afghanistan", "Bangladesh", "China")', engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>country_id</th>
      <th>country</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Afghanistan</td>
      <td>2006-02-15 04:44:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>12</td>
      <td>Bangladesh</td>
      <td>2006-02-15 04:44:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>23</td>
      <td>China</td>
      <td>2006-02-15 04:44:00</td>
    </tr>
  </tbody>
</table>
</div>



3a. Add a middle_name column to the table actor. Position it between first_name and last_name. Hint: you will need to specify the data type.


```python
def RunSQL(sql_command):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='kcmo1728',
                             db='sakila',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            commands = sql_command.split(';')
            for command in commands:
                if command == '\n': continue
                cursor.execute(command + ';')
                connection.commit()
    except Exception as e: 
        print(e)
    finally:
        connection.close()
```


```python
sql_query = """
 alter table actor
 add column middle_name varchar(30) after first_name;
"""
RunSQL(sql_query)
```

3b. You realize that some of these actors have tremendously long last names. Change the data type of the middle_name column to blobs.


```python
sql_query = """
 alter table actor
 modify middle_name blob;
"""
RunSQL(sql_query)
```

3c. Now delete the middle_name column.


```python
sql_query = """
 alter table actor
 drop middle_name;
"""
RunSQL(sql_query)
```

4a. List the last names of actors, as well as how many actors have that last name.


```python
sql_query = """
select last_name, count(last_name) AS 'Number of Actors' 
from actor
group BY last_name;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>last_name</th>
      <th>Number of Actors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AKROYD</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ALLEN</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ASTAIRE</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BACALL</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BAILEY</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors


```python
sql_query = """
select last_name, count(last_name) AS 'Number of Actors' 
from actor
group by last_name
having count(last_name) > 1;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>last_name</th>
      <th>Number of Actors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AKROYD</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ALLEN</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BAILEY</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BENING</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BERRY</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



4c. Oh, no! The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS, the name of Harpo's second cousin's husband's yoga teacher. Write a query to fix the record.


```python
sql_query = """
update actor 
set first_name = 'HARPO'
where first_name like '%GROUCHO%' and last_name = 'WILLIAMS';
"""
RunSQL(sql_query)
```


```python
sql_query = """
Select * 
From actor
where first_name = 'HARPO' and last_name = 'WILLIAMS';
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>172</td>
      <td>HARPO</td>
      <td>WILLIAMS</td>
      <td>2018-02-27 06:03:15</td>
    </tr>
  </tbody>
</table>
</div>



4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO. Otherwise, change the first name to MUCHO GROUCHO, as that is exactly what the actor will be with the grievous error. BE CAREFUL NOT TO CHANGE THE FIRST NAME OF EVERY ACTOR TO MUCHO GROUCHO, HOWEVER! (Hint: update the record using a unique identifier.)


```python
sql_query = """
update actor
set first_name = 
    case 
        when first_name = "HARPO"
            then "GROUCHO"
        else "MUCHO GROUCHO"
    end
where actor_id = 172;
"""
RunSQL(sql_query)
```


```python
sql_query = """
select * from actor
where actor_id = 172;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>actor_id</th>
      <th>first_name</th>
      <th>last_name</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>172</td>
      <td>GROUCHO</td>
      <td>WILLIAMS</td>
      <td>2018-02-27 06:03:52</td>
    </tr>
  </tbody>
</table>
</div>



5a. You cannot locate the schema of the address table. Which query would you use to re-create it? 


Hint: https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html


```python
sql_query = """
SHOW COLUMNS from sakila.address;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Field</th>
      <th>Type</th>
      <th>Null</th>
      <th>Key</th>
      <th>Default</th>
      <th>Extra</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>address_id</td>
      <td>smallint(5) unsigned</td>
      <td>NO</td>
      <td>PRI</td>
      <td>None</td>
      <td>auto_increment</td>
    </tr>
    <tr>
      <th>1</th>
      <td>address</td>
      <td>varchar(50)</td>
      <td>NO</td>
      <td></td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>address2</td>
      <td>varchar(50)</td>
      <td>YES</td>
      <td></td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>district</td>
      <td>varchar(20)</td>
      <td>NO</td>
      <td></td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>city_id</td>
      <td>smallint(5) unsigned</td>
      <td>NO</td>
      <td>MUL</td>
      <td>None</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
sql_query = """
SHOW COLUMNS from sakila.address;


SHOW CREATE TABLE sakila.address;

CREATE TABLE `address` (
  `address_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `address` varchar(50) NOT NULL,
  `address2` varchar(50) DEFAULT NULL,
  `district` varchar(20) NOT NULL,
  `city_id` smallint(5) unsigned NOT NULL,
  `postal_code` varchar(10) DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `location` geometry NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`address_id`),
  KEY `idx_fk_city_id` (`city_id`),
  SPATIAL KEY `idx_location` (`location`),
  CONSTRAINT `fk_address_city` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=606 DEFAULT CHARSET=utf8 

"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```

6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:


```python
sql_query = """
SELECT first_name, last_name, address from staff s
INNER JOIN address a ON s.address_id = a.address_id;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>address</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Mike</td>
      <td>Hillyer</td>
      <td>23 Workhaven Lane</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Jon</td>
      <td>Stephens</td>
      <td>1411 Lillydale Drive</td>
    </tr>
  </tbody>
</table>
</div>



6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.


```python
sql_query = """
SELECT s.staff_id, first_name, last_name, SUM(amount) as "Total Amount Rung Up"
FROM staff s
INNER JOIN payment p 
ON s.staff_id = p.staff_id
GROUP BY s.staff_id;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>staff_id</th>
      <th>first_name</th>
      <th>last_name</th>
      <th>Total Amount Rung Up</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Mike</td>
      <td>Hillyer</td>
      <td>33489.47</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Jon</td>
      <td>Stephens</td>
      <td>33927.04</td>
    </tr>
  </tbody>
</table>
</div>



6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.


```python
sql_query = """
Select f.title, COUNT(fa.actor_id) as "Number of Actors"
FROM film f
LEFT JOIN film_actor fa
ON f.film_id = fa.film_id
GROUP BY f.film_id;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>Number of Actors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ACADEMY DINOSAUR</td>
      <td>10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ACE GOLDFINGER</td>
      <td>4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ADAPTATION HOLES</td>
      <td>5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AFFAIR PREJUDICE</td>
      <td>5</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AFRICAN EGG</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>



6d. How many copies of the film Hunchback Impossible exist in the inventory system?


```python
sql_query = """
SELECT f.title, COUNT(i.inventory_id) as "Number in Inventory"
FROM film f
INNER JOIN inventory i
ON f.film_id = i.film_id
GROUP BY f.film_id
HAVING title = "Hunchback Impossible";
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>Number in Inventory</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HUNCHBACK IMPOSSIBLE</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:


```python
sql_query = """
SELECT c.last_name, c.first_name, SUM(p.amount) as "Total Paid"
FROM customer c
INNER JOIN payment p
ON c.customer_id = p.customer_id
GROUP BY p.customer_id
ORDER BY last_name, first_name;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>last_name</th>
      <th>first_name</th>
      <th>Total Paid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ABNEY</td>
      <td>RAFAEL</td>
      <td>97.79</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ADAM</td>
      <td>NATHANIEL</td>
      <td>133.72</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ADAMS</td>
      <td>KATHLEEN</td>
      <td>92.73</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ALEXANDER</td>
      <td>DIANA</td>
      <td>105.73</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ALLARD</td>
      <td>GORDON</td>
      <td>160.68</td>
    </tr>
  </tbody>
</table>
</div>



7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.


```python
sql_query = """
SELECT title FROM film
WHERE language_id IN
    (SELECT language_id FROM language
    WHERE name = "English") 
    AND (title LIKE "K%%") OR (title LIKE "Q%%");
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>KANE EXORCIST</td>
    </tr>
    <tr>
      <th>1</th>
      <td>KARATE MOON</td>
    </tr>
    <tr>
      <th>2</th>
      <td>KENTUCKIAN GIANT</td>
    </tr>
    <tr>
      <th>3</th>
      <td>KICK SAVANNAH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>KILL BROTHERHOOD</td>
    </tr>
  </tbody>
</table>
</div>



7b. Use subqueries to display all actors who appear in the film Alone Trip.


```python
sql_query = """
SELECT first_name, last_name FROM actor
WHERE actor_id IN
    (SELECT actor_id FROM film_actor
    WHERE film_id IN
        (SELECT film_id FROM film
        WHERE title = "Alone Trip"));
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ED</td>
      <td>CHASE</td>
    </tr>
    <tr>
      <th>1</th>
      <td>KARL</td>
      <td>BERRY</td>
    </tr>
    <tr>
      <th>2</th>
      <td>UMA</td>
      <td>WOOD</td>
    </tr>
    <tr>
      <th>3</th>
      <td>WOODY</td>
      <td>JOLIE</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SPENCER</td>
      <td>DEPP</td>
    </tr>
  </tbody>
</table>
</div>



7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.


```python
sql_query = """
SELECT c.first_name, c.last_name, c.email, co.country FROM customer c
LEFT JOIN address a
ON c.address_id = a.address_id
LEFT JOIN city ci
ON ci.city_id = a.city_id
LEFT JOIN country co
ON co.country_id = ci.country_id
WHERE country = "Canada";
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
      <th>email</th>
      <th>country</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>DERRICK</td>
      <td>BOURQUE</td>
      <td>DERRICK.BOURQUE@sakilacustomer.org</td>
      <td>Canada</td>
    </tr>
    <tr>
      <th>1</th>
      <td>DARRELL</td>
      <td>POWER</td>
      <td>DARRELL.POWER@sakilacustomer.org</td>
      <td>Canada</td>
    </tr>
    <tr>
      <th>2</th>
      <td>LORETTA</td>
      <td>CARPENTER</td>
      <td>LORETTA.CARPENTER@sakilacustomer.org</td>
      <td>Canada</td>
    </tr>
    <tr>
      <th>3</th>
      <td>CURTIS</td>
      <td>IRBY</td>
      <td>CURTIS.IRBY@sakilacustomer.org</td>
      <td>Canada</td>
    </tr>
    <tr>
      <th>4</th>
      <td>TROY</td>
      <td>QUIGLEY</td>
      <td>TROY.QUIGLEY@sakilacustomer.org</td>
      <td>Canada</td>
    </tr>
  </tbody>
</table>
</div>



7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as famiy films.


```python
sql_query = """
SELECT * from film
WHERE film_id IN
    (SELECT film_id FROM film_category
    WHERE category_id IN
        (SELECT category_id FROM category
        WHERE name = "Family"));
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>film_id</th>
      <th>title</th>
      <th>description</th>
      <th>release_year</th>
      <th>language_id</th>
      <th>original_language_id</th>
      <th>rental_duration</th>
      <th>rental_rate</th>
      <th>length</th>
      <th>replacement_cost</th>
      <th>rating</th>
      <th>special_features</th>
      <th>last_update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5</td>
      <td>AFRICAN EGG</td>
      <td>A Fast-Paced Documentary of a Pastry Chef And ...</td>
      <td>2006</td>
      <td>1</td>
      <td>None</td>
      <td>6</td>
      <td>2.99</td>
      <td>130</td>
      <td>22.99</td>
      <td>G</td>
      <td>Deleted Scenes</td>
      <td>2006-02-15 05:03:42</td>
    </tr>
    <tr>
      <th>1</th>
      <td>31</td>
      <td>APACHE DIVINE</td>
      <td>A Awe-Inspiring Reflection of a Pastry Chef An...</td>
      <td>2006</td>
      <td>1</td>
      <td>None</td>
      <td>5</td>
      <td>4.99</td>
      <td>92</td>
      <td>16.99</td>
      <td>NC-17</td>
      <td>Commentaries,Deleted Scenes,Behind the Scenes</td>
      <td>2006-02-15 05:03:42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>43</td>
      <td>ATLANTIS CAUSE</td>
      <td>A Thrilling Yarn of a Feminist And a Hunter wh...</td>
      <td>2006</td>
      <td>1</td>
      <td>None</td>
      <td>6</td>
      <td>2.99</td>
      <td>170</td>
      <td>15.99</td>
      <td>G</td>
      <td>Behind the Scenes</td>
      <td>2006-02-15 05:03:42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>50</td>
      <td>BAKED CLEOPATRA</td>
      <td>A Stunning Drama of a Forensic Psychologist An...</td>
      <td>2006</td>
      <td>1</td>
      <td>None</td>
      <td>3</td>
      <td>2.99</td>
      <td>182</td>
      <td>20.99</td>
      <td>G</td>
      <td>Commentaries,Behind the Scenes</td>
      <td>2006-02-15 05:03:42</td>
    </tr>
    <tr>
      <th>4</th>
      <td>53</td>
      <td>BANG KWAI</td>
      <td>A Epic Drama of a Madman And a Cat who must Fa...</td>
      <td>2006</td>
      <td>1</td>
      <td>None</td>
      <td>5</td>
      <td>2.99</td>
      <td>87</td>
      <td>25.99</td>
      <td>NC-17</td>
      <td>Commentaries,Deleted Scenes,Behind the Scenes</td>
      <td>2006-02-15 05:03:42</td>
    </tr>
  </tbody>
</table>
</div>



7e. Display the most frequently rented movies in descending order.


```python
sql_query = """
SELECT f.title , COUNT(r.rental_id) AS "Number of Rentals" FROM film f
RIGHT JOIN inventory i
ON f.film_id = i.film_id
JOIN rental r 
ON r.inventory_id = i.inventory_id
GROUP BY f.title
ORDER BY COUNT(r.rental_id) DESC;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>Number of Rentals</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BUCKET BROTHERHOOD</td>
      <td>34</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ROCKETEER MOTHER</td>
      <td>33</td>
    </tr>
    <tr>
      <th>2</th>
      <td>RIDGEMONT SUBMARINE</td>
      <td>32</td>
    </tr>
    <tr>
      <th>3</th>
      <td>JUGGLER HARDLY</td>
      <td>32</td>
    </tr>
    <tr>
      <th>4</th>
      <td>GRIT CLOCKWORK</td>
      <td>32</td>
    </tr>
  </tbody>
</table>
</div>



7f. Write a query to display how much business, in dollars, each store brought in.


```python
sql_query = """
SELECT s.store_id, sum(amount) as "Revenue" FROM store s
RIGHT JOIN staff st
ON s.store_id = st.store_id
LEFT JOIN payment p
ON st.staff_id = p.staff_id
GROUP BY s.store_id;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>store_id</th>
      <th>Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>33489.47</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>33927.04</td>
    </tr>
  </tbody>
</table>
</div>



7g. Write a query to display for each store its store ID, city, and country.


```python
sql_query = """
SELECT s.store_id, ci.city, co.country FROM store s
JOIN address a
ON s.address_id = a.address_id
JOIN city ci
ON a.city_id = ci.city_id
JOIN country co
ON ci.country_id = co.country_id;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>store_id</th>
      <th>city</th>
      <th>country</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Lethbridge</td>
      <td>Canada</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Woodridge</td>
      <td>Australia</td>
    </tr>
  </tbody>
</table>
</div>



7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)


```python
sql_query = """
SELECT c.name, sum(p.amount) as "Revenue per Category" FROM category c
JOIN film_category fc
ON c.category_id = fc.category_id
JOIN inventory i
ON fc.film_id = i.film_id
JOIN rental r
ON r.inventory_id = i.inventory_id
JOIN payment p
ON p.rental_id = r.rental_id
GROUP BY name;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>Revenue per Category</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Action</td>
      <td>4375.85</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Animation</td>
      <td>4656.30</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Children</td>
      <td>3655.55</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Classics</td>
      <td>3639.59</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Comedy</td>
      <td>4383.58</td>
    </tr>
  </tbody>
</table>
</div>



8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.


```python
sql_query = """
CREATE VIEW top_5_by_genre AS
SELECT c.name, sum(p.amount) as "Revenue per Category" FROM category c
JOIN film_category fc
ON c.category_id = fc.category_id
JOIN inventory i
ON fc.film_id = i.film_id
JOIN rental r
ON r.inventory_id = i.inventory_id
JOIN payment p
ON p.rental_id = r.rental_id
GROUP BY name
ORDER BY SUM(p.amount) DESC
LIMIT 5;
"""
RunSQL(sql_query)
```

8b. How would you display the view that you created in 8a?


```python
sql_query = """
SELECT * FROM top_5_by_genre;
"""
RunSQL(sql_query)
actor = pd.read_sql_query(sql_query, engine)
actor.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>Revenue per Category</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Sports</td>
      <td>5314.21</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Sci-Fi</td>
      <td>4756.98</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Animation</td>
      <td>4656.30</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Drama</td>
      <td>4587.39</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Comedy</td>
      <td>4383.58</td>
    </tr>
  </tbody>
</table>
</div>



8c. You find that you no longer need the view top_five_genres. Write a query to delete it.


```python
sql_query = """
DROP VIEW top_5_by_genre;
"""
RunSQL(sql_query)
```
