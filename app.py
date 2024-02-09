from requests import session
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from engine.montecarlo import (
    performance_stats,
    simulate_multiple_cycles,
    aggregate_results,
)

import logging
import plotly.graph_objects as go

st.title("DCA vs Lump Sum MonteCarlo Simulator")

year_invested = st.sidebar.slider("Years in the market", min_value=1, max_value=50)
portfolio_returns = st.sidebar.slider(
    "Match real returns interval",
    min_value=1928,
    max_value=2021,
    value=(1928, 2021),
    help="Based on the analysis of the following resource: http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html",
)
portfolio_value = st.sidebar.number_input("Insert a portfolio value", value=100_000)
number_of_simulations = st.sidebar.number_input(
    "Number of simulations to run", value=10_000, max_value=100_000
)

strategy_portfolio_A = st.sidebar.slider(
    "Percentage invested at start portofolio A",
    min_value=0,
    max_value=100,
    help="100 being Lump sum and 0 being pure DCA -> yearly invested total_portofolio*(100 - percentage_invested_right_away) / years invested",
)
strategy_portfolio_B = st.sidebar.slider(
    "Percentage invested at start portofolio B",
    min_value=0,
    max_value=100,
    help="100 being Lump sum and 0 being pure DCA -> yearly invested total_portofolio*(100 - percentage_invested_right_away) / years invested",
)


button_check = st.sidebar.button("Submit")

if button_check:

    mean, std = performance_stats(portfolio_returns[0], portfolio_returns[1])
    portfolioA = simulate_multiple_cycles(
        number_of_simulations,
        mean,
        std,
        strategy_portfolio_A / 100.0,
        portfolio_value,
        year_invested,
    )
    portfolioB = simulate_multiple_cycles(
        number_of_simulations,
        mean,
        std,
        strategy_portfolio_B / 100.0,
        portfolio_value,
        year_invested,
    )
    results = aggregate_results(portfolioA, portfolioB)

    st.write(
        f"Mean and std of expected returns",
        np.around(mean, decimals=2),
        " \u00B1 ",
        np.around(std, decimals=2),
    )
    st.write("Mean portofolio A", np.around(results.portfolioA.mean(), decimals=2))
    st.write("Mean portfolio B ", np.around(results.portfolioB.mean(), decimals=2))

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=results.portfolioA, name="PORTFOLIO A", marker_color="blue", bingroup=1
        )
    )
    fig.add_trace(
        go.Histogram(
            x=results.portfolioB, name="PORTFOLIO B", marker_color="red", bingroup=1
        )
    )
    fig.add_vline(
        x=results.portfolioA.mean(), line_width=1, line_dash="dash", line_color="blue"
    )
    fig.add_vline(
        x=results.portfolioB.mean(), line_width=1, line_dash="dash", line_color="red"
    )

    # The two histograms are drawn on top of another
    fig.update_layout(barmode="overlay")
    fig.update_traces(opacity=0.5)
    fig.update_layout(width=1100, height=1100)

    st.plotly_chart(fig, clear_figure=True)
