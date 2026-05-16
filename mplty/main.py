import typst
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional


def ax_typst(
    x,
    y,
    markup,
    ax=None,
    scale=1,
    page_rule='#set page(width: auto, height: auto, margin: 0pt, fill: rgb("#00000000"))',
    ppi=300,
    typst_kwargs: Optional[dict] = None,
):
    """
    Render Typst markup and place it on a matplotlib Axes.

    The markup preserves its original aspect ratio without distortion
    from data-coordinate scaling.

    Parameters
    ----------
    x : float
        X coordinate in data space.

    y : float
        Y coordinate in data space.

    markup : str
        Typst markup to render.

    ax : matplotlib.axes.Axes, optional
        Target axes. Defaults to the current axes.

    scale : float, default=1
        Scaling factor applied to the rendered Typst content.

    page_rule : str or None, optional
        Typst page configuration prepended to `markup` before compilation.
        Set to ``None`` to disable automatic page configuration.

    ppi : int
        Pixel per inches for Typst markup. Higher values mean better quality
        but may be slower to compile.

    kwargs : dict
        Additional arguments passed to `typst.compile()`.

    Returns
    -------
    matplotlib.offsetbox.AnnotationBbox
        The created annotation artist.

    Examples
    --------
    >>> ax_typst(1.5, 2, "#text(fill: red)[Hello *from* Typst!]")

    Notes
    -----
    The Typst content is rasterized to PNG before insertion into the figure.
    """
    if ax is None:
        ax = plt.gca()

    if typst_kwargs is None:
        typst_kwargs = dict()

    with TemporaryDirectory() as tmp:
        typst_file = Path(tmp) / "input.typ"
        output_file = Path(tmp) / "output.png"

        if page_rule:
            markup = f"{page_rule}\n{markup}"
        typst_file.write_text(markup, encoding="utf-8")

        typst.compile(str(typst_file), output=str(output_file), ppi=ppi, **typst_kwargs)

        img = mpimg.imread(output_file)

    imagebox = OffsetImage(img, zoom=scale / 3)
    ab = AnnotationBbox(imagebox, (x, y), frameon=False, box_alignment=(0, 0))

    ax.add_artist(ab)
