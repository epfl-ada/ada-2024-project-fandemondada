# Favoring local beers: a study on the evolution of american beer consumption
## Abstract: 
In this project, we aim to explore how beer consumption in the United States reflect broader societal trends by leveraging user-generated beer reviews. Specifically, we will look into the evolution of the distance between the place of brewing and the place of consumption of the beer.

The analysis will proceed in three stages. First, we will aggregate beer reviews by state to identify the variation in local, national and foreign beer consumption unique to each state. Next, we will compute the statewise average of the distance between the brewing and drinking place. Finally, we will look at their evolution over time and try to explain it.

The results of this study will be showcased in an interactive data story, deployed on a public, allowing the users to navigate through our thoughts process and reach the same conclusion as us.

## Research questions:
1. **How does the distance between the place of brewing and of drinking evoluate over time?**  
   By analysing beer reviews, we aim to uncover clear trends in the evolution of the local consumption.

2. **Can we accurately explain the evolution found?**  
   We will look for correlations with various data/metrics to explain what we have just found.

## Additional datasets:
**The additional datasets are not used anymore, as we changed the direction that our project took.**

U.S. Census Bureau, "URBAN AND RURAL." Decennial Census, DEC 118th Congressional District Summary File (accessed Friday, November 15, 2024)[ (link)](https://data.census.gov/table/DECENNIALCD1182020.H2?q=rural): this dataset provides the raw number of inhabitants per state living in cities and in the countryside. We have these numbers for the years 2010 and 2020. We wanted to predict wether someone was living in a rural or urban area based on their beer taste, but due to lack of intersting result (prediction was nearly always "urban" due to the vast majority of the American population living in cities), this dataset will most likely not be further used in our project.

U.S. Bureau of Economic Analysis, "SASUMMARY State annual summary statistics: personal income, GDP, consumer spending, price indexes, and employment" (accessed Friday, November 15, 2024)[ (link)](https://apps.bea.gov/itable/?ReqID=70&step=1#eyJhcHBpZCI6NzAsInN0ZXBzIjpbMSwyOSwyNSwzMSwyNiwyNywzMF0sImRhdGEiOltbIlRhYmxlSWQiLCI2MDAiXSxbIk1ham9yX0FyZWEiLCIwIl0sWyJTdGF0ZSIsWyIwIl1dLFsiQXJlYSIsWyJYWCJdXSxbIlN0YXRpc3RpYyIsWyItMSJdXSxbIlVuaXRfb2ZfbWVhc3VyZSIsIkxldmVscyJdLFsiWWVhciIsWyItMSJdXSxbIlllYXJCZWdpbiIsIi0xIl0sWyJZZWFyX0VuZCIsIi0xIl1dfQ==): this dataset provide various information about the American economy. We have yearly numbers from 1998 to 2023. We are only interested in the state wise income per capita, that will be used to predict the income of someone based on their beer taste.

Ann Arbor MI: Inter-university Consortium for Political and Social Research, Kaplan and Jacob, "Apparent Per Capita Alcohol Consumption: National, State, and Regional Trends 1977-2018" (accessed Friday, November 15, 2024)[ (link)](https://doi.org/10.3886/E105583V5-82040): this dataset contains various metrics about statewise alcohol consumption. We have yearly numbers from 1977 to 2018. The metrics that we will be using are the number of beers per capita and the beer ethanol per capita. They will be used to predict the yearly quantity of beers drunk based on someones beer tasts.

U.S. Census Bureau, "PROFILE OF GENERAL POPULATION AND HOUSING CHARACTERISTICS." Decennial Census, DEC Demographic Profile (accessed Friday, November 15, 2024)[ (link)](https://data.census.gov/table/DECENNIALDP2020.DP1?q=decenial%20census&g=010XX00US$0400000_9500000US5699999): this dataset contains many demographic characteristics, such as sex, race and relationship status. We have statewise number for the year 2020. The metrics most interesting to us is the age, that we will use to predict the age of the user based on their beer taste.


## Methods:

Our analysis consists of several stages, including data preprocessing, local consumption analysis, explanations of our results, and data visualization. Below is an outline of each step:

### 1. Statewise local consumption
- Analyze the beer review dataset to determine the amount of local, national and foreign beers drunk in each state.

### 2. Distance evolution
- Look into the evolution of the distance between the place of brewing and of consumption of the beer: 
  - Use state-level average to get more precise results.
  - Reduce the complexity by considering only monthly results.

### 3. Explanation of the results
- Try to combine the evolution of the distance with diverse pertinent factors, namely:
   - The evolution of the climate change attitude.
   - The evolution of the patriotism over time,
   - The evolution of the number of breweries.

### 4. Crafting a Data Story and Interactive Website
- Design an engaging data story that explains the methodology, findings, and insights of the analysis.
- Develop an interactive website where users can:
  - Explore visualizations of the state profiles derived from the data.
  - Travel through time with interractive plots.


## Proposed timeline:
Deadline for each part:
- 22.11.24 - Statewise local consumption
- 29.11.24 - Homework 2
- 6.12.24 - Distance evolution
- 13.12.24 - Explanation of the results
- 20.12.24 - Datastory and Website
  
## Organisation within the team:

For each task, a team member will oversee it. He will delegates subtasks to others and ensures all aspects are completed at the assigned deadline.

| Vassiliy Cheremetiev        | Patrick Gilliard      | Felix Schmeding            | John Taylor | Alex Zanetta            |
|-----------------------------|-----------------------|----------------------------|-------------|-------------------|
| Statewise local consumption | Datastory and Website | Explanation of the results | Homework 2  | Distance evolution |
