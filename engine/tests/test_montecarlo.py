import pytest
import numpy as np
import math
from engine.montecarlo import simulate_single_investment_cycle, simulate_multiple_cycles


def test_simulate_valid_return_one_year_investment_dca() -> None:
    assert simulate_single_investment_cycle(0, 100_000, [0.04]) == 100_000.0
    
def test_simulate_valid_return_one_year_investment_lump_sum() -> None:
    assert simulate_single_investment_cycle(100_000, 0, [0.04]) == 100_000 * (1 + 0.04)

def test_simulate_valid_return_one_year_investment_a_third_invested() -> None:
    assert simulate_single_investment_cycle(100_000, 20_000, [0.04]) == 100_000*(1 + 0.04) + 20_000

def test_simulate_multiple_years() -> None:
    assert simulate_single_investment_cycle(0, 50_000, [0.04, 0.01]) == 100_500.

def test_simulate_multiple_years_no_increments() -> None:
    assert simulate_single_investment_cycle(100_000, 0, [0.04, 0.01]) == 105_040.

def test_simulate_multiple_years_w_increments() -> None:
    assert simulate_single_investment_cycle(50_000, 25_000, [0.04, 0.01]) == 102_770.0
    
def test_simulate_multiple_years_w_increments_max_return() -> None:
    assert simulate_single_investment_cycle(50_000, 25_000, [1.00, 0.01]) == (50_000*(1+1.00) + 25_000)*(1+0.01) + 25_000

def test_simulate_multiple_cycles() -> None:
    assert np.isclose(simulate_multiple_cycles(1, 0.05, 0, 1, 10_000, 3), [[0, 10_000*(math.pow(1.05,3))]]).all()  