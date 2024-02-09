# What is this project: 

This projects want to visualize the difference in return between a lump sum investment and a DCA. 

Sliders: 
- in the market -> duration of the investment 
- Match real returns interval -> calculate mean and std of the SP500 during this interval to use it as a base for the returns distribution
- Percentage invested at start portofolio *: percentage that is invested right away. 100% mean all capital invested from the very beginning, 0% mean the capital is invested evenly during the duration of the investment



## run it: 
`$ cd webapp`
`$ streamlit run app.py`


## To do/improvements: 
- improve test coverage of montecarlo
- dockerize it
- add a duration for your DCA time horizon (let's say that you want to invest 100K and the investment duration is 10 years, dca your cash into 2 years)

