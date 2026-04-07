# AltOnline AB: End-to-End Relational Database Design

## Project Overview
This project involves the full-cycle design and implementation of a relational database system for **AltOnline AB**, a Swedish e-commerce platform. The project spans from initial customer requirements to conceptual modeling (ER), relational mapping, 3NF normalization, and the development of Python-based applications for database interaction.

### Key Objectives:
*   **Conceptual Modeling**: Architected a complex ER diagram including recursive relationships for hierarchical data and weak entities for historical tracking.
*   **Schema Optimization**: Normalized the database to **Third Normal Form (3NF)** to ensure data integrity and minimize redundancy.
*   **Performance Tuning**: Implemented and analyzed SQL indexing (BTree) to optimize query execution time.
*   **Application Development**: Built CLI-based Python applications to interface with the database for real-time inventory management.

---

## Tech Stack
*   **Database:** Mimer SQL (RDBMS)
*   **Languages:** Python (mimerpy, pandas)
*   **Tools:** ERDPlus, Git, SSHTunnel
*   **Core Concepts:** 3NF Normalization, BTree Indexing, ETL Logic, CRUD Operations

---

## Project Structure
The repository is organized into the following modules:

*   **/diagrams**: Contains the conceptual ER Diagram and the logical Relational Schema.
*   **/scripts**: 
    *   `department_browser.py`: Implements recursive logic to navigate a hierarchical "tree" of store departments.
    *   `product_update.py`: A management tool for CRUD operations on product metadata, pricing, and discount calculations.
*   **/docs**: Comprehensive project report detailing the normalization process, functional dependencies, and performance benchmarks.

---

## Key Features

### 1. Hierarchical Department System
Designed a recursive "Parent-Child" relationship within the Department table. The system distinguishes between "Branch" departments (which show sub-categories) and "Leaf" departments (which contain products), utilizing specialized SQL queries to navigate the tree structure.

### 2. Order History Tracking
Implemented a weak entity pattern (`order_status_hist`) to track the lifecycle of an order (New -> Open -> Dispatched), allowing for historical auditing of order status changes over time.

### 3. Automated Pricing Logic
Product pricing is handled via derived attribute logic. The system calculates current retail prices in real-time by applying tax percentages and store-wide discounts to the base retail price.

### 4. SQL Performance Optimization
Analyzed query execution plans using `EXPLAIN`. By implementing BTree indices on frequently filtered columns like `featured` and `discount_perc`, we achieved significant performance gains for homepage rendering and sales sorting.

---

## ⚙️ How to Run
*Detailed execution instructions can be found in the [docs/Instructions.pdf](docs/Instructions.pdf).*

1. **Prerequisites**:
   ```bash
   pip install mimerpy pandas sshtunnel
