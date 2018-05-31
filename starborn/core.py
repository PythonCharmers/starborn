import altair as alt
import pandas as pd


def get_limit_tuple(series):
    lim = (series.min(), series.max())
    return lim


def scatterplot(x, y, data, hue=None, xlim=None, ylim=None):
    # TODO: refactor so it uses category_chart_kwargs?
    if xlim is None:
        xlim = get_limit_tuple(data[x])
    if ylim is None:
        ylim = get_limit_tuple(data[y])
    xscale = alt.Scale(domain=xlim)
    yscale = alt.Scale(domain=ylim)
    
    other_args = {'color': '{hue}:N'.format(hue=hue)} if hue else {}
    points = alt.Chart(data).mark_circle().encode(
        alt.X(x, scale=xscale),
        alt.Y(y, scale=yscale),
        **other_args
    )
    return points


def jointplot(x, y, data, kind='scatter', hue=None, xlim=None, ylim=None):
    if xlim is None:
        xlim = get_limit_tuple(data[x])
    if ylim is None:
        ylim = get_limit_tuple(data[y])
    xscale = alt.Scale(domain=xlim)
    yscale = alt.Scale(domain=ylim)
 
    points = scatterplot(x, y, data, hue=hue, xlim=xlim, ylim=ylim)

    area_args = {'opacity': .3, 'interpolate': 'step'}

    blank_axis = alt.Axis(title='')

    top_hist = alt.Chart(data).mark_area(**area_args).encode(
        alt.X('{x}:Q'.format(x=x),
              # when using bins, the axis scale is set through
              # the bin extent, so we do not specify the scale here
              # (which would be ignored anyway)
              bin=alt.Bin(maxbins=20, extent=xscale.domain),
              stack=None,
              axis=blank_axis,
             ),
        alt.Y('count()', stack=None, axis=blank_axis),
        alt.Color('{hue}:N'.format(hue=hue)),
    ).properties(height=60)

    right_hist = alt.Chart(data).mark_area(**area_args).encode(
        alt.Y('{y}:Q'.format(y=y),
              bin=alt.Bin(maxbins=20, extent=yscale.domain),
              stack=None,
              axis=blank_axis,
             ),
        alt.X('count()', stack=None, axis=blank_axis),
        alt.Color('{hue}:N'.format(hue=hue)),
    ).properties(width=60)

    return top_hist & (points | right_hist)


def heatmap(data, vmin=None, vmax=None, annot=None, fmt='.2g'):

    # We always want to have a DataFrame with semantic information
    if not isinstance(data, pd.DataFrame):
        matrix = np.asarray(data)
        data = pd.DataFrame(matrix)

    melted = data.stack().reset_index(name='Value')

    x = data.columns.name
    y = data.index.name

    heatmap = alt.Chart(melted).mark_rect().encode(
        alt.X('{x}:O'.format(x=x), scale=alt.Scale(paddingInner=0)),
        alt.Y('{y}:O'.format(y=y), scale=alt.Scale(paddingInner=0)),
        color='Value:Q'
    )
    
    if not annot:
        return heatmap

    # Overlay text
    text = alt.Chart(melted).mark_text(baseline='middle').encode(
        x='{x}:O'.format(x=x),
        y='{y}:O'.format(y=y),
        text=alt.Text('Value', format=fmt),
        color=alt.condition(alt.expr.datum['Value'] > 70,
                            alt.value('black'),
                            alt.value('white'))
    )
    return heatmap + text


def stripplot(x=None, y=None, hue=None, data=None):
    # TODO: refactor so it uses category_chart_kwargs()
    if data is None:
        if y is None:
            data = x.to_frame()
            x = data.columns[0]
        elif x is None:
            data = y.to_frame()
            y = data.columns[0]
        else:
            raise RuntimeError('not supported yet ...')

    kwargs = {}
    if x is not None:
        kwargs['x'] = '{x}'.format(x=x)
    if y is not None:
        kwargs['y'] = '{y}'.format(y=y)
    if hue is not None:
        kwargs['color'] = hue

    chart = alt.Chart(data).mark_tick().encode(**kwargs)
    return chart


def pairplot(data, hue=None, vars=None):
    if vars is None:
        vars = list(data.columns)

    chart = alt.Chart(data).mark_circle().encode(
                alt.X(alt.repeat("column"), type='quantitative'),
                alt.Y(alt.repeat("row"), type='quantitative'),
                color='{hue}:N'.format(hue=hue)
            ).properties(
                width=250,
                height=250
            ).repeat(
                row=vars,
                column=vars
            )
    return chart


