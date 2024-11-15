
# Beers in the USA: a prediction of State of origin based on beer tastes
## Abstract: 
In this project, we aim to explore how beer preferences in the United States reflect broader societal trends by leveraging user-generated beer reviews and demographic data. Specifically, we will develop a method to infer a user’s demographic profile—such as state of residence, income, and age—based on their beer ratings.

The analysis will proceed in three stages. First, we will aggregate beer reviews by state to identify grading patterns unique to each state. Next, we will construct a formula that maps a user’s ratings of a small set of beers to a proportional affiliation with each state. Finally, we will combine these affiliations with demographic data to estimate the user’s profile based on the average characteristics of the identified states.

The results of this study will be showcased in an interactive data story, deployed on a public website, allowing users to input their beer ratings and receive a personalized demographic profile. This project bridges the gap between cultural preferences and societal data, offering insights into how personal tastes align with demographic patterns.

Finally, we will try to find some correlations between the beers we just found and the diverse demographic metrics previously chosen.

## Research questions:
1. **How do beer grading patterns differ across states in the United States?**  
   By analyzing user reviews, we aim to uncover state-specific preferences in beer styles, characteristics, and ratings.

2. **Can we accurately infer a user’s proportional affiliation to different states based on their beer ratings?**  
   We will develop a formula to map individual beer ratings to state-level preferences and assess its effectiveness.

3. **How can demographic data, such as age, income, and state population trends, be combined with beer grading patterns to generate a user’s profile?**  
   We will explore the relationship between state-specific beer preferences and demographic metrics to create meaningful user identities.

## Additional datasets:
Each additional dataset will contribute to defining the demographic attributes associated with each state.

U.S. Census Bureau, "URBAN AND RURAL." Decennial Census, DEC 118th Congressional District Summary File (accessed Friday, November 15, 2024)[ (link)](https://data.census.gov/table/DECENNIALCD1182020.H2?q=rural): this dataset provides the raw number of inhabitants per state living in cities and in the countryside. We have these numbers for the years 2010 and 2020. We wanted to predict wether someone was living in a rural or urban area based on their beer taste, but due to lack of intersting result (prediction was nearly always "urban" due to the vast majority of the American population living in cities), this dataset will most likely not be further used in our project.

U.S. Bureau of Economic Analysis, "SASUMMARY State annual summary statistics: personal income, GDP, consumer spending, price indexes, and employment" (accessed Friday, November 15, 2024)[ (link)](https://apps.bea.gov/itable/?ReqID=70&step=1#eyJhcHBpZCI6NzAsInN0ZXBzIjpbMSwyOSwyNSwzMSwyNiwyNywzMF0sImRhdGEiOltbIlRhYmxlSWQiLCI2MDAiXSxbIk1ham9yX0FyZWEiLCIwIl0sWyJTdGF0ZSIsWyIwIl1dLFsiQXJlYSIsWyJYWCJdXSxbIlN0YXRpc3RpYyIsWyItMSJdXSxbIlVuaXRfb2ZfbWVhc3VyZSIsIkxldmVscyJdLFsiWWVhciIsWyItMSJdXSxbIlllYXJCZWdpbiIsIi0xIl0sWyJZZWFyX0VuZCIsIi0xIl1dfQ==): this dataset provide various information about the American economy. We have yearly numbers from 1998 to 2023. We are only interested in the state wise income per capita, that will be used to predict the income of someone based on their beer taste.

Ann Arbor MI: Inter-university Consortium for Political and Social Research, Kaplan and Jacob, "Apparent Per Capita Alcohol Consumption: National, State, and Regional Trends 1977-2018" (accessed Friday, November 15, 2024)[ (link)](https://doi.org/10.3886/E105583V5-82040): this dataset contains various metrics about statewise alcohol consumption. We have yearly numbers from 1977 to 2018. The metrics that we will be using are the number of beers per capita and the beer ethanol per capita. They will be used to predict the yearly quantity of beers drunk based on someones beer tasts.

U.S. Census Bureau, "PROFILE OF GENERAL POPULATION AND HOUSING CHARACTERISTICS." Decennial Census, DEC Demographic Profile (accessed Friday, November 15, 2024)[ (link)](https://data.census.gov/table/DECENNIALDP2020.DP1?q=decenial%20census&g=010XX00US$0400000_9500000US5699999): this dataset contains many demographic characteristics, such as sex, race and relationship status. We have statewise number for the year 2020. The metrics most interesting to us is the age, that we will use to predict the age of the user based on their beer taste.


## Methods:

Our analysis consists of several stages, including data preprocessing, beer representativeness analysis, demographic correlation analysis, and data visualization. Below is an outline of each step:

### 1. Aggregating State-Level Beer Grades
- Analyze the beer review dataset to determine the average grades given to each beer by users in each state.
- Categorize and summarize the grading trends per state, creating a profile of beer preferences for each state.

### 2. Creating a Grading-Based State Association Formula
- Develop a mathematical formula that maps a user's grades of 5 specific beers to a proportional affinity for each state.  
  - Use state-level beer grade profiles as the baseline for comparison.
  - Normalize the user’s grading pattern against state profiles to estimate their connection to each state.

### 3. Mapping State Affinity to Demographic Attributes
- Combine the derived state proportions from the user’s grading with demographic datasets (e.g., rural/urban proportions, income, age distributions, beer consumption).
- Calculate a synthetic demographic ID for the user based on the weighted averages of state-level demographic attributes.
- Use this ID to represent the user's inferred demographic and regional profile.

### 4. Crafting a Data Story and Interactive Website
- Design an engaging data story that explains the methodology, findings, and societal insights of the analysis.
- Develop an interactive website where users can:
  - Explore visualizations of the state profiles and demographic trends derived from the data.
  - Input their beer ratings.
  - Receive a personalized demographic ID based on the analysis.


## Proposed timeline:
Deadline for each part:
- 22.11.24 - State-level Beer Grades
- 29.11.24 - Homework 2
- 6.12.24 - Association Formula
- 13.12.24 - Demographic Attributes
- 20.12.24 - Datastory and Website
  
## Organisation within the team:

For each task, a team member will oversee it. He will delegates subtasks to others and ensures all aspects are completed at the assigned deadline.

| Vassiliy Cheremetiev    | Patrick Gilliard    | Felix Schmeding        | John Taylor | Alex Zanetta          |
|-------------------------|---------------------|------------------------|-------------|-----------------------|
| State-level Beer Grades | Association Formula | Demographic Attributes | Homework 2  | Datastory and Website |
