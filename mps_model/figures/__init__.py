"""Charts and maps, drawn from the tables in a results folder.

Each module draws one or a few related figures and reads only result tables and data files, so the
figures can be redrawn without re-running the model: `python -m mps_model figures`.
"""
from . import basemaps, capacity, deck, glide_path, kenwood, levers, maps, recruit_value, savings
from .style import plt


def draw_all(results, assumptions, deck_images=False, log=print):
    results.create()
    log("Drawing figures")
    steps = [
        lambda: basemaps.build_basemaps(results),
        lambda: savings.draw(results, assumptions),                   # fig1, fig1b, fig2
        lambda: maps.draw(results),                       # fig3, fig4, fig5, fig8, figA1-A3
        lambda: levers.draw(results, assumptions),        # fig6, fig7
        lambda: kenwood.draw(results),                    # fig9
        lambda: glide_path.draw(results),                 # fig10
        lambda: capacity.draw(results),                   # fig11
        lambda: recruit_value.draw(results, assumptions),  # fig12
    ]
    if deck_images:
        steps.append(lambda: deck.draw(results))
    for step in steps:
        with plt.rc_context():  # style changes made by one figure module do not leak into the next
            step()
