import base64
import logging
from collections import OrderedDict
from operator import itemgetter

import werkzeug
from dateutil.relativedelta import relativedelta
from dateutil.utils import today

from odoo import _, api, fields, models, tools
import odoo.http as http
from odoo.http import request
from odoo.osv.expression import AND
from odoo.tools import date_utils


def portal_pager(url, url_args, total, page, step):
    pass


def groupbyelem(locations, param):
    pass


@http.route(['/location', '/location/page/<int:page>'], type='http', auth="user", website=True)
def portal_location(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby='project',
                         **kw):
    location_sudo = request.env['account.analytic.line'].sudo()
    values = self._prepare_portal_layout_values()
    domain = request.env['account.analytic.line']._location_get_portal_domain()

    searchbar_sortings = {
        'date': {'label': _('Newest'), 'order': 'date desc'},
        'name': {'label': _('Name'), 'order': 'name'},
    }

    searchbar_inputs = {
        'all': {'input': 'all', 'label': _('Search in All')},
    }

    searchbar_groupby = {
        'none': {'input': 'none', 'label': _('None')},
        'project': {'input': 'project', 'label': _('Project')},
    }

    searchbar_filters = {
        'all': {'label': _('All'), 'domain': []},
        'today': {'label': _('Today'), 'domain': [("date", "=", today)]},

    }
    # default sort by value
    if not sortby:
        sortby = 'date'
    order = searchbar_sortings[sortby]['order']
    # default filter by value
    if not filterby:
        filterby = 'all'
    domain = AND([domain, searchbar_filters[filterby]['domain']])

    if search and search_in:
        domain = AND([domain, [('name', 'ilike', search)]])

    location_count = location_sudo.search_count(domain)
    # pager
    pager = portal_pager(
        url="/location",
        url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'filterby': filterby},
        total=location_count,
        page=page,
        step=self._items_per_page
    )

    if groupby == 'project':
        order = "project_id, %s" % order
    locations = location_sudo.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
    if groupby == 'project':
        grouped_locations = [location_sudo.concat(*g) for k, g in groupbyelem(locations, itemgetter('project_id'))]
    else:
        grouped_locations = [locations]

    values.update({
        'locations': locations,
        'grouped_locations': grouped_locations,
        'page_name': 'location',
        'default_url': 'locations',
        'pager': pager,
        'searchbar_sortings': searchbar_sortings,
        'search_in': search_in,
        'sortby': sortby,
        'groupby': groupby,
        'searchbar_inputs': searchbar_inputs,
        'searchbar_groupby': searchbar_groupby,
        'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
        'filterby': filterby,
    })
    return request.render("hr_location.portal_my_locations", values)