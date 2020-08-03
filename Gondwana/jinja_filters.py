# add jinja2 filter as blueprint
# https://stackoverflow.com/questions/12288454/how-to-import-custom-jinja2-filters-from-another-file-and-using-flask
import jinja2
import flask

bp = flask.Blueprint('fitlers', __name__)

@jinja2.contextfilter
@bp.app_template_filter('order_status_2_name')
def order_status_2_name(context, value):
    s_2_n = {
            'P':'Processed',
            'C':'Complete',
            'O':'Open',
            'F':'Failed',
            'D':'Declined',
            'B':'Backordered',
            'I':'Canceled',
            'Y':'Awaiting call',
            'A':'Shipped',
            'E':'Out of stock',
            # custom order status
            'J':'Awaiting Fullfillment',
            'H':'Partially Refunded',
            'G':'Refunded',
    }

    return s_2_n.get(value, value)

@jinja2.contextfilter
@bp.app_template_filter('format_datetime')
def format_datetime(context, value, format='yyyy-mm-dd'):
    if format == 'yyyy-mm-dd':
        return value.strftime('%Y-%m-%d')

    return value
