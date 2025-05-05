### Queries

#### 1. List all books given author (Jane Smith)

**Goal**: Display all books in the library collection written by a particular author

```sql
SELECT *
FROM books As b
JOIN library_material As lm
	ON b.material_id = lm.material_id
WHERE b.author='Jane Smith';
```

**Output**:

```sql
 book_id | material_id |   author   |     isbn      | material_id |       title        | publication_year |  genre  | availability_status | type
---------+-------------+------------+---------------+-------------+--------------------+------------------+---------+---------------------+------
       2 |           2 | Jane Smith | 9789876543210 |           2 | History of Rome    |             2015 | History | Checked Out         | Book
       5 |          13 | Jane Smith | 9781234567890 |          13 | Adventures of Ruby |             2022 | Fiction | Available           | Book
(2 rows)

```

---

#### 2. Find books by publication year given publication year (2020)

**Goal**: Retrieve a list of books published in a specific year

```sql
SELECT *
FROM books AS b
JOIN library_material AS lm
    ON b.material_id = lm.material_id
WHERE lm.publication_year = 2020;
```

**Output**:

```sql
 book_id | material_id |   author    |     isbn      | material_id |       title        | publication_year |   genre    | availability_status | type
---------+-------------+-------------+---------------+-------------+--------------------+------------------+------------+---------------------+------
       1 |           1 | John Doe    | 9780123456789 |           1 | The Great Novel    |             2020 | Fiction    | Available           | Book
       6 |          14 | Test Author | 9781111111111 |          14 | The Art of Testing |             2020 | Technology | Available           | Book
(2 rows)
```

---

#### 3. Check membership status given client id (client_id = 1)

**Goal**: Display the current status and account information for a specific client based on their unique ID

```sql
SELECT *
FROM clients
WHERE client_id = 1;
```

**Output**:

```sql
 client_id |    name     |      contact_info       | membership_type | account_status
-----------+-------------+-------------------------+-----------------+----------------
         1 | Alice Smith | alice.smith@example.com | Regular         | Active
(1 row)
```

---

#### 4. Fine calculation

**Goal**: Calculate the total fines owed by each member, considering overdue books and a daily fine rate

```sql
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
```

**Output**:

```sql
 client_id |      name      | total_fines
-----------+----------------+-------------
         2 | Bob Johnson    |        50.3
         1 | Alice Smith    |        4.00
         5 | Eve Green      |         2.0
         4 | David Brown    |        0.00
         3 | Carol Williams |         0.0
(5 rows)
```

---

#### 5. Book availability given a genre (genre = Fiction)

**Goal**: Display a list of all available books (not currently borrowed) within a specific genre

```sql
SELECT *
FROM books AS b
JOIN library_material AS lm
ON b.material_id = lm.material_id
WHERE lm.genre = 'Fiction'
AND lm.availability_status = 'Available';
```

**Output**:

```sql
 book_id | material_id |   author   |     isbn      | material_id |       title        | publication_year |  genre  | availability_status | type
---------+-------------+------------+---------------+-------------+--------------------+------------------+---------+---------------------+------
       1 |           1 | John Doe   | 9780123456789 |           1 | The Great Novel    |             2020 | Fiction | Available           | Book
       5 |          13 | Jane Smith | 9781234567890 |          13 | Adventures of Ruby |             2022 | Fiction | Available           | Book
(2 rows)


```

---

#### 6. Frequent borrowers of a specific genre (genre = History)

**Goal**: Identify the members who have borrowed the most books in a particular genre in the last year

```sql
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
```

**Output**:

```sql
 client_id |    name     | borrow_count
-----------+-------------+--------------
         2 | Bob Johnson |            2
(1 row)
```

---

#### 7. Books due soon (within a week)

**Goal**: Generate a report of all books due within the next week, sorted by due date.

```sql
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
```

**Output**:

```sql
 transaction_id | client_id |  client_name   |        contact_info        | material_id | material_title  | borrow_date |  due_date
----------------+-----------+----------------+----------------------------+-------------+-----------------+-------------+------------
              9 |         3 | Carol Williams | carol.williams@example.com |           1 | The Great Novel | 2025-05-01  | 2025-05-08
(1 row)
```

---

#### 8. Members with overdue books

**Goal**: List all members who currently have at least one overdue book, along with the titles of the overdue books

```sql
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
```

**Output**:

```sql
 client_id |      name      | total_fines
-----------+----------------+-------------
         2 | Bob Johnson    |        50.3
         1 | Alice Smith    |        4.00
         5 | Eve Green      |         2.0
         4 | David Brown    |        0.00
         3 | Carol Williams |         0.0
(5 rows)
```

---

#### 9. Average borrowing time for specific genre (for Fiction genre)

**Goal**: Calculate the average number of days members borrow books for a specific genre

