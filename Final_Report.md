## Final Report
## Data Source
1.  Tampa Port Authority (2025) Annual Revenue Report https://flauditor.gov/pages/specialdistricts_efile%20rpts/2025%20tampa%20port%20authority.pdf
    1.  "Date of access: 10/12/2026
2.  Tampa Bay Estuary Program (TBEP) (2026-07-13) sgsegest https://tbep-tech.r-universe.dev/datasets
    1.  "Date of access: 10/5/2026
3.  Sarasota County wateratlas Water Quality 2026 https://sarasota.wateratlas.usf.edu/DataDownload/Default.aspx
    1.  Date of access: 10/10/2026
4.  Florida Fish and Wildlife Conservation Commission 2025 FL_Fisheries_Independent_Monitoring_Inshore_Stratified-Random_Sampling_Records,  https://data.florida-seacar.org/programs/details/69
    1.  Date of access: 10/11/2026

## Discovery
1. According to Florida Fish and Wildlife Conservation Commission, the sample size collected each year can be treated as a representation of the population size of the fish at that year
   1. Still fairly inaccurate due to sample size based entirely on whether the scientist can catch the fish
   2. Still accurate enough to infer some conclusions.
2. No strong correlation between the total fish sample size and other features in the dataset
3. Positive correlation between the PH of the water with the temperature of the water
4. No significant correlation between salinity and the temperature of the water.
5. No strong correlation between PH and the amount of dissolved ammonia in the water.
6. No strong correlation between total fish sampling and sea grass coverage.
   1. However, strong correlation between these two factors for specific species.
7. Significant correlation between sea grass coverage and total fish sample size with dock usage.

## Visualization Explanation
1. Dash presentation. Below is a dedicated bar containing a next and previous button. These buttons are how you traverse between the different tabs in the presentation
2. Dropdown menu on slides 8, 9, and 10 are not linked together. Originally wished to have these drop down menus link together for the same of writing less code, but I value my display looking visually pleasing rather than looking cluttered
3. The presentation itself is treated like a report.

## Conclusion
1. As expected, there is no strong correlation between the total fish sample size and other features in the dataset. 
   1. Each species react differently to their environment
   2. Decided to see the relations between each species. 
2. Hypothesis that PH and Salinity is correlated with Water Temperature is partially true
   1. Positive correlation between the PH of the water with the temperature of the water. 
   2. No significant correlation between salinity and the temperature of the water.
3. There also doesn't seem to be a strong correlation between PH and the amount of dissolved ammonia in the water. This runs counter with one of my hypothesis. 
4. Overall, there does not seem to be a strong correlation between total fish sampling and sea grass coverage. 
   1. Specific species have a strong correlation between these two factors. 
   2. This makes sense as not every marine species depends on sea grass for survival, but those that do will be severely impacted. 
5. There seems to be a correlation between sea grass coverage and total fish sample size with dock usage, 
   1. Supports my hypothesis that the increase vessel presence, which often use oil to run, as well as intensive land use of the area is leading to the decline of marine life and sea grass coverage. 
6. Overall, there seems to be some correlation, although it is not direct, between human anthropomorphic climate change and a decline in marine life population in the Tampa Bay region. 
   1. However, the results are not conclusive and more data is required to make further analysis.

## Feedback
1. Go into more detailed during presentation of certain aspects of the visualization for the audience.
2. Personal feedback, do not dwell to much on certain topics and waste time. Try and move quicker to allow for some questions.

## Future Improvements
1. Last minute discovered I used the wrong region water quality data. Instead of using the tampa bay region, I recently found out that the sarasota bay region is located just a little bit south of the tampa bay region
2. I recently found out more about the TBEP tools contains other data that would be interesting to look into, such as benthic and nekton data.
   1. Benthic refers to bottom feeding stationary marine organisms like clams and oysters
   2. Nekton refers to swimming marine organisms like fish.
3. There could be other things I would love to do with regard to expanding the scope of the project to more regions around Florida.