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
 book_id | material_id |   author   |     isbn      | material_id |       title        | publication_year