# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from Modules.metriclibrary.STRATTEST_FUNCBASE_MMBM import unifatshell_single, dropmag_single, dropprev_single, dropscore_single


class VolStatProfile:
    def __init__(self, stock):
        self.volstatprofile = [
            {
                'metricname': 'fatscore_baremaxtoraw',
                'metricfunc': unifatshell_single,
                'metricparams': {
                    'prices': None,
                    'idealcol': f'{stock}_baremax',
                    'focuscol': stock,
                    'stat_type': 'avg'
                },
                'calibration': ['baremaxraw']
            },
            {
                'metricname': 'fatscore_baremaxtobaremin',
                'metricfunc': unifatshell_single,
                'metricparams': {
                    'prices': None,
                    'idealcol': f'{stock}_baremax',
                    'focuscol': f'{stock}_oldbareminraw',
                    'stat_type': 'avg'
                },
                'calibration': ['oldbareminraw', 'baremaxraw']
            },
            {
                'metricname': 'drop_mag',
                'metricfunc': dropmag_single,
                'metricparams': {
                    'prices': None,
                    'uppercol': f'{stock}_baremax',
                    'lowercol': stock,
                    'stat_type': 'avg'
                },
                'calibration': ['baremaxraw']
            },
            {
                'metricname': 'drop_prev',
                'metricfunc': dropprev_single,
                'metricparams': {
                    'prices': None,
                    'uppercol': f'{stock}_baremax',
                    'lowercol': stock
                },
                'calibration': ['baremaxraw']
            },
            {
                'metricname': 'dropscore',
                'metricfunc': dropscore_single,
                'metricparams': {
                    'prices': None,
                    'uppercol': f'{stock}_baremax',
                    'lowercol': stock,
                    'stat_type': 'avg'
                },
                'calibration': ['baremaxraw']
            }
        ]
