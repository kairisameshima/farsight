# Interview Take-Home Project

This take-home project and its functionality has been scoped in a separate document sent to you. Feel free to create any new files and edit existing files as needed. Make sure to update this README with instructions and important notes before returning the project.

## Setup

1. **Create and activate a virtual environment**

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI backend**

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Workflow One**

   ```bash
   localhost:8000/api/trend/sector?sector={sector}
   localhost:8000/api/trend/sector_chart?sector={sector}
   ```

   The first endpoint provides the total and average fundraising amount for the top 100 matched companies within a given sector.

   I included the second endpoint to provide point by point data so that fundraising rounds over time could be visualized through a chart. The inclusion of the `org_uuid` will allow us to group these events by a color key and `organization_name` can be used in a hover-over to display the organizations name.

   Use case:
   "How are investments in a given sector?" Given this data we can see trends if for certain sectors funding is skewed towards earlier or later stages. We can also see how long it takes between funding rounds and how they may increas or decrease over time.

5. **Workflow Two**
   ```bash
   localhost:8000/api/trend/top_investors?sector=finance
   ```
   This second workflow retrieves the top investors in a given sector. It shows the number of fundraising deals that have been closed per given investor, it also shows the total amount of funding they have given.

   Use case:
   "Who is investing into a given sector?" Given the data we retrieve, if coupled with a more in depth "Investor" table, we could get insights into the top investors in a given sector. With more endpoints, we could also drill down into specific investors ansewring questions such as: "Are their investments skewed towards early or late stage startups?" "How are their investments distributed across industries?"
   This endpoint would be a great start into gaining insights into the major investors within a given sector.

6. **Future Improvements**
   1. **SQLAlchemy**
   I'm currently using SQLAlchemy for my ORM because it easy to convert an existing DB into a SQLAlchemy schema using `sqlacodegen`.
   SqlAlchemy in my opinion isn't a long term solution because of it's tendency to allow queries to be unexpectedly made to the DB (Relational fields can quickly lead to n+1 queries) and because the DB record can be manipulated easily.
   To improve this, a V2 would move querying the DB and retrieving records to a `repository.py` model where we would only use the SQLAlchemy models for querying the DB and the data would be transformed into Pydantic schemas. The repository would be the single source for retrieving, updating and deleting records.
   2.  **Refactor `postgres_service.py`**
   For sake of simplicity I am having the postgres service do a lot of opinionated retrieving of data from postgres. In a V2 I would organize the backend to organized by domain, where each domain is a business entity that we deal with in the backend. If we need to do any kind of business logic beyond retrieving data from the DB, we can create a method in a domain's `service.py` service.
   ```bash 
   route (orchestrate services) -> domain service (perform business logic) -> repository (retrieve data)
   ```

   ```plaintext
   farsight/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py
   │   ├── routes/
   │   │   ├── __init__.py
   │   │   ├── trends.py
   │   ├── services/
   │   │   ├── __init__.py
   │   │   ├── pinecone_service.py
   │   │   ├── trend_service.py
   │   ├── models/
   │   │   ├── __init__.py
   │   │   ├── models.py
   │   ├── funding_rounds/
   │   │   ├── __init__.py
   │   │   ├── repository.py
   │   │   ├── service.py
   │   ├── organizations/
   │   │   ├── __init__.py
   │   │   ├── repository.py
   │   │   ├── service.py
   │   ├── acquisitions/
   │   │   ├── __init__.py
   │   │   ├── repository.py
   │   │   ├── service.py
   ...
   ```