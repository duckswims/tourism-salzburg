# Salzburger Guest Mobility Ticket -- Tourism Technology Festival 3.0

## Challenge Overview

The **Salzburger Verkehrsverbund (SVV)** provides the **Salzburg Guest Mobility Ticket** for tourists, which allows them to travel throughout the province of Salzburg as part of their paid tourism fee/incoming tax.

Aside from being a convenient travel service, the ticket also supports the registration process for incoming tourists. Guests check in to public transport by scanning their ticket, using specially installed hardware.

### Challenge Points

1. **Low Scanning Rates:** Even though guests should scan their tickets, only 10–30% do so due to:

   * Lack of awareness about the scanning process.
   * Inconvenience, e.g., when entering with skiing gear.
2. **Data Utilization:** Use the provided dataset to extract insights and identify gaps in information.
3. **Better Tracking:** Explore ways for SVV to track tourist activity in public transport to measure the impact of the Salzburg Guest Mobility Ticket.


## Our Solution
![dashboard](assets/dashboard.png)

We built an **interactive dashboard** with **Streamlit** to:

* Analyze the dataset provided by SVV.
* Predict passenger boarding counts on specific routes.
* Help SVV staff make informed decisions about **route demand** at specific dates and times.

### Features

* **Passenger Analytics:** View daily and route-wise passenger boarding trends.
* **Prediction:** Estimate boarding counts for better resource planning.
* **Route Visualization:**
  * OpenStreetMap (OSM) to display bus routes.
  * GTFS data for accurate bus stop locations.
  * Statistics Austria for **Gemeinde** information and tourism statistics.


## Tech Stack

* Python
* Streamlit
* Pandas, NumPy, Altair for data analysis and visualization
* OpenStreetMap & GTFS for spatial visualization


## Setup Instructions

1. **Create a virtual environment and activate it**:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate     # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**:

   ```bash
   streamlit run app.py
   ```


## Data Sources

* SVV dataset provided for the hackathon challenge
* OpenStreetMap (OSM) for route mapping
* GTFS data for bus stop locations
* Statistics Austria for tourism and Gemeinde information
