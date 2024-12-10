# Does Public Law 280 Explain Variation in AIAN Drug Related Deaths?

My project is examining variation in drug-related deaths amongs the American Indian and Alaskan
Native (AIAN) populations. Specifically I am interested in whether drug-related deaths are higher
on Native American reservations that lack criminal jurisdiction under Public Law 280. Public Law 280
is a law passed in 1953 that gave certain states the ability to assume legal jurisdiction on Native American
Reservations that was otherwise held by the federal government. In the process, it gave the states
jurisdiction over all minor and municipal criminal offenses. In practice what that means is that
a Tribal Authority on a reservation under public law 280 has no authority to enforce municipal laws
unless county law enforcement delegate some authority to it. Tribal Authorities on reservations
not covered by public law 280 can make and enforce their own municipal codes. 

I am researching if the difference in who is responsible for criminal jurisdiction explains variation in drug-related deaths. The idea being that tribal authorities are better able to handle drug use and 
drug distribution on reservations than county authorities. I am conducting this research
as part of my work as an intern with the University of Chicago Health Lab.

# What data will I use for this project?

I am using the public use multiple causes of mortality file from 2000-2020 managed by the NCHS (see: https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm#Mortality_Multiple). I am interested in the state-level aggregate
of American Indian and Alaskan Native (AIAN) drug related deaths as well as the county-level aggregate AIAN drug
related deaths. The state-level data has 1100 observations state-year observations (although the number of observations that are relevant when dropping states that don't have reservations is smaller). At the county level we
begin with 69,358 observations although once again there will be fewer observations when we drop non-reservation counties.

# Questions

1. One of the first challenges is visualizing both:
- Which Counties/ States have the highest AIAN drug related death rates
- On the same visualization showing their relative AIAN populations
What suggestions would you have for accomplishing both goals on the same plot? For
context it is relvant to viewers which states carry more "weight" when looking at
this relationship.

2. I have been using a lot of regressions. What is a good starting point for
displaying regression output in a visually appealing and interpretable fashion?
