import altair as alt
import pandas as pd


def get_limit_tuple(series):
    lim = (series.min(), series.max())
    return lim


def scatterplot(x, y, data, hue=None, xlim=None, ylim=None):
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
