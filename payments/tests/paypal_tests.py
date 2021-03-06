#!/usr/bin/python
import numpy as np
import pandas as pd
import pytest

from NGS2apis.payments.paypal import *


@pytest.mark.parametrize('test', [
    (pd.DataFrame({
        'batch_id': ['A'],
        'first_name': ['holder'],
        'receiver_email': ['test@test.com'],
        'value': [.11],
        'currency': ['USD'],
        'item_id': ['A1'],
        'processed_code': ['s0meth|ng'],
    })),
])
def test_data_struture_test_pass(test):
    assert data_structure_test(test) == None


@pytest.mark.parametrize('test', [
    (pd.DataFrame({
        'batch_id': ['A'],
        'first_name': ['holder'],
        'receiver_email': ['test@test.com'],
        'value': [.11],
        'item_id': ['A1'],
        'processed_code': ['s0meth|ng'],
        'extra_col': [None],
    })),
])
@pytest.mark.xfail(raises=AssertionError)
def test_data_structure_test_fail(test):
    assert data_structure_test(test)


@pytest.mark.parametrize('test', [
    (pd.DataFrame({'batch_id': ['A', 'A', 'B']})),
])
def test_batch_size_test_pass(test):
    assert batch_size_test(test) == None


@pytest.mark.parametrize('test', [
    (pd.DataFrame({'batch_id': np.repeat('long', 251)})),
])
@pytest.mark.xfail(raises=AssertionError)
def test_batch_size_test_fail(test):
    assert batch_size_test(test)


@pytest.mark.parametrize('test, expected', [
    (pd.DataFrame({'first_name': ['mark', 'LIZ']}), ('Mark', 'Liz')),
    (pd.DataFrame({'first_name': ['Mark', 'liz']}), ('Mark', 'Liz')),
    (pd.DataFrame({'first_name': ['MARK', 'Liz']}), ('Mark', 'Liz')),
])
def test_check_name_test_pass(test, expected):
    result = check_name_test(test)
    assert result[0] == expected[0]
    assert result[1] == expected[1]


@pytest.mark.parametrize('test', [
    (pd.DataFrame({'first_name': ['Mark', np.nan, 'Liz']})),
])
@pytest.mark.xfail(raises=AssertionError)
def test_check_name_test_test_fail(test):
    assert check_name_test(test)


@pytest.mark.parametrize('test, expected', [
    (pd.DataFrame({'currency': ['USD', 'PHP']}), ('USD', 'PHP')),
    (pd.DataFrame({'currency': ['Usd', 'pHP']}), ('USD', 'PHP')),
    (pd.DataFrame({'currency': ['usd', 'php']}), ('USD', 'PHP')),
])
def test_currency_type_test_pass(test, expected):
    result = currency_type_test(test)
    assert result[0] == expected[0]
    assert result[1] == expected[1]


@pytest.mark.parametrize('test', [
    (pd.DataFrame({'currency': ['USD', 'US', 'AUD']})),
])
@pytest.mark.xfail(raises=AssertionError)
def test_currency_type_test_fail(test):
    assert currency_type_test(test)


@pytest.mark.parametrize('test', [
    (pd.DataFrame({
        'receiver_email': ['this@g.com', 'that@help.edu', '112@test.org']
    })),
])
def test_email_formation_test_pass(test):
    assert email_formation_test(test) == None


@pytest.mark.parametrize('test', [
    (pd.DataFrame({
        'receiver_email': ['112@help', 'this@good.com', 'that#fail.org']
    })),
])
@pytest.mark.xfail(raises=AssertionError)
def test_email_formation_test_fail(test):
    assert email_formation_test(test)


@pytest.mark.parametrize('test', [
    (pd.DataFrame({
        'batch_id': ['A', 'A', 'B'],
        'item_id': [1, 2, 1],
    })),
])
def test_unique_transaction_ids_test_pass(test):
    assert unique_transaction_ids_test(test) == None


@pytest.mark.parametrize('test', [
    (pd.DataFrame({
        'batch_id': ['A', 'A', 'B'],
        'item_id': [1, 1, 1],
    })),
])
@pytest.mark.xfail(raises=AssertionError)
def test_unique_transaction_ids_test_fail(test):
    assert unique_transaction_ids_test(test)


@pytest.mark.parametrize('test', [
    (pd.DataFrame({'value': [1, .99, 2.3, 14]})),
])
def test_values_numeric_test_pass(test):
    assert values_numeric_test(test) == None


@pytest.mark.parametrize('test', [
    (pd.DataFrame({'value': ['1', '1.99', 2.3, 14]})),
])
@pytest.mark.xfail(raises=AssertionError)
def test_values_numeric_test_fail(test):
    assert values_numeric_test(test)


@pytest.mark.parametrize('test, expected', [
    (pd.DataFrame({
        'first_name': ['Fe'],
        'value': [1],
        'currency': ['USD'],
        'receiver_email': ['this@test.com'],
        'item_id': ['A'],
    }), ('Fe', '1.00', 'USD', 'this@test.com', 'A')),
    (pd.DataFrame({
        'first_name': ['Fi'],
        'value': [199.34],
        'currency': ['PHP'],
        'receiver_email': ['that@test.org'],
        'item_id': ['B'],
    }), ('Fi', '199.34', 'PHP', 'that@test.org', 'B')),
    (pd.DataFrame({
        'first_name': ['Fo'],
        'value': [.5],
        'currency': ['USD'],
        'receiver_email': ['t@t.edu'],
        'item_id': ['C'],
    }), ('Fo', '0.50', 'USD', 't@t.edu', 'C')),
])
def test_build_payout(test, expected):
    result = build_payout(test)
    assert expected[0] in result[0]['note']
    assert result[0]['amount']['value'] == expected[1]
    assert result[0]['amount']['currency'] == expected[2]
    assert result[0]['receiver'] == expected[3]
    assert result[0]['sender_item_id'] == expected[4]
