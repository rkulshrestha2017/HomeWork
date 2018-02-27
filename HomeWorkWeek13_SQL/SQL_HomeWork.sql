show databases;

use sakila;

show tables;

SELECT * FROM actor;

/* 1a. show first and last name */
SELECT first_name, last_name from actor;

/* 1b. Show first and last name in one column with only uppercase letters */
SELECT CONCAT(UCASE(first_name), " ", UCASE(last_name)) as "Actor Name"
FROM actor;

/* 	2a. Query to find first name "Joe" and display ID, first name, and last name */
SELECT actor_id, first_name, last_name FROM actor
WHERE first_name = "Joe";

/* 2b. Find actors whose last name contain the letters "GEN" */
SELECT * FROM actor
WHERE last_name LIKE '%gen%';

/* 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order: */
Select * FROM actor
WHERE last_name LIKE '%li%'
ORDER BY last_name, first_name;

/* 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China: */
SELECT * FROM country
WHERE country in ('Afghanistan', 'Bangladesh', 'China');

/* 3a. Add a middle_name column to the table actor. Position it between first_name and last_name. Hint: you will need to specify the data type. */
ALTER TABLE actor
ADD COLUMN middle_name VARCHAR(30) AFTER first_name;

/* 3b. You realize that some of these actors have tremendously long last names. Change the data type of the middle_name column to blobs. */
ALTER TABLE actor MODIFY middle_name BLOB;

/* DESCRIBE actor; */
ALTER TABLE actor DROP middle_name;

/* 4a. List the last names of actors, as well as how many actors have that last name. */
SELECT last_name, COUNT(last_name) AS 'Number of Actors' 
FROM actor
GROUP BY last_name;

/* 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors */
SELECT last_name, COUNT(last_name) AS 'Number of Actors' 
FROM actor
GROUP BY last_name
HAVING COUNT(last_name) > 1;

/* 4c. Change "GROUCHO WILLIAMS" to "HARPO WILLIAMS" */
UPDATE actor
SET first_name = 'HARPO' 
WHERE first_name = "GROUCHO" AND last_name = "WILLIAMS";

/* 4d. conditional change value */
UPDATE actor
SET first_name = 
	CASE 
		WHEN first_name = "HARPO"
			THEN "GROUCHO"
		ELSE "MUCHO GROUCHO"
	END
WHERE actor_id = 172;

/* 5a. You cannot locate the schema of the address table. Which query would you use to re-create it? */
SHOW COLUMNS from sakila.address;

SHOW CREATE TABLE sakila.address;

/* CREATE TABLE `address` (
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
) ENGINE=InnoDB AUTO_INCREMENT=606 DEFAULT CHARSET=utf8 */


/* 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address */
SELECT first_name, last_name, address from staff s
INNER JOIN address a ON s.address_id = a.address_id;

/* 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment. */

SELECT s.staff_id, first_name, last_name, SUM(amount) as "Total Amount Rung Up"
FROM staff s
INNER JOIN payment p 
ON s.staff_id = p.staff_id
GROUP BY s.staff_id;

/* 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join. */

Select f.title, COUNT(fa.actor_id) as "Number of Actors"
FROM film f
LEFT JOIN film_actor fa
ON f.film_id = fa.film_id
GROUP BY f.film_id;

/* 6d. How many copies of the film Hunchback Impossible exist in the inventory system? */
SELECT f.title, COUNT(i.inventory_id) as "Number in Inventory"
FROM film f
INNER JOIN inventory i
ON f.film_id = i.film_id
GROUP BY f.film_id
HAVING title = "Hunchback Impossible";

/* 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name */


SELECT c.last_name, c.first_name, SUM(p.amount) as "Total Paid"
FROM customer c
INNER JOIN payment p
ON c.customer_id = p.customer_id
GROUP BY p.customer_id
ORDER BY last_name, first_name;

/* 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English. */


SELECT title FROM film
WHERE language_id IN
	(SELECT language_id FROM language
	WHERE name = "English")
AND (title LIKE "K%") OR (title LIKE "Q%");

/* 7b. Use subqueries to display all actors who appear in the film Alone Trip. */

SELECT first_name, last_name FROM actor
WHERE actor_id IN
	(SELECT actor_id FROM film_actor
	WHERE film_id IN
		(SELECT film_id FROM film
		WHERE title = "Alone Trip"));

/* 7c. You want to run an email marketing campaign in Canada, for which you 
will need the names and email addresses of all Canadian customers. Use joins to retrieve this information. */

SELECT c.first_name, c.last_name, c.email, co.country FROM customer c
LEFT JOIN address a
ON c.address_id = a.address_id
LEFT JOIN city ci
ON ci.city_id = a.city_id
LEFT JOIN country co
ON co.country_id = ci.country_id
WHERE country = "Canada";

/* 7d. Sales have been lagging among young families, and you wish to target all 
family movies for a promotion. Identify all movies categorized as famiy films. */

SELECT * from film
WHERE film_id IN
	(SELECT film_id FROM film_category
	WHERE category_id IN
		(SELECT category_id FROM category
		WHERE name = "Family"));
		
/* 7e. Display the most frequently rented movies in descending order. */
SELECT f.title , COUNT(r.rental_id) AS "Number of Rentals" FROM film f
RIGHT JOIN inventory i
ON f.film_id = i.film_id
JOIN rental r 
ON r.inventory_id = i.inventory_id
GROUP BY f.title
ORDER BY COUNT(r.rental_id) DESC;

/* 7f. Write a query to display how much business, in dollars, each store brought in. */

SELECT s.store_id, sum(amount) as "Revenue" FROM store s
RIGHT JOIN staff st
ON s.store_id = st.store_id
LEFT JOIN payment p
ON st.staff_id = p.staff_id
GROUP BY s.store_id;

/* 7g. Write a query to display for each store its store ID, city, and country. */
SELECT s.store_id, ci.city, co.country FROM store s
JOIN address a
ON s.address_id = a.address_id
JOIN city ci
ON a.city_id = ci.city_id
JOIN country co
ON ci.country_id = co.country_id;

/* 7h. List the top five genres in gross revenue in descending order. 
(Hint: you may need to use the following tables: 
category, film_category, inventory, payment, and rental.) */

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

/* 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. 
Use the solution from the problem above to create a view. 
If you haven't solved 7h, you can substitute another query to create a view. */

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

/* 8b. How would you display the view that you created in 8a? */
SELECT * FROM top_5_by_genre;

/* 8c. You find that you no longer need the view top_five_genres. Write a query to delete it. */
DROP VIEW top_5_by_genre;