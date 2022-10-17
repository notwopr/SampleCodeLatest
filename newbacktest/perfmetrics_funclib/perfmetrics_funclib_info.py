from Modules.dates import DateOperations
from newbacktest.symbology.sampcode import SampCode
from newbacktest.symbology.investplancode import InvestPlanCode


def portsize(sampcode):
    return InvestPlanCode().decode((SampCode().decode(sampcode)['ipcode']))['portsize']


def periodlen(sampcode):
    return InvestPlanCode().decode((SampCode().decode(sampcode)['ipcode']))['periodlen']


def batchstart(sampcode):
    return InvestPlanCode().decode((SampCode().decode(sampcode)['ipcode']))['batchstart']


def batchend(sampcode):
    return batchstart(sampcode) + portsize(sampcode) - 1


def invest_startdate(sampcode):
    return SampCode().decode(sampcode)['invest_startdate']


def invest_enddate(sampcode):
    return DateOperations().plusminusdays(invest_startdate(sampcode), periodlen(sampcode))


def stratipcode(sampcode):
    return SampCode().decode(sampcode)['stratipcode']
