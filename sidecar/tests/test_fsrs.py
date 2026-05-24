import pytest
from app.ml.fsrs import FSRS

def test_fsrs_init_card():
    fsrs = FSRS()
    
    # 1. Again (grade=1)
    s, d, interval = fsrs.init_card(grade=1)
    assert s == fsrs.w[0]
    assert interval == 0
    
    # 2. Good (grade=3)
    s, d, interval = fsrs.init_card(grade=3)
    assert s == fsrs.w[2]
    assert interval == 3
    
    # 3. Easy (grade=4)
    s, d, interval = fsrs.init_card(grade=4)
    assert s == fsrs.w[3]
    assert interval == 7

def test_fsrs_next_interval():
    fsrs = FSRS()
    # next_interval = round(9 * stability)
    assert fsrs.next_interval(stability=1.0) == 9
    assert fsrs.next_interval(stability=0.5) == 4
    assert fsrs.next_interval(stability=10.0) == 90

def test_fsrs_step_brand_new():
    fsrs = FSRS()
    # reps == 0 should fallback to init_card
    s, d, interval = fsrs.step(stability=0.0, difficulty=0.0, reps=0, lapses=0, grade=3, elapsed_days=0)
    expected_s, expected_d, expected_i = fsrs.init_card(3)
    assert s == expected_s
    assert d == expected_d
    assert interval == expected_i

def test_fsrs_step_success():
    fsrs = FSRS()
    # reps > 0 and grade == 3 (Good)
    init_s, init_d, init_i = fsrs.init_card(3)
    
    new_s, new_d, new_i = fsrs.step(
        stability=init_s,
        difficulty=init_d,
        reps=1,
        lapses=0,
        grade=3,
        elapsed_days=3
    )
    
    # Success on a card should increase stability and interval
    assert new_s > init_s
    assert new_i > init_i
    assert new_d == init_d # grade=3 doesn't shift difficulty because (grade - 3) == 0

def test_fsrs_step_lapse():
    fsrs = FSRS()
    # reps > 0 and grade == 1 (Again)
    init_s, init_d, init_i = fsrs.init_card(3)
    
    new_s, new_d, new_i = fsrs.step(
        stability=init_s,
        difficulty=init_d,
        reps=1,
        lapses=0,
        grade=1,
        elapsed_days=3
    )
    
    # Lapse on a card should decrease stability and reset interval to 0 (relearn today)
    assert new_s < init_s
    assert new_i == 0
    assert new_d > init_d # difficulty increases on lapse
