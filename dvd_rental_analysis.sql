SELECT 	
	f.film_id, 
	f.title AS film_title, 
	c.name AS category,
	SUM(p.amount) AS total_rental_revenue,
	COUNT(DISTINCT r.rental_id) AS total_rentals,
	SUM(p.amount)/ COUNT(DISTINCT r.rental_id) AS avg_revenue_per_rental,
	MAX(r.rental_date) AS last_rental_date
FROM film f 
LEFT JOIN film_category fc
ON f.film_id = fc.film_id
LEFT JOIN category c 
ON fc.category_id = c.category_id
LEFT JOIN inventory i 
ON f.film_id = i.film_id
LEFT JOIN rental r 
ON i.inventory_id = r.inventory_id
LEFT JOIN payment p 
ON r.rental_id = p.rental_id
GROUP BY f.film_id, f.title, c.name
ORDER BY total_rental_revenue DESC;


-- CUSTOMER BEHAVIOUR & RETENTION 
SELECT 
	cu.customer_id,
	CONCAT(cu.first_name, ' ', cu.last_name) AS full_name,
	co.country,
	ci.city,
	SUM(p.amount) AS total_amount_spent,
	COUNT(DISTINCT r.rental_id) AS total_rentals,
	MIN(r.rental_date) AS first_rental_date,
	MAX(r.rental_date) AS most_recent_rental_date,
	COUNT(DISTINCT DATE_TRUNC('month', r.rental_date) ) AS rental_month
FROM customer cu 
JOIN address a
ON cu.address_id = a.address_id
JOIN city ci
ON a.city_id = ci.city_id
JOIN country co 
ON ci.country_id = co.country_id
JOIN rental r
ON cu.customer_id = r.customer_id
JOIN payment p
ON r.rental_id = p.rental_id
GROUP BY 
	cu.customer_id,
	cu.first_name, 
	cu.last_name,
	co.country,
	ci.city
ORDER BY total_amount_spent DESC;

--TIME BASED BUSINESS TRENDS

SELECT 
	EXTRACT(YEAR FROM r.rental_date) AS year,
	EXTRACT(MONTH FROM r.rental_date) AS month,
	COUNT(DISTINCT r.rental_id) AS total_rentals,
	COUNT(DISTINCT r.customer_id) AS unique_customers,
	SUM(p.amount)/ COUNT(DISTINCT r.rental_id) AS avg_revenue_per_rental
FROM rental r
JOIN payment p 
ON r.rental_id = p.rental_id
GROUP BY 
	EXTRACT(YEAR FROM r.rental_date),
	EXTRACT(MONTH FROM r.rental_date)
ORDER BY year, month DESC;


-- STORE AND STAFF PERFORMANCE
SELECT 
	s.store_id,
	CONCAT(st.first_name, ' ', st.last_name) AS staff_name,
	COUNT(DISTINCT r.rental_id) AS total_rental_processed,
	SUM(p.amount) AS total_revenue_collected,
	COUNT(DISTINCT r.customer_id) AS unique_customer_served,
	ROUND(COUNT(DISTINCT r.rental_id)::numeric
	/ NULLIF(COUNT(DISTINCT DATE(r.rental_date)), 0), 2) AS avg_rentals_per_day
FROM staff st
JOIN store s 
ON st.store_id = s.store_id
JOIN rental r 
ON st.staff_id = r.staff_id
JOIN payment p
ON r.rental_id = p.rental_id
GROUP BY 
	s.store_id,
	st.staff_id,
	st.first_name,
	st.last_name
ORDER BY s.store_id, total_revenue_collected;

--GEOGRAPHIC AND MARKET ANALYSis
SELECT
	co.country, 
	ci.city,
	COUNT(DISTINCT r.rental_id) AS total_rentals,
	SUM(p.amount) as total_revenue,
	COUNT(DISTINCT cu.customer_id) AS unique_customers,
	(
	SELECT c.name 
	FROM category c
	JOIN film_category fc
	ON c.category_id = fc.category_id
	JOIN inventory i2
	ON fc.film_id = i2.film_id
	JOIN rental r2
	ON i2.inventory_id = r2.inventory_id
	JOIN customer cu2
	ON r2.customer_id = cu2.customer_id
	JOIN address a2
	ON cu2.address_id = a2.address_id
	JOIN city ci2 
	ON a2.city_id = ci2.city_id
	WHERE ci2.city_id = ci.city_id
	GROUP BY c.category_id,c.name
	ORDER BY COUNT(DISTINCT r2.rental_id) DESC
	LIMIT 1
	) AS most_popular_film_category
FROM customer cu
JOIN address a 
	ON cu.address_id = a.address_id
JOIN city ci
	ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id
JOIN rental r 
ON cu.customer_id = r.customer_id
JOIN payment p
ON r.rental_id = p.rental_id
GROUP BY 
	co.country,
	ci.city,
	ci.city_id
ORDER BY total_revenue DESC;

--INVENTORY & OPERATION
SELECT 
	f.film_id,
	f.title AS film_title,
	c.name AS category,
	COUNT(DISTINCT i.inventory_id) AS inventory_count,
	COUNT(DISTINCT r.rental_id) AS total_rentals,
	SUM(p.amount) AS total_revenue,
	MAX(r.rental_date) AS last_rental_date,
	AVG(EXTRACT(
			DAY FROM (r.return_date - r.rental_date)
			)) AS avg_rental_duration
FROM film f
JOIN film_category fc
ON f.film_id = fc.film_id
JOIN category c
ON fc.category_id = c.category_id
JOIN inventory i
ON f.film_id = i.film_id
JOIN rental r
ON i.inventory_id = r.inventory_id
JOIN payment p
ON r.rental_id = p.rental_id
GROUP BY 
	f.film_id,
	f.title,
	c.name
ORDER BY total_rentals DESC;
