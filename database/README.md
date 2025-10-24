# Chinook Database

The Chinook database is a sample database that represents a digital media store, including tables for artists, albums, media tracks, invoices, and customers.

## Database Schema

The Chinook database contains 11 tables:

### Core Tables

1. **Album** - Album information
   - AlbumId (Primary Key)
   - Title
   - ArtistId (Foreign Key to Artist)

2. **Artist** - Artist information
   - ArtistId (Primary Key)
   - Name

3. **Track** - Music track information
   - TrackId (Primary Key)
   - Name
   - AlbumId (Foreign Key to Album)
   - MediaTypeId (Foreign Key to MediaType)
   - GenreId (Foreign Key to Genre)
   - Composer
   - Milliseconds
   - Bytes
   - UnitPrice

4. **MediaType** - Media format types
   - MediaTypeId (Primary Key)
   - Name

5. **Genre** - Music genres
   - GenreId (Primary Key)
   - Name

### Customer and Sales Tables

6. **Customer** - Customer information
   - CustomerId (Primary Key)
   - FirstName
   - LastName
   - Company
   - Address
   - City
   - State
   - Country
   - PostalCode
   - Phone
   - Fax
   - Email
   - SupportRepId (Foreign Key to Employee)

7. **Invoice** - Invoice information
   - InvoiceId (Primary Key)
   - CustomerId (Foreign Key to Customer)
   - InvoiceDate
   - BillingAddress
   - BillingCity
   - BillingState
   - BillingCountry
   - BillingPostalCode
   - Total

8. **InvoiceLine** - Individual line items on invoices
   - InvoiceLineId (Primary Key)
   - InvoiceId (Foreign Key to Invoice)
   - TrackId (Foreign Key to Track)
   - UnitPrice
   - Quantity

### Employee and Playlist Tables

9. **Employee** - Employee information
   - EmployeeId (Primary Key)
   - LastName
   - FirstName
   - Title
   - ReportsTo (Foreign Key to Employee)
   - BirthDate
   - HireDate
   - Address
   - City
   - State
   - Country
   - PostalCode
   - Phone
   - Fax
   - Email

10. **Playlist** - Playlist collections
    - PlaylistId (Primary Key)
    - Name

11. **PlaylistTrack** - Mapping between playlists and tracks
    - PlaylistId (Foreign Key to Playlist)
    - TrackId (Foreign Key to Track)

## Statistics

- **Total Tables**: 11
- **Total Records**: ~25,000
- **Database Size**: ~1 MB
- **Relationships**: 10 foreign key relationships

## Sample Queries

Here are some example queries you can try:

### Basic Queries
```sql
-- Get all artists
SELECT * FROM Artist LIMIT 10;

-- Get all albums with artist names
SELECT Album.Title, Artist.Name
FROM Album
JOIN Artist ON Album.ArtistId = Artist.ArtistId
LIMIT 10;
```

### Analytics Queries
```sql
-- Top 10 best-selling tracks
SELECT Track.Name, COUNT(*) as TimesSold
FROM Track
JOIN InvoiceLine ON Track.TrackId = InvoiceLine.TrackId
GROUP BY Track.TrackId
ORDER BY TimesSold DESC
LIMIT 10;

-- Sales by country
SELECT BillingCountry, SUM(Total) as TotalSales
FROM Invoice
GROUP BY BillingCountry
ORDER BY TotalSales DESC;

-- Customer lifetime value
SELECT Customer.FirstName || ' ' || Customer.LastName as CustomerName,
       SUM(Invoice.Total) as TotalSpent
FROM Customer
JOIN Invoice ON Customer.CustomerId = Invoice.CustomerId
GROUP BY Customer.CustomerId
ORDER BY TotalSpent DESC
LIMIT 10;
```

### Complex Queries
```sql
-- Revenue by genre
SELECT Genre.Name, SUM(InvoiceLine.UnitPrice * InvoiceLine.Quantity) as Revenue
FROM Genre
JOIN Track ON Genre.GenreId = Track.GenreId
JOIN InvoiceLine ON Track.TrackId = InvoiceLine.TrackId
GROUP BY Genre.GenreId
ORDER BY Revenue DESC;

-- Employee sales performance
SELECT Employee.FirstName || ' ' || Employee.LastName as EmployeeName,
       COUNT(DISTINCT Invoice.InvoiceId) as InvoiceCount,
       SUM(Invoice.Total) as TotalSales
FROM Employee
JOIN Customer ON Employee.EmployeeId = Customer.SupportRepId
JOIN Invoice ON Customer.CustomerId = Invoice.CustomerId
GROUP BY Employee.EmployeeId
ORDER BY TotalSales DESC;
```

## Natural Language Query Examples

Try these natural language queries with the NL to SQL system:

1. "Show me all customers from the USA"
2. "What are the top 10 best-selling artists?"
3. "List all rock music tracks"
4. "What is the average invoice amount?"
5. "Show monthly sales for 2023"
6. "Which genres generate the most revenue?"
7. "Who are the top 5 customers by total purchases?"
8. "List all employees and their managers"
9. "Show the most popular playlists"
10. "What are the total sales by country?"

## Source

This database is sourced from the Chinook Database project:
https://github.com/lerocha/chinook-database

## License

The Chinook database is available under the MIT License.
