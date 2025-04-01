To create a new PostgreSQL database, schema, and table using the PostgreSQL command-line interface (CLI), follow these steps:

### **Step 1: Access PostgreSQL CLI**
1. Open a terminal or command prompt.
2. Connect to PostgreSQL as a superuser (e.g., `postgres`):
   ```sh
   psql -U postgres
   ```
   If your PostgreSQL is running on a specific host or port, use:
   ```sh
   psql -U postgres -h localhost -p 5432
   ```
   You may need to enter the password.

---

### **Step 2: Create a New Database**
To create a new database (e.g., `mydb`):
```sql
CREATE DATABASE mydb;
```
Connect to the newly created database:
```sh
\c mydb
```

---

### **Step 3: Create a New Schema**
By default, PostgreSQL uses the `public` schema. To create a new schema (e.g., `myschema`):
```sql
CREATE SCHEMA myschema;
```
Set the schema as the default for the session:
```sql
SET search_path TO myschema;
```

---

### **Step 4: Create a Table in the Schema**
To create a new table (e.g., `employees`) inside `myschema`:
```sql
CREATE TABLE myschema.employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    department VARCHAR(50)
);
```

---

### **Step 5: Insert Data (Optional)**
Insert sample data into the `employees` table:
```sql
INSERT INTO myschema.employees (name, age, department) 
VALUES ('John Doe', 30, 'IT');
```

---

### **Step 6: Verify Table Creation**
To list all schemas:
```sql
SELECT schema_name FROM information_schema.schemata;
```
To list all tables in `myschema`:
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'myschema';
```
To view table data:
```sql
SELECT * FROM myschema.employees;
```

---

### **Step 7: Exit PostgreSQL CLI**
Exit the PostgreSQL shell by typing:
```sh
\q
```

Now, you have successfully created a **PostgreSQL database, schema, and table** using the CLI. Let me know if you need further details!