```sql
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
```

**Output**:

```sql
 client_id |    name     | average_borrow_days
-----------+-------------+---------------------
         2 | Bob Johnson | 15.0000000000000000
         1 | Alice Smith |  9.0000000000000000
(2 rows)
```

---

#### 10. Most popular author in the last month

**Goal**: Determine the author whose books have been borrowed the most in the last month

```sql
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

**Output**:

```sql
  author  | borrow_count
----------+--------------
 John Doe |            4
(1 row)
```

---

### Reports

#### Planning a collection analysis report

##### 1. Distribution of Books by Genre

**Goal:** Understand how your collection is spread across genres.

```sql
SELECT
  lm.genre,
  COUNT(*) AS book_count,
  ROUND( COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1 ) AS pct_of_collection
FROM library_material lm
WHERE lm.type = 'Book'
GROUP BY lm.genre
ORDER BY book_count DESC;
```

**Output**:

```sql
   genre    | book_count | pct_of_collection
------------+------------+-------------------
 Fiction    |          2 |              33.3
 Technology |          2 |              33.3
 History    |          1 |              16.7
 Mystery    |          1 |              16.7
(4 rows)
```

- **`book_count`** shows how many titles you have in each genre.
- **`pct_of_collection`** tells you each genre’s share of the total.

> **Insight:** Look for very small slices (< 5 %)—these may be under-represented genres worth expanding.

---

##### 2. Acquisition Trends Over the Past 5 Years

**Goal:** See if you’ve been steadily adding new titles, or if there are dips/spikes.

```sql
SELECT
  publication_year,
  COUNT(*) AS titles_acquired
FROM library_material
WHERE
  type = 'Book'
  AND publication_year >= EXTRACT(YEAR FROM CURRENT_DATE) - 4
GROUP BY publication_year
ORDER BY publication_year;
```

**Output**:

```sql
 publication_year | titles_acquired
------------------+-----------------
             2021 |               1
             2022 |               1
(2 rows)
```

- Tracks the # of new titles added per year (e.g. 2021–2025).
- A downward trend may suggest a slowdown in acquisitions.

> **Insight:** If you see a drop-off in recent years, consider boosting your purchasing or donation efforts.

---

##### 3. Age of the Collection

**Goal:** Measure how “old” your books are on average, and flag very outdated materials.

###### 3.1 Average Age

```sql
SELECT
  ROUND(
    AVG(
      EXTRACT(YEAR FROM CURRENT_DATE) - lm.publication_year
    )::numeric,
    1
  ) AS avg_book_age_years
FROM library_material lm
WHERE lm.type = 'Book';
```

**Output**:

```sql
 avg_book_age_years
--------------------
                5.7
(1 row)
```

- **`avg_book_age_years`** is the mean difference between today’s year and each book’s publication year.

###### 3.2 Outdated Materials

Define “outdated” as, say, **25+ years old**:

```sql
SELECT
  lm.material_id,
  lm.title,
  lm.publication_year,
  (EXTRACT(YEAR FROM CURRENT_DATE) - lm.publication_year) AS age_years
FROM library_material lm
WHERE
  lm.type = 'Book'
  AND EXTRACT(YEAR FROM CURRENT_DATE) - lm.publication_year >= 25
ORDER BY age_years DESC;
```

**Output**:

```sql
 material_id | title | publication_year | age_years
-------------+-------+------------------+-----------
(0 rows)
```

> **Insight:** Titles more than 25 years old may need review for relevance or preservation.

---

##### 4. Low-Circulation & “Zero-Borrow” Titles

**Goal:** Spot books that rarely (or never) leave the shelf.

###### 4.1 Completely Unborrowed

```sql
SELECT
  lm.material_id,
  lm.title,
  lm.genre,
  lm.publication_year
FROM library_material lm
WHERE
  lm.type = 'Book'
  AND NOT EXISTS (
    SELECT 1
    FROM borrowing_transactions bt
    WHERE bt.material_id = lm.material_id
  )
ORDER BY lm.publication_year;
```

**Output**:

```sql
 material_id |       title        |   genre    | publication_year
-------------+--------------------+------------+------------------
          14 | The Art of Testing | Technology |             2020
          13 | Adventures of Ruby | Fiction    |             2022
(2 rows)
```

###### 4.2 Rarely Borrowed (e.g., ≤ 1 time)

```sql
SELECT
  lm.material_id,
  lm.title,
  COUNT(bt.transaction_id) AS times_borrowed
FROM library_material lm
LEFT JOIN borrowing_transactions bt
  ON bt.material_id = lm.material_id
GROUP BY
  lm.material_id,
  lm.title
HAVING
  COUNT(bt.transaction_id) <= 1
ORDER BY
  times_borrowed ASC,
  lm.publication_year;
```

**Output**:

```sql
 material_id |       title        | times_borrowed
