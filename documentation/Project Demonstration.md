**Queries**

```sql
-- List all books given author (Jane Smith)
SELECT *
FROM books As b
JOIN library_material As lm
	ON b.material_id = lm.material_id
WHERE b.author='Jane Smith';

-- Find books by publication year given publication year (2020)
SELECT *
FROM books AS b
JOIN library_material AS lm
    ON b.material_id = lm.material_id
WHERE lm.publication_year = 2020;

-- Check membership status given client id(client_id = 1)
SELECT *
FROM clients
WHERE client_id = 1;

-- Fine calculation
SELECT
    c.client_id,
    c.name,
    SUM(
        GREATEST(
            (COALESCE(bt.return_date, CURRENT_DATE)::date - bt.due_date),
            0
        )
        * mt.late_fee_rate
    ) AS total_fines
FROM borrowing_transactions AS bt
JOIN clients AS c
    ON bt.client_id = c.client_id
JOIN membership_types AS mt
    ON c.membership_type = mt.membership_type
GROUP BY
    c.client_id,
    c.name
ORDER BY
    total_fines DESC;

-- Book availability given a genre (genre = Fiction)
SELECT *
FROM books AS b
JOIN library_material AS lm
ON b.material_id = lm.material_id
WHERE lm.genre = 'Fiction'
AND lm.availability_status = 'Available';

-- Frequent borrowers of a specific genre (genre = Mystery)
WITH genre_counts AS (
    SELECT
        bt.client_id,
        COUNT(*) AS borrow_count
    FROM borrowing_transactions bt
    JOIN library_material lm
        ON bt.material_id = lm.material_id
    WHERE
    -- Input genre below
        lm.genre = 'History'
        AND bt.borrow_date >= CURRENT_DATE - INTERVAL '1 year'
    GROUP BY bt.client_id
),

max_count AS (
    SELECT MAX(borrow_count) AS top_count
    FROM genre_counts
)

SELECT
    c.client_id,
    c.name,
    gc.borrow_count
FROM genre_counts gc
JOIN max_count mc
    ON gc.borrow_count = mc.top_count
JOIN clients c
    ON gc.client_id = c.client_id
ORDER BY c.name;

-- Books due soon (within a week)
SELECT
    bt.transaction_id,
    c.client_id,
    c.name          AS client_name,
    c.contact_info,
    lm.material_id,
    lm.title        AS material_title,
    bt.borrow_date,
    bt.due_date
FROM borrowing_transactions bt
JOIN clients c
    ON bt.client_id = c.client_id
JOIN library_material lm
    ON bt.material_id = lm.material_id
WHERE
    bt.return_date IS NULL
    AND bt.due_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
ORDER BY
    bt.due_date ASC;

-- Members with overdue books
SELECT
    c.client_id,
    c.name AS client_name,
    string_agg(lm.title, ', ' ORDER BY bt.due_date) AS overdue_titles,
    COUNT(*) AS num_overdues
FROM borrowing_transactions bt
JOIN clients c
    ON bt.client_id = c.client_id
JOIN library_material lm
    ON bt.material_id = lm.material_id
WHERE
    bt.return_date IS NULL
    AND bt.due_date < CURRENT_DATE
GROUP BY
    c.client_id,
    c.name
ORDER BY
    c.name;

-- Average borrowing time for specific genre (for Fiction genre)
SELECT
    c.client_id,
    c.name,
    AVG((bt.return_date::date - bt.borrow_date::date)) AS average_borrow_days
FROM borrowing_transactions bt
JOIN library_material lm
    ON bt.material_id = lm.material_id
JOIN clients c
    ON bt.client_id = c.client_id
WHERE
    lm.genre = 'Fiction'
    AND bt.return_date IS NOT NULL
GROUP BY
    c.client_id,
    c.name
ORDER BY
    average_borrow_days DESC;

-- Most popular author in the last month
SELECT
    b.author,
    COUNT(*) AS borrow_count
FROM borrowing_transactions bt
JOIN books b
    ON bt.material_id = b.material_id
WHERE
    bt.borrow_date >= CURRENT_DATE - INTERVAL '1 month'
GROUP BY
    b.author
ORDER BY
    borrow_count DESC
LIMIT 1;
```

**Reports**

```sql
-- Collection analysis report
-- Member engagement report
-- Operational efficiency report
```
