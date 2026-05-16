import matplotlib.pyplot as plt
import pytest
from typst import TypstError

from mplty import ax_typst


SIMPLE_MARKUP = "#text(fill: red)[hello]"


def test_ax_typst_adds_artist_to_given_ax():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])

    before = len(ax.artists) + len(ax.get_children())
    ax_typst(1.5, 2, SIMPLE_MARKUP, ax=ax)
    after = len(ax.artists) + len(ax.get_children())

    assert after > before
    plt.close(fig)


def test_ax_typst_uses_current_axes_when_ax_is_none():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])

    ax_typst(1.5, 2, SIMPLE_MARKUP)

    assert plt.gca() is ax
    plt.close(fig)


def test_ax_typst_accepts_scale():
    fig, ax = plt.subplots()
    ax_typst(0.5, 0.5, SIMPLE_MARKUP, ax=ax, scale=2.0)
    plt.close(fig)


def test_ax_typst_with_page_rule_disabled():
    fig, ax = plt.subplots()
    ax_typst(0.5, 0.5, SIMPLE_MARKUP, ax=ax, page_rule=None)
    plt.close(fig)


def test_ax_typst_invalid_markup_raises():
    fig, ax = plt.subplots()
    with pytest.raises(TypstError):
        ax_typst(0.5, 0.5, "#this is not valid typst {{{", ax=ax)
    plt.close(fig)
