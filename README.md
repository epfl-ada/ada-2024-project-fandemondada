
# Beers in the USA: a societal study on American beer consumption
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
## Additional dataset:
[Rural and urban population proportions](https://data.census.gov/table/DECENNIALCD1182020.H2?q=rural) Periods 2000 - 2010 and 2010 - 2020
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
