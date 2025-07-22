import pytest
import pandas as pd
from definition_85effa0ea0f049568644c615bd80ebc9 import aggregate_losses

def test_aggregate_losses_empty_dataframe():
    df = pd.DataFrame({'gross_loss': [], 'transferred_loss': [], 'retained_loss': []})
    expected = {'gross_loss': 0.0, 'transferred_loss': 0.0, 'retained_loss': 0.0}
    result = aggregate_losses(df)
    assert result['gross_loss'] == expected['gross_loss']
    assert result['transferred_loss'] == expected['transferred_loss']
    assert result['retained_loss'] == expected['retained_loss']


def test_aggregate_losses_standard_values():
    df = pd.DataFrame({'gross_loss': [100, 200, 300], 'transferred_loss': [50, 100, 150], 'retained_loss': [50, 100, 150]})
    expected = {'gross_loss': 600.0, 'transferred_loss': 300.0, 'retained_loss': 300.0}
    result = aggregate_losses(df)
    assert result['gross_loss'] == expected['gross_loss']
    assert result['transferred_loss'] == expected['transferred_loss']
    assert result['retained_loss'] == expected['retained_loss']

def test_aggregate_losses_negative_values():
    df = pd.DataFrame({'gross_loss': [-100, -200, -300], 'transferred_loss': [-50, -100, -150], 'retained_loss': [-50, -100, -150]})
    expected = {'gross_loss': -600.0, 'transferred_loss': -300.0, 'retained_loss': -300.0}
    result = aggregate_losses(df)
    assert result['gross_loss'] == expected['gross_loss']
    assert result['transferred_loss'] == expected['transferred_loss']
    assert result['retained_loss'] == expected['retained_loss']

def test_aggregate_losses_mixed_values():
    df = pd.DataFrame({'gross_loss': [-100, 200, 300], 'transferred_loss': [50, -100, 150], 'retained_loss': [-150, 300, 150]})
    expected = {'gross_loss': 400.0, 'transferred_loss': 100.0, 'retained_loss': 300.0}
    result = aggregate_losses(df)
    assert result['gross_loss'] == expected['gross_loss']
    assert result['transferred_loss'] == expected['transferred_loss']
    assert result['retained_loss'] == expected['retained_loss']

def test_aggregate_losses_single_row():
    df = pd.DataFrame({'gross_loss': [100], 'transferred_loss': [50], 'retained_loss': [50]})
    expected = {'gross_loss': 100.0, 'transferred_loss': 50.0, 'retained_loss': 50.0}
    result = aggregate_losses(df)
    assert result['gross_loss'] == expected['gross_loss']
    assert result['transferred_loss'] == expected['transferred_loss']
    assert result['retained_loss'] == expected['retained_loss']