-------------+--------------------+----------------
          14 | The Art of Testing |              0
           3 | Digital Marketing  |              0
          13 | Adventures of Ruby |              0
           4 | Sci-Fi Movie       |              0
          10 | Health & Wellness  |              0
           5 | Tech Today         |              0
           7 | Science Today      |              0
           9 | Nature Documentary |              1
           8 | Learning SQL       |              1
(9 rows)
```

> **Insight:** Books never or seldom borrowed are prime candidates for weeding or replacement.

---

##### 5. Borrowing Patterns & Under-Represented Genres/Authors

**Goal:** Compare actual borrowing activity against collection size to find gaps.

###### 5.1 Borrow Counts by Genre vs. Holdings

```sql
WITH holdings AS (
  SELECT genre, COUNT(*) AS num_titles
  FROM library_material
  WHERE type = 'Book'
  GROUP BY genre
),
borrows AS (
  SELECT lm.genre, COUNT(*) AS borrow_events
  FROM borrowing_transactions bt
  JOIN library_material lm
    ON bt.material_id = lm.material_id
  GROUP BY lm.genre
)
SELECT
  h.genre,
  h.num_titles,
  COALESCE(b.borrow_events, 0) AS borrow_events,
  ROUND( COALESCE(b.borrow_events,0)::numeric / h.num_titles, 2 ) AS avg_borrows_per_title
FROM holdings h
LEFT JOIN borrows b USING (genre)
ORDER BY avg_borrows_per_title DESC NULLS LAST;
```

**Output**:

```sql
   genre    | num_titles | borrow_events | avg_borrows_per_title
------------+------------+---------------+-----------------------
 History    |          1 |             4 |                  4.00
 Fiction    |          2 |             6 |                  3.00
 Mystery    |          1 |             2 |                  2.00
 Technology |          2 |             1 |                  0.50
(4 rows)

```

- **`avg_borrows_per_title`** shows which genres see heavy use relative to their size.
- **Low values** point to under-utilized genres—even if you have many titles, they might not circulate.

###### 5.2 Top/Bottom Authors by Borrow Rate

```sql
WITH author_holdings AS (
  SELECT b.author, COUNT(*) AS num_titles
  FROM books b
  GROUP BY b.author
),
author_borrows AS (
  SELECT b.author, COUNT(*) AS borrow_events
  FROM borrowing_transactions bt
  JOIN books b
    ON bt.material_id = b.material_id
  GROUP BY b.author
)
SELECT
  ah.author,
  ah.num_titles,
  COALESCE(ab.borrow_events, 0) AS borrow_events,
  ROUND( COALESCE(ab.borrow_events,0)::numeric / ah.num_titles, 2 ) AS avg_borrows_per_title
FROM author_holdings ah
LEFT JOIN author_borrows ab USING (author)
-- ORDER BY avg_borrows_per_title DESC
-- LIMIT 10;   -- top 10

-- and for bottom 10:
ORDER BY avg_borrows_per_title ASC
LIMIT 10;
```

**Output for Top 10**:

```sql
      author       | num_titles | borrow_events | avg_borrows_per_title
-------------------+------------+---------------+-----------------------
 John Doe          |          1 |             6 |                  6.00
 Agatha Christie   |          1 |             2 |                  2.00
 Jane Smith        |          2 |             4 |                  2.00
 Daniele Moschella |          1 |             1 |                  1.00
 Test Author       |          1 |             0 |                  0.00
(5 rows)
```

**Output for Bottom 10**:

```sql
      author       | num_titles | borrow_events | avg_borrows_per_title
-------------------+------------+---------------+-----------------------
 Test Author       |          1 |             0 |                  0.00
 Daniele Moschella |          1 |             1 |                  1.00
 Agatha Christie   |          1 |             2 |                  2.00
 Jane Smith        |          2 |             4 |                  2.00
 John Doe          |          1 |             6 |                  6.00
(5 rows)
```

> **Insight:** Authors with low **`avg_borrows_per_title`** may indicate stale or niche authors to reconsider.

---

##### 6. Recommendations for Collection Development

###### 6.1 Expand Under-Represented Genres

- Genres with < 5 % of holdings **and** low average borrows per title deserve more acquisitions.

###### 6.2 Weed Out Outdated/Unused Titles

- Books older than 25 years with ≤ 1 borrow in the past 5 years can be de-accessioned.

###### 6.3 Track Acquisition Cadence

- If you see fewer than \~ X new titles per year (compare to peer libraries), increase purchasing budgets.

###### 6.4 Author & Series Refresh

- Authors with zero or near-zero circulation—consider replacing with newer, in-demand writers.

###### 6.5 Community Needs Assessment

- Tie low-borrow genres back to patron surveys: maybe add popular sub-genres or digital formats.
