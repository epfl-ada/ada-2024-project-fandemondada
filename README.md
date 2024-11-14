
# Beers in the USA: a societal study on American beer consumption
## Abstract: 
In this period of deep political turmoil in the USA, symptom of a country more divided than ever, we want to find out if this division can also be found in the beers drunk. In this project, we will investigate the links between multiple demographic metrics of the American states and beer consumption and production in them.

Specifically, we will begin by deep diving into each State’s favourite beers based on RateBeer and BeerAdvocate reviews and find out which beers represents the state the best. In parallel, we will look into what beers are being produced in each State to discover the one most representative of it.

Finally, we will try to find some correlations between the beers we just found and the diverse demographic metrics previously chosen.
## Research questions:
-	Based on the reviews from American users, what is the beer most liked in a state? More specifically, we will find out the characteristics of a beer and propose a candidate most representative of it.
-	Based on the origin of the beers reviewed, what is the beer most produced in a state? Is it also the most liked? We will use the absolute number of beers coming from the state and not the volume produced.
-	Can we find a correlation between the beers we just found and some demographic metrics of the states? Is it possible to find out some beers most representative of each metrics?
## Additional dataset:
[Rural and urban population proportions](https://data.census.gov/table/DECENNIALCD1182020.H2?q=rural) Periods 2000 - 2010 and 2010 - 2020
## Methods:

Our analysis consists of several stages, including data preprocessing, beer representativeness analysis, demographic correlation analysis, and data visualization. Below is an outline of each step:

### 1. Data Preprocessing
- **Dataset Cleaning**: 
  - Clean the datasets by removing incomplete entries and outliers to ensure data reliability. Convert the datasets provided as txt to dictionaries in format csv for easier access 
  - Standardize fields such as beer style, state names, and user location to prevent discrepancies.
  - Merge datasets on beers and breweries by state for a consolidated view of beer production and consumption.
- **Feature Engineering**: 
  - Create relevant features from reviews, such as average ratings, most-reviewed beers, and unique flavor profiles.
  - Generate state-based beer consumption metrics, such as total reviews per beer type and average ratings, to quantify beer preferences.
- **Demographic Data Integration**: 
  - Extract urban and rural population proportions for each state across different years.
  - Normalize demographic data to account for population differences across states, enabling fair comparison.

### 2. Beer Representativeness Analysis
- **Defining Representative Beers by Consumption**:
  - Identify the most "liked" beers in each state based on average review scores and user sentiment.
  - Use clustering techniques on beer styles, ratings, and flavors to identify characteristics unique to each state’s preferred beer types.
- **Defining Representative Beers by Production**:
  - Calculate the number of unique beers produced in each state to find production trends.
  - Determine which beer types are most commonly produced in each state, assessing whether these correlate with popular styles by reviews.

### 3. Additional Dataset and Correlation Analysis
- **Beer and Demographics Correlation**:
  - Calculate correlation coefficients between beer preferences and demographic variables like urban/rural population ratios.
  - Run regression models to evaluate if certain demographic characteristics can predict beer preferences or production trends by state.
  - Explore additional factors, such as the presence of local breweries, and how they may impact beer choices in different demographic areas.

### 4. Datastory and Data Visualization
- **DataStory**:
  - Synthesize key findings and insights from the analysis to shape a compelling narrative that guides readers through the relationships between beer preferences, state demographics, and regional characteristics.
- **Website**
  - Create an interactive website to present the data story, allowing readers to explore the connections between demographic characteristics and beer culture across states.
- **Geographic Visualizations**:
  - Create interactive maps showing beer preferences and production volume by state, using color coding for easy comparison.
  - Plot demographic variables alongside beer preference metrics to visualize regional patterns and possible correlations.
- **Graphs and Charts**:
  - Use bar charts to display the most popular beer styles and average ratings per state.
  - Visualize correlations between demographic metrics and beer characteristics using scatter plots and heatmaps.
## Proposed timeline:
- Week 10 - Data analysis: analyse the beer data and combine it with the data from the additional datasets in meaningful ways regarding the research questions
- Week 11 - Homework 2: take care of the homework, do some more data analysis
- Week 12 - Concept of the Data Story: do some more data analysis, look at what the data has been telling us and decide what to present and how to do it
- Week 13 - Begin the website: finish the last data analysis, create the first graphics and start the text
- Week 14 - Milestone 3 : finish the data story and clean up the code 
## Organisation within the team:
| Vassiliy Cheremetiev | Patrick Gilliard | Felix Schmeding    | John Taylor | Alex Zanetta      |
|----------------------|------------------|--------------------|-------------|-------------------|
| Data analysis        | Website          | Coffee + good mood | Homework 2  | Data storytelling |

The roles represent the main responsible for each part, everyone will work on all parts of the project.