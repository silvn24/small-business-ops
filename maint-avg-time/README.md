**Maintenance Average Time & Pricing Alignment Analysis**

Overview

MaintAveTimeCalc-github.py is a Python script designed to analyse exported ERP visit data in a small service-business context.

The script calculates:
•	Average visit duration per customer and work type

•	Visit frequency counts
•	Most recent posted date
•	Most recently used price
•	Time-normalized pricing based on a defined baseline rate
•	Pricing variance relative to expected duration

This tool was built as a quick operational audit to evaluate whether customer pricing aligns with actual service time.
 
Business Question:
If the default service visit is X minutes and priced at $X,
are customers being priced appropriately relative to the average time spent on site?

This script provides a high-level pricing alignment check.
It is not intended as a full pricing optimization model.
 
What the Script Does
1.	Loads ERP visit export data from Excel.
2.	Creates a unique customer_id using Customer + Sub-location.
3.	Removes unwanted records (e.g., specific work codes).
4.	Calculates visit duration in hours from StartDate and EndDate.
5.	Groups by:
   o	customer_id
   o	WorkCode
6.	Calculates:
   o	Mean visit time
   o	Number of visits
   o	Most recent posted date
   o	Most recent price
7.	Computes:
   o	Over/Under duration relative to expected visit length
   o	Time-normalized price using a default per-minute rate
   o	Pricing variance (actual price – normalized price)
8.	Outputs results to a new Excel file.
 
Key Assumptions
•	Default visit duration: 42 minutes
•	Default baseline price: $58
•	Baseline rate per minute = 58 / 42
•	PostedDate represents the correct ordering for identifying most recent pricing.
•	Date-only precision is sufficient for determining recency.
**All numeric values in this repository are placeholders and do not reflect actual operational pricing.**
 
Output: Columns & Column	Description
customer_id:	Combined customer + sub-location identifier
WorkCode:	Type of service
Item_count:	Number of visits per customer and corresponding service type(s) in dataset
MostRecentPostedDate:	Most recent service posting date
Price:	Most recently used price
visit_time:	Average visit duration (hours)
Over_Under:	Difference from expected visit length (hours)
TimeNormalizedPrice:	Expected price based on baseline rate
PricingVariance:	Actual price minus normalized price
 
Technical Notes
•	Uses pandas for grouping and aggregation.
•	.groupby().mean() for average visit time.
•	.groupby().last() after sorting by date to obtain most recent price.
•	Key-aligned merges to prevent index misalignment.
•	Explicit column reindexing for structured output.
 
Limitations
This is a first-pass diagnostic tool. It does not:
•	Account for property size variations
•	Model tiered pricing logic
•	Evaluate profitability
•	Handle seasonal complexity
•	Detect price changes mid-cycle beyond most recent entry
A deeper pricing analysis would require modelling customer characteristics and visit complexity variables.
 
Intended Use
This script demonstrates:
•	Practical operational data analysis
•	ERP export transformation
•	Aggregation logic
•	Business-rule encoding
•	Analytical validation using Python

This script is shared for portfolio and demonstration purposes only.
