from datetime import date
import pytest
from model import Batch, OrderLine


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    large_batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    small_line = OrderLine("order-ref", "SMALL-TABLE", 2)

    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_equal_than_required():
    small_batch = Batch("batch-001", "SMALL-TABLE", qty=2, eta=date.today())
    large_line = OrderLine("order-ref", "SMALL-TABLE", 2)

    assert small_batch.can_allocate(large_line) is True


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch = Batch("batch-001", "SMALL-TABLE", qty=2, eta=date.today())
    large_line = OrderLine("order-ref", "SMALL-TABLE", 10)

    assert small_batch.can_allocate(large_line) is False


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "SMALL-TABLE", qty=2, eta=date.today())
    different_line = OrderLine("order-ref", "BIG-TABLE", 10)

    assert batch.can_allocate(different_line) is False


def test_can_only_deallocate_allocated_lines():
    batch = Batch("batch-001", "SMALL-TABLE", 20, eta=date.today())
    unallocated_line = OrderLine("order-ref", "SMALL-TABLE", 10)

    batch.deallocate(unallocated_line)

    assert batch.available_quantity == 20
