
## Database Engineering


```python
import pandas as pd
```


```python
# Read in cleaned CSV files
measurements_df = pd.read_csv('clean_measurements.csv')
stations_df = pd.read_csv('clean_stations.csv')
```


```python
# SQLAlchemy dependencies
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# create base
Base = declarative_base()
```


```python
# Data types from SQLAlchemy 
from sqlalchemy import Column, Integer, String, Float, Date
```


```python
# Create base classes
class Measurements(Base):
    __tablename__ = 'measurements'
    meas_id = Column(Integer, primary_key=True)
    station = Column(String(255))
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Float)

class Stations(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    station = Column(String(255))
    name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
```


```python
# Create sqlite engine
engine = create_engine("sqlite:///hawaii.sqlite")
```


```python
# Add metadata to tables
Base.metadata.create_all(engine)
```


```python
# Append data from CSV created df to correct classes(tables)
measurements_df.to_sql('measurements', engine, if_exists='append', index=False)
```


```python
stations_df.to_sql('stations', engine, if_exists='append', index=False)
```


```python
from sqlalchemy.orm import Session
session = Session(bind=engine)
```


```python
session.commit()
```