def category_chart_kwargs(x=None, y=None, hue=None, data=None, order=None, orient=None, hue_order=None, estimator='mean'):
    """
    Somewhat similar to the `establish_variables()` method in Seaborn's
    `_CategoricalPlotter` class.

    Return value
    ============
    a dictionary of kwargs for encoding the Altair chart
    """

    if data is None:
        if y is None:
            data = x.to_frame()
            x = data.columns[0]
        elif x is None:
            data = y.to_frame()
            y = data.columns[0]
        else:
            raise RuntimeError('not supported yet ...')

    kwargs = {}

    # TODO: infer the orientation automatically:
    if orient is None:
        orient = 'v'

    if orient == 'v':
        if x is not None:
            kwargs['x'] = '{x}'.format(x=x)
        if y is not None:
            kwargs['y'] = '{estimator}({y})'.format(estimator=estimator, y=y)
    else:
        if x is not None:
            kwargs['x'] = '{estimator}({x})'.format(estimator=estimator, x=x)
        if y is not None:
            kwargs['y'] = '{y}'.format(y=y)

    if hue is not None:
        if orient == 'h':
            kwargs['row'] = kwargs['y']
            kwargs['y'] = hue
        elif orient == 'v':
            kwargs['column'] = kwargs['x']
            kwargs['x'] = hue
        kwargs['color'] = hue

    empty_axis=alt.Axis(domain=False, labels=False, title='', ticks=False) #, offset=-12, zindex=1)

    axis_kwargs = {}
    if hue is None:
        axis_kwargs['sort'] = order
    else:
        if hue_order is not None:
            axis_kwargs['sort'] = hue_order
        axis_kwargs['axis'] = empty_axis
    
    if orient == 'v':
        x = alt.X(kwargs['x'], **axis_kwargs)
        kwargs['x'] = x
    else:
        y = alt.Y(kwargs['y'], **axis_kwargs)
        kwargs['y'] = y

    if hue is not None:
        if order is not None:
            raise ValueError('custom order is not implemented for grouped bar charts (when `hue` is not `None`). Vega-Lite current does not support sorting of facets ...')
        if orient == 'v':
            column = alt.Column(kwargs['column']) #, axis=alt.Axis(orient='bottom'))
            kwargs['column'] = column
        else:
            row = alt.Row(kwargs['row']) #, axis=alt.Axis(orient='left'), sort=order)
            kwargs['row'] = row

    return kwargs


def barplot(x=None, y=None, hue=None, data=None, order=None, orient=None, hue_order=None):
    kwargs = category_chart_kwargs(x=x, y=y, hue=hue, data=data, order=order, orient=orient, hue_order=hue_order)

    chart = alt.Chart(data).mark_bar().encode(**kwargs)
    return chart


def boxplot(x=None, y=None, hue=None, data=None, order=None, orient=None):
    # TODO: refactor so it uses category_chart_kwargs

    # TODO: infer the orientation automatically:
    if orient is None or orient == 'v':
        return boxplot_vertical(x=x, y=y, hue=hue, data=data, order=order)
    else:
        return boxplot_horizontal(x=x, y=y, hue=hue, data=data, order=order)


def boxplot_vertical(x=None, y=None, hue=None, data=None, order=None):

    # orientation_mapper = {'v': {'x': 'x', 'y': 'y'},
    #                       'h': {'x': 'y', 'y': 'x'}}

    # Define aggregate fields
    lower_box = 'q1({value}):Q'.format(value=y)
    lower_whisker = 'min({value}):Q'.format(value=y)
    upper_box = 'q3({value}):Q'.format(value=y)
    upper_whisker = 'max({value}):Q'.format(value=y)
    
    kwargs = {'x': '{x}:O'.format(x=x)}

    if hue is not None:
        kwargs['color'] = '{hue}:N'.format(hue=hue)
        # Swap x for column
        column, kwargs['x'] = kwargs['x'], '{hue}:N'.format(hue=hue)

    base = alt.Chart().encode(
        **kwargs
    )

    # Compose each layer individually
    lower_whisker = base.mark_rule().encode(
        y=alt.Y(lower_whisker, axis=alt.Axis(title=y)),
        y2=lower_box,
    )
    
    middle_bar_kwargs = dict(
        y=lower_box,
        y2=upper_box,
    )
    if hue is None:
        middle_bar_kwargs['color'] = 'year:O'

    middle_bar = base.mark_bar(size=10.0).encode(**middle_bar_kwargs)

    upper_whisker = base.mark_rule().encode(
        y=upper_whisker,
        y2=upper_box,
    )
    
    middle_tick = base.mark_tick(
        color='white',
        size=10.0
    ).encode(
        y='median({value}):Q'.format(value=y),
    )
    
    chart = (lower_whisker + upper_whisker + middle_bar + middle_tick)

    if hue is None:
        chart.data = data
        return chart
    else:
        return chart.facet(column=column, data=data)


def violinplot(x=None, y=None, data=None, orient=None):
    # TODO: automatically infer orientation

    if orient is None or orient == 'v':
        kwargs = dict(
                    x=alt.X('count(*):Q',
                            axis=alt.Axis(grid=False, labels=False),
                            stack='center',
                            title=''),
                    y=alt.Y('{y}:Q'.format(y=y), bin=alt.Bin(maxbins=100)),
                    column='{x}:N'.format(x=x),
                    color='{x}:N'.format(x=x)
        )
    else:
        kwargs = dict(
                    y=alt.Y('count(*):Q',
                            axis=alt.Axis(grid=False, labels=False),
                            stack='center',
                            title=''),
                    x=alt.X('{x}:Q'.format(x=x), bin=alt.Bin(maxbins=100)),
                    row='{y}:N'.format(y=y),
                    color='{y}:N'.format(y=y)
        )
    chart = alt.Chart(data).mark_area().encode(**kwargs)
    return chart

