import pandas as pd
import numpy as np
from numba import jit


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html

historical_sp500_date = pd.read_excel(
    "data/histretSP.xls",
    sheet_name="Returns by year",
    skiprows=range(0, 17),
    skipfooter=10,
)
historical_sp500_date = historical_sp500_date[
    ["Year", "S&P 500 (includes dividends)2"]
].rename(columns={"S&P 500 (includes dividends)2": "SP&500_return_inflation_adjusted"})


def performance_stats(start_year, end_year):
    returns = historical_sp500_date[
        (historical_sp500_date.Year >= start_year)
        & (historical_sp500_date.Year <= end_year)
    ]
    mean = returns["SP&500_return_inflation_adjusted"].mean()
    std = returns["SP&500_return_inflation_adjusted"].std()

    return mean, std


@jit(nopython=True)
def simulate_single_investment_cycle(start, increment, performance):
    tmp = start
    for item in performance:
        tmp = tmp * (1 + item) + increment
    return tmp


@jit(nopython=True)
def simulate_multiple_cycles(
    n_simulations: int,
    avg_returns: float,
    std_returns: float,
    lump_sum_percentage: float,
    total_portofolio: float,
    year_invested: int,
):
    result = []
    for _ in range(0, n_simulations):
        sim_returns = np.random.normal(avg_returns, std_returns, year_invested)
        start = total_portofolio * lump_sum_percentage
        increment = (total_portofolio - start) / year_invested
        # print(start, increment)
        result.append(
            [_, simulate_single_investment_cycle(start, increment, sim_returns)]
        )

    return result


def aggregate_results(portfolioA, portfolioB):
    portfolioA = pd.DataFrame(portfolioA, columns=["N_sim", "portfolioA"])
    portfolioB = pd.DataFrame(portfolioB, columns=["N_sim", "portfolioB"])

    results = portfolioA.merge(portfolioB, how="outer", on="N_sim")

    return results
