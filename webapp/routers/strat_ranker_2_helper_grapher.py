import pandas as pd
import plotly.express as px
from webapp.routers.strat_ranker_2_helper_cols import scattercols, profilecols, abovecols
from formatting import formatting_schema

figure_layout_mastertemplate = formatting_schema['figure_layout_mastertemplate']


class StratRankerGrapher:
    def _format_fig(self, fig, hovermode):
        fig.update_xaxes(categoryorder='category ascending', ticklabeloverflow='allow', automargin=False)
        fig.update_layout(legend_title_text='Legend', hovermode=hovermode)

    def _prep_bdf(self, bdf, mode):
        colnames = ['stratipcode']
        if mode == 'scatter':
            colnames.extend([i for i in bdf.columns if i.startswith('WLP') or i in scattercols])
            # scattercols.extend([i for i in bdf.columns if i.startswith('WLP')])
        if mode == 'profile':
            colnames.extend([i for i in bdf.columns if i in profilecols])
        if mode == 'above':
            colnames.extend([i for i in bdf.columns if i in abovecols])
        return bdf[colnames].copy()

    def gen_rank_fig(self, bdf, chart_type, hovermode):
        bdf = self._prep_bdf(bdf, 'scatter')
        df = pd.melt(bdf, id_vars="stratipcode", value_vars=bdf.columns[1:], var_name='metric', value_name='value')
        if chart_type == 'Scatter':
            fig = px.scatter(df, x="stratipcode", y="value", color="metric", template=figure_layout_mastertemplate)
            fig.update_traces(marker=dict(size=12, opacity=0.5))
        elif chart_type == 'Box':
            fig = px.box(df, x="stratipcode", y="value", color="metric", boxmode="overlay", template=figure_layout_mastertemplate)
        elif chart_type == 'Violin':
            fig = px.violin(df, x="stratipcode", y="value", color="metric", violinmode="overlay", template=figure_layout_mastertemplate)
        fig.update_yaxes(matches=None)
        fig.add_hline(
            y=0,
            line_dash="solid",
            line_color="grey",
            line_width=2.5)
        self._format_fig(fig, hovermode)
        return fig

    def gen_prof_fig(self, bdf, hovermode):
        bdf = self._prep_bdf(bdf, 'profile')
        bdf['sample size'] = bdf['stratipcode'].apply(lambda x: bdf[bdf['stratipcode'] == x]['stratipcode'].count())
        bdf = bdf.groupby(by=["stratipcode"], dropna=False, as_index=False).mean(numeric_only=True)
        bar_y = bdf.columns[1:]
        bar_x = 'stratipcode'
        fig = px.bar(bdf, x=bar_x, y=bar_y, barmode='group', template=figure_layout_mastertemplate)
        self._format_fig(fig, hovermode)
        return fig

    def gen_above_fig(self, bdf, hovermode):
        bdf = self._prep_bdf(bdf, 'above')
        bdf = bdf.groupby(by=["stratipcode"], dropna=False, as_index=False).mean(numeric_only=True)
        bar_y = bdf.columns[1:]
        bar_x = 'stratipcode'
        fig = px.bar(bdf, x=bar_x, y=bar_y, barmode='group', template=figure_layout_mastertemplate)
        self._format_fig(fig, hovermode)
        return fig
