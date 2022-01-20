"""
Return strings to build an instance template
"""
from datetime import timedelta, datetime
from random import randint, choice, uniform, randrange
from xml.sax.saxutils import escape
from decimal import Decimal, BasicContext, setcontext

# from django.contrib import messages

import exrex


def get_latlon():
    latlon = [0, 0]
    latlon[0] = str(float(Decimal(randrange(-90, 90))))
    latlon[1] = str(float(Decimal(randrange(-180, 180))))
    return(latlon)


def random_dtstr(start=None, end=None):
    if not start:
        start = datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')

    if not end:
        end = datetime.strptime('2015-12-31', '%Y-%m-%d')
    rand_dts = datetime.strftime(
        start + timedelta(seconds=randint(0, int((end - start).total_seconds()))), '%Y-%m-%dT%H:%M:%S')
    return rand_dts


def Xd_boolean(xd, indent):
    choices = []
    for c in xd.trues.splitlines():
        choices.append(c)

    bool_xd = choice(choices)

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    tr = random_dtstr()

    indent += '  '
    elstr = indent + """<s3m:ms-""" + str(xd.ct_id) + """>\n"""
    elstr += indent + """  <label>""" + escape(xd.label.strip()) + """</label>\n"""
    if xd.require_vtb:
        elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    if xd.require_vte:
        elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if xd.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if xd.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if xd.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""
    elstr += indent + """  <true-value>""" + bool_xd + """</true-value>\n"""
    elstr += indent + """</s3m:ms-""" + str(xd.ct_id) + """>\n"""

    return elstr


def Xd_link(xd, indent, pcs=True):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    tr = random_dtstr()

    elstr = ''
    indent += '  '
    if pcs:
        elstr += indent + """<s3m:ms-""" + str(xd.ct_id) + """>\n"""
    elstr += indent + """  <label>""" + escape(xd.label.strip()) + """</label>\n"""

    if xd.require_vtb:
        elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    if xd.require_vte:
        elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if xd.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if xd.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if xd.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""

    elstr += indent + """  <link>https://Infotropictools.com</link>\n"""
    elstr += indent + """  <relation>""" + escape(xd.relation.strip()) + """</relation>\n"""
    elstr += indent + """  <relation-uri>""" + escape(xd.relation_uri.strip()) + """</relation-uri>\n"""
    if pcs:
        elstr += indent + """</s3m:ms-""" + str(xd.ct_id) + """>\n"""

    return elstr


def Xd_string(xd, indent, pcs=True):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    tr = random_dtstr()

    if xd.def_val:
        s = xd.def_val
    elif xd.enums:
        enum_list = []
        for e in xd.enums.splitlines():
            enum_list.append(escape(e))
        s = choice(enum_list)
    else:
        s = 'DefaultString'

    elstr = ''
    indent += '  '
    if pcs:
        elstr += indent + """<s3m:ms-""" + str(xd.ct_id) + """>\n"""
    elstr += indent + """  <label>""" + escape(xd.label.strip()) + """</label>\n"""

    if xd.require_vtb:
        elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    if xd.require_vte:
        elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if xd.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if xd.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if xd.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""

    elstr += indent + """  <xdstring-value>""" + s.strip() + """</xdstring-value>\n"""
    elstr += indent + """  <xdstring-language>""" + xd.lang + """</xdstring-language>\n"""
    if pcs:
        elstr += indent + """</s3m:ms-""" + str(xd.ct_id) + """>\n"""

    return elstr


def Xd_count(xd, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    tr = random_dtstr()

    _min = None
    _max = None

    if xd.min_inclusive is not None:
        _min = xd.min_inclusive
    if xd.min_exclusive is not None:
        _min = xd.min_exclusive + 1
    if xd.max_inclusive is not None:
        _max = xd.max_inclusive
    if xd.max_exclusive is not None:
        _max = xd.max_exclusive - 1

    if _max is None:
        _max = 999999
    if _min is None:
        _min = -999999

    mag = randint(_min, _max)

    if xd.total_digits is not None:
        if len(str(mag)) > xd.total_digits:  # Opps!  Have to trim it down.
            mag = int(str(mag)[:xd.total_digits])

    indent += '  '
    elstr = indent + """<s3m:ms-""" + str(xd.ct_id) + """>\n"""
    elstr += indent + """  <label>""" + escape(xd.label.strip()) + """</label>\n"""

    if xd.require_vtb:
        elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    if xd.require_vte:
        elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if xd.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if xd.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if xd.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""

    if xd.reference_ranges:
        for rr in xd.reference_ranges.all():
            elstr += indent + referencerange(rr, indent)

    if xd.normal_status:
        elstr += indent + """  <normal-status>""" + escape(xd.normal_status.strip()) + """</normal-status>\n"""

    elstr += indent + """  <magnitude-status>equal</magnitude-status>\n"""
    elstr += indent + """  <error>0</error>\n"""
    elstr += indent + """  <accuracy>0</accuracy>\n"""
    elstr += indent + """  <xdcount-value>""" + str(mag) + """</xdcount-value>\n"""

    # select units
    enum_list = []
    for e in xd.units.enums.splitlines():
        enum_list.append(escape(e))
    unit = choice(enum_list)

    elstr += indent + """  <xdcount-units>\n"""
    elstr += indent + """    <label>""" + escape(xd.units.label.strip()) + """</label>\n"""
    if xd.units.require_vtb:
        elstr += indent + """    <vtb>""" + vtb + """</vtb>\n"""
    if xd.units.require_vte:
        elstr += indent + """    <vte>""" + vte + """</vte>\n"""
    if xd.units.require_tr:
        elstr += indent + """    <tr>""" + tr + """Z</tr>\n"""
    if xd.units.require_mod:
        elstr += indent + """    <modified>""" + tr + """Z</modified>\n"""

    elstr += indent + """    <xdstring-value>""" + unit + """</xdstring-value>\n"""

    elstr += indent + """  </xdcount-units>\n"""

    elstr += indent + """</s3m:ms-""" + str(xd.ct_id) + """>\n"""

    return elstr


def Xd_interval(xd, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    tr = random_dtstr()

    indent += '  '
    elstr = indent + """<interval>\n"""
    elstr += indent + """  <label>""" + \
        escape(xd.label.strip()) + """</label>\n"""

    if xd.require_vtb:
        elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    if xd.require_vte:
        elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if xd.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if xd.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if xd.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""

    elstr += indent + """  <lower>\n"""
    if xd.lower_bounded:
        elstr += indent + """    <invl-""" + xd.interval_type + """>""" + xd.lower + """</invl-""" + xd.interval_type + """>\n"""
    else:
        elstr += indent + """    <invl-""" + xd.interval_type + """ xsi:nil='true'/>\n"""
    elstr += indent + """  </lower>\n"""
    elstr += indent + """  <upper>\n"""
    if xd.upper_bounded:
        elstr += indent + """    <invl-""" + xd.interval_type + """>""" + xd.upper + """</invl-""" + xd.interval_type + """>\n"""
    else:
        elstr += indent + """    <invl-""" + xd.interval_type + """ xsi:nil='true'/>\n"""
    elstr += indent + """  </upper>\n"""

    if xd.lower_included:
        elstr += indent + """  <lower-included>true</lower-included>\n"""
    else:
        elstr += indent + """  <lower-included>false</lower-included>\n"""
    if xd.upper_included:
        elstr += indent + """  <upper-included>true</upper-included>\n"""
    else:
        elstr += indent + """  <upper-included>false</upper-included>\n"""

    if xd.lower_bounded:
        elstr += indent + """  <lower-bounded>true</lower-bounded>\n"""
    else:
        elstr += indent + """  <lower-bounded>false</lower-bounded>\n"""
    if xd.upper_bounded:
        elstr += indent + """  <upper-bounded>true</upper-bounded>\n"""
    else:
        elstr += indent + """  <upper-bounded>false</upper-bounded>\n"""

    if xd.units_name and xd.units_uri:
        elstr += indent + """  <interval-units>\n"""
        elstr += indent + """    <units-name>""" + xd.units_name.strip() + """</units-name>\n"""
        elstr += indent + """    <units-uri>""" + xd.units_uri.strip() + """</units-uri>\n"""
        elstr += indent + """  </interval-units>\n"""

    elstr += indent + """</interval>\n"""

    return elstr


def Xd_file(xd, indent, pcs=True):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    tr = random_dtstr()

    mt = None
    media_list = []
    if xd.media_type:
        for m in xd.media_type.splitlines():
            media_list.append(escape(m))
        mt = choice(media_list)

    elstr = ''
    indent += '  '
    if pcs:
        elstr += indent + """<s3m:ms-""" + str(xd.ct_id) + """>\n"""
    elstr += indent + """  <label>""" + escape(xd.label.strip()) + """</label>\n"""

    if xd.require_vtb:
        elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    if xd.require_vte:
        elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if xd.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if xd.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if xd.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""

    elstr += indent + """  <size>64536</size>\n"""
    elstr += indent + """  <encoding>utf-8</encoding>\n"""
    elstr += indent + """  <xdfile-language>""" + xd.lang + """</xdfile-language>\n"""

    if mt:
        elstr += indent + """  <media-type>""" + mt + """</media-type>\n"""
    else:
        if xd.content_mode == 'binary':
            elstr += indent + """  <media-type>png</media-type>\n"""
        elif xd.content_mode == 'text':
            elstr += indent + """  <media-type>text/plain</media-type>\n"""
        elif xd.content_mode == 'url':
            elstr += indent + """  <media-type>png</media-type>\n"""

    elstr += indent + """  <compression-type>gz</compression-type>\n"""
    elstr += indent + """  <hash-result>dshfsoud6y3rwpef838rhf983trgf9e93w8rytgf</hash-result>\n"""
    elstr += indent + """  <hash-function>MD5</hash-function>\n"""
    elstr += indent + """  <alt-txt>Fake entry data.</alt-txt>\n"""
    if xd.content_mode == 'binary':
        elstr += indent + """<media-content>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</media-content>\n"""
    elif xd.content_mode == 'text':
        elstr += indent + """<text-content>my sample text content</text-content>\n"""
    elif xd.content_mode == 'url':
        elstr += indent + """  <uri>http://www.mlhim.org/fake_media.png</uri>\n"""
    if pcs:
        elstr += indent + """</s3m:ms-""" + str(xd.ct_id) + """>\n"""

    return elstr


def Xd_ordinal(xd, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    tr = random_dtstr()

    o = []
    for a in xd.ordinals.splitlines():
        o.append(escape(a).strip())

    s = []
    for a in xd.symbols.splitlines():
        s.append(escape(a).strip())

    ri = randint(0, len(o) - 1)  # get a random index

    indent += '  '
    elstr = indent + """<s3m:ms-""" + str(xd.ct_id) + """>\n"""
    elstr += indent + """  <label>""" + escape(xd.label.strip()) + """</label>\n"""

    if xd.require_vtb:
        elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    if xd.require_vte:
        elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if xd.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if xd.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if xd.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""

    if xd.reference_ranges:
        for rr in xd.reference_ranges.all():
            elstr += indent + referencerange(rr, indent)
    if xd.normal_status:
        elstr += indent + """  <normal-status>""" + xd.normal_status.strip() + """</normal-status>\n"""
    elstr += indent + """  <ordinal>""" + o[ri] + """</ordinal>\n"""
    elstr += indent + """  <symbol>""" + s[ri] + """</symbol>\n"""
    elstr += indent + """</s3m:ms-""" + str(xd.ct_id) + """>\n"""

    return elstr


def Xd_quantity(xd, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    tr = random_dtstr()

    ctx = BasicContext
    setcontext(ctx)

    _min = None
    _max = None

    if xd.total_digits:  # total digits
        ctx.prec = xd.total_digits

    if xd.min_inclusive is not None:
        _min = xd.min_inclusive
    if xd.min_exclusive is not None:
        _min = xd.min_exclusive + 1

    if xd.max_inclusive is not None:
        _max = xd.max_inclusive
    if xd.max_exclusive is not None:
        _max = xd.max_exclusive - 1

    if _max is None:
        _max = 9999.0
    if _min is None:
        _min = 0.0

    _max = float(_max)
    _min = float(_min)

    mag = uniform(_min, _max)

    if xd.fraction_digits:
        if '.' in str(mag):
            fd = str(mag).split('.')[1]
            if len(fd) > xd.fraction_digits:
                fd = fd[0:xd.fraction_digits]
                mag = float(str(mag).split('.')[1] + '.' + fd)

    if xd.total_digits is not None:
        if len(str(mag)) > xd.total_digits:  # Opps!  Have to trim it down.
            mag = float(str(mag)[:xd.total_digits])

    indent += '  '
    elstr = indent + """<s3m:ms-""" + str(xd.ct_id) + """> \n"""
    elstr += indent + """  <label>""" + escape(xd.label.strip()) + """</label>\n"""

    if xd.require_vtb:
        elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    if xd.require_vte:
        elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if xd.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if xd.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if xd.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""

    if xd.reference_ranges:
        for rr in xd.reference_ranges.all():
            elstr += indent + referencerange(rr, indent)
    if xd.normal_status:
        elstr += indent + """  <normal-status>""" + xd.normal_status.strip() + """</normal-status>\n"""
    elstr += indent + """  <magnitude-status>equal</magnitude-status>\n"""
    elstr += indent + """  <error>0</error>\n"""
    elstr += indent + """  <accuracy>0</accuracy>\n"""
    elstr += indent + """    <xdquantity-value>""" + str(mag) + """</xdquantity-value>\n"""

    # select units
    enum_list = []
    for e in xd.units.enums.splitlines():
        enum_list.append(escape(e))
    unit = choice(enum_list)

    elstr += indent + """  <xdquantity-units>\n"""
    elstr += indent + """    <label>""" + escape(xd.units.label.strip()) + """</label>\n"""
    if xd.units.require_vtb:
        elstr += indent + """    <vtb>""" + vtb + """</vtb>\n"""
    if xd.units.require_vte:
        elstr += indent + """    <vte>""" + vte + """</vte>\n"""
    if xd.units.require_tr:
        elstr += indent + """    <tr>""" + tr + """Z</tr>\n"""
    if xd.units.require_mod:
        elstr += indent + """    <modified>""" + tr + """Z</modified>\n"""
    elstr += indent + """    <xdstring-value>""" + unit + """</xdstring-value>\n"""

    elstr += indent + """  </xdquantity-units>\n"""

    elstr += indent + """</s3m:ms-""" + str(xd.ct_id) + """>\n"""

    return elstr


def Xd_float(xd, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    tr = random_dtstr()

    ctx = BasicContext
    setcontext(ctx)

    _min = None
    _max = None

    if xd.total_digits:  # total digits
        ctx.prec = xd.total_digits

    if xd.min_inclusive is not None:
        _min = xd.min_inclusive
    if xd.min_exclusive is not None:
        _min = xd.min_exclusive + 1

    if xd.max_inclusive is not None:
        _max = xd.max_inclusive
    if xd.max_exclusive is not None:
        _max = xd.max_exclusive - 1

    if _max is None:
        _max = 9999.0
    if _min is None:
        _min = 0.0

    _max = float(_max)
    _min = float(_min)

    mag = uniform(_min, _max)

    if xd.total_digits is not None:
        if len(str(mag)) > xd.total_digits:  # Opps!  Have to trim it down.
            mag = float(str(mag)[:xd.total_digits])

    indent += '  '
    elstr = indent + """<s3m:ms-""" + str(xd.ct_id) + """> \n"""
    elstr += indent + """  <label>""" + escape(xd.label.strip()) + """</label>\n"""

    if xd.require_vtb:
        elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    if xd.require_vte:
        elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if xd.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if xd.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if xd.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""

    if xd.reference_ranges:
        for rr in xd.reference_ranges.all():
            elstr += indent + referencerange(rr, indent)
    if xd.normal_status:
        elstr += indent + """  <normal-status>""" + xd.normal_status.strip() + """</normal-status>\n"""
    elstr += indent + """  <magnitude-status>equal</magnitude-status>\n"""
    elstr += indent + """  <error>0</error>\n"""
    elstr += indent + """  <accuracy>0</accuracy>\n"""
    elstr += indent + """    <xdfloat-value>""" + str(mag) + """</xdfloat-value>\n"""

    # select units
    enum_list = []
    for e in xd.units.enums.splitlines():
        enum_list.append(escape(e))
    unit = choice(enum_list)

    elstr += indent + """  <xdfloat-units>\n"""
    elstr += indent + """    <label>""" + escape(xd.units.label.strip()) + """</label>\n"""
    if xd.units.require_vtb:
        elstr += indent + """    <vtb>""" + vtb + """</vtb>\n"""
    if xd.units.require_vte:
        elstr += indent + """    <vte>""" + vte + """</vte>\n"""
    if xd.units.require_tr:
        elstr += indent + """    <tr>""" + tr + """Z</tr>\n"""
    if xd.units.require_mod:
        elstr += indent + """    <modified>""" + tr + """Z</modified>\n"""
    elstr += indent + """    <xdstring-value>""" + unit + """</xdstring-value>\n"""

    elstr += indent + """  </xdfloat-units>\n"""

    elstr += indent + """</s3m:ms-""" + str(xd.ct_id) + """>\n"""

    return elstr


def Xd_ratio(xd, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    tr = random_dtstr()

    num_min = None
    num_max = None

    if xd.num_min_inclusive is not None:
        num_min = xd.num_min_inclusive
    if xd.num_min_exclusive is not None:
        num_min = xd.num_min_exclusive + 1
    if xd.num_max_inclusive is not None:
        num_max = xd.num_max_inclusive
    if xd.num_max_exclusive is not None:
        num_max = xd.max_exclusive - 1

    if num_max is None:
        num_max = 999999
    if num_min is None:
        num_min = -999999

    fnum_min = float(num_min)
    fnum_max = float(num_max)

    fnum = uniform(fnum_min, fnum_max)  # random float

    num = Decimal.from_float(fnum)

    den_min = None
    den_max = None

    if xd.den_min_inclusive is not None:
        den_min = xd.den_min_inclusive
    if xd.den_min_exclusive is not None:
        den_min = xd.den_min_exclusive + 1
    if xd.den_max_inclusive is not None:
        den_max = xd.den_max_inclusive
    if xd.den_max_exclusive is not None:
        den_max = xd.den_max_exclusive - 1

    if den_max is None:
        den_max = 999999
    if den_min is None:
        den_min = -999999

    fden_min = float(den_min)
    fden_max = float(den_max)

    fden = uniform(fden_min, fden_max)  # random float

    den = Decimal.from_float(fden)

    mag = num / den

    indent += '  '
    elstr = indent + """<s3m:ms-""" + str(xd.ct_id) + """>\n"""
    elstr += indent + """  <label>""" + escape(xd.label.strip()) + """</label>\n"""

    if xd.require_vtb:
        elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    if xd.require_vte:
        elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if xd.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if xd.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if xd.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""

    if xd.reference_ranges:
        for rr in xd.reference_ranges.all():
            elstr += indent + referencerange(rr, indent)
    if xd.normal_status:
        elstr += indent + """  <normal-status>""" + xd.normal_status.strip() + """</normal-status>\n"""
    elstr += indent + """  <magnitude-status>equal</magnitude-status>\n"""
    elstr += indent + """  <error>0</error>\n"""
    elstr += indent + """  <accuracy>0</accuracy>\n"""
    elstr += indent + """  <ratio-type>""" + xd.ratio_type + """</ratio-type>\n"""
    elstr += indent + """  <numerator>""" + str(num) + """</numerator>\n"""
    elstr += indent + """  <denominator>""" + str(den) + """</denominator>\n"""
    elstr += indent + """    <xdratio-value>""" + str(mag) + """</xdratio-value>\n"""
    if xd.num_units:
        for e in xd.num_units.enums.splitlines():
            enum_list.append(escape(e))
        unit = choice(enum_list)
        elstr += indent + """<numerator-units>\n<label>""" + escape(xd.num_units.label.strip()) + """</label>\n    <xdstring-value>""" + unit + """</xdstring-value>\n  </numerator-units>\n"""
    if xd.den_units:
        for e in xd.den_units.enums.splitlines():
            enum_list.append(escape(e))
        unit = choice(enum_list)
        elstr += indent + """<denominator-units>\n<label>""" + escape(xd.den_units.label.strip()) + """</label>\n    <xdstring-value>""" + unit + """</xdstring-value>\n  </denominator-units>\n"""
    if xd.ratio_units:
        for e in xd.ratio_units.enums.splitlines():
            enum_list.append(escape(e))
        unit = choice(enum_list)
        elstr += indent + """<ratio-units>\n<label>""" + escape(xd.ratio_units.label.strip()) + """</label>\n    <xdstring-value>""" + unit + """</xdstring-value>\n  </ratio-units>\n"""

    elstr += indent + """</s3m:ms-""" + str(xd.ct_id) + """>\n"""

    return elstr


def Xd_temporal(xd, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    tr = random_dtstr()
    # Build a duration
    start = datetime.strptime('1/1/1970', '%m/%d/%Y')
    end = datetime.strptime('12/31/2020', '%m/%d/%Y')
    rdt = start + timedelta(seconds=randint(0, int((end - start).total_seconds())))
    rdt2 = start + timedelta(seconds=randint(0, int((end - start).total_seconds())))
    dur = abs((rdt - rdt2).days)

    indent += '  '
    elstr = indent + """<s3m:ms-""" + str(xd.ct_id) + """>\n"""
    elstr += indent + """  <label>""" + escape(xd.label.strip()) + """</label>\n"""

    if xd.require_vtb:
        elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    if xd.require_vte:
        elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if xd.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if xd.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if xd.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""

    if xd.reference_ranges:
        for rr in xd.reference_ranges.all():
            elstr += indent + referencerange(rr, indent)
    if xd.normal_status:
        elstr += indent + """  <normal-status>""" + xd.normal_status.strip() + """</normal-status>\n"""
    if xd.allow_date:
        elstr += indent + """  <xdtemporal-date>""" + datetime.strftime(rdt.date(), '%Y-%m-%d') + """</xdtemporal-date>\n"""
    if xd.allow_time:
        elstr += indent + """  <xdtemporal-time>""" + datetime.strftime(rdt.date(), '%H:%M:%S') + """</xdtemporal-time>\n"""
    if xd.allow_datetime:
        elstr += indent + """  <xdtemporal-datetime>""" + random_dtstr() + """</xdtemporal-datetime>\n"""
    if xd.allow_day:
        elstr += indent + """  <xdtemporal-day>""" + datetime.strftime(rdt.date(), '---%d') + """</xdtemporal-day>\n"""
    if xd.allow_month:
        elstr += indent + """  <xdtemporal-month>""" + datetime.strftime(rdt.date(), '--%m') + """</xdtemporal-month>\n"""
    if xd.allow_year:
        elstr += indent + """  <xdtemporal-year>""" + datetime.strftime(rdt.date(), '%Y') + """</xdtemporal-year>\n"""
    if xd.allow_year_month:
        elstr += indent + """  <xdtemporal-year-month>""" + datetime.strftime(rdt.date(), '%Y-%m') + """</xdtemporal-year-month>\n"""
    if xd.allow_month_day:
        elstr += indent + """  <xdtemporal-month-day>--""" + datetime.strftime(rdt.date(), '%m-%d') + """</xdtemporal-month-day>\n"""
    if xd.allow_duration:
        elstr += indent + """  <xdtemporal-duration>""" + 'P' + str(dur) + 'D' + """</xdtemporal-duration>\n"""
    elstr += indent + """</s3m:ms-""" + str(xd.ct_id) + """>\n"""

    return elstr


def attestation(a, indent):

    indent += '  '
    elstr = """<label>""" + escape(a.label.strip()) + """</label>\n"""
    if a.view:
        elstr += indent + "<view>\n"
        elstr += Xd_file(a.view, indent, False)
        elstr += indent + "</view>\n"
    if a.proof:
        elstr += indent + "<proof>\n"
        elstr += Xd_file(a.proof, indent, False)
        elstr += indent + "</proof>\n"
    if a.reason:
        elstr += indent + "<reason>\n"
        elstr += Xd_string(a.reason, indent, False)
        elstr += indent + "</reason>\n"
    if a.committer:
        elstr += indent + "<committer>\n"
        elstr += party(a.committer, indent)
        elstr += indent + "</committer>\n"
    elstr += indent + "  <committed>" + random_dtstr() + "Z</committed>\n"
    elstr += indent + "  <pending>true</pending>\n"

    return elstr


def audit(aud, indent):
    indent += '  '
    elstr = indent + """<s3m:ms-""" + str(aud.ct_id) + """>\n"""
    elstr += indent + """<label>""" + escape(aud.label.strip()) + """</label>\n"""
    if aud.system_id:
        elstr += indent + "<system-id>\n"
        elstr += Xd_string(aud.system_id, indent, False)
        elstr += indent + "</system-id>\n"

    if aud.system_user:
        elstr += indent + "<system-user>\n"
        elstr += party(aud.system_user, indent)
        elstr += indent + "</system-user>\n"

    if aud.location:
        elstr += indent + "<location>\n"
        elstr += cluster(aud.location, indent, False)
        elstr += indent + "</location>\n"

    elstr += indent + "  <timestamp>" + random_dtstr() + "Z</timestamp>\n"
    elstr += indent + """</s3m:ms-""" + str(aud.ct_id) + """>\n"""

    return elstr


def participation(p, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    indent += '  '
    elstr = indent + """<s3m:ms-""" + str(p.ct_id) + """>\n"""
    elstr += indent + """<label>""" + escape(p.label.strip()) + """</label>\n"""

    if p.performer:
        elstr += indent + """<performer>\n"""
        elstr += party(p.performer, indent)
        elstr += indent + """</performer>\n"""

    if p.function:
        elstr += indent + """<function>\n"""
        elstr += Xd_string(p.function, indent, False)
        elstr += indent + """</function>\n"""

    if p.mode:
        elstr += indent + """<mode>\n"""
        elstr += Xd_string(p.mode, indent, False)
        elstr += indent + """</mode>\n"""

    elstr += indent + """  <start>""" + vtb + """Z</start>\n"""
    elstr += indent + """  <end>""" + vte + """Z</end>\n"""
    elstr += indent + """</s3m:ms-""" + str(p.ct_id) + """>\n"""

    return elstr


def party(pi, indent):
    indent += '  '
    elstr = indent + "  <label>" + escape(pi.label.strip()) + "</label>\n"
    elstr += indent + "  <party-name>A. Sample Name</party-name>\n"
    if pi.external_ref:
        for ref in pi.external_ref.all():
            elstr += indent + "<party-ref>\n"
            elstr += Xd_link(ref, indent, False)
            elstr += indent + "</party-ref>\n"

    if pi.details:
        elstr += indent + "<party-details>\n"
        elstr += cluster(pi.details, indent, False)
        elstr += indent + "</party-details>\n"

    return elstr


def referencerange(rr, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    indent += '  '
    elstr = """<s3m:ms-""" + str(rr.ct_id) + """> \n"""
    elstr += indent + """  <label>""" + escape(rr.label.strip()) + """</label>\n"""

    elstr += indent + """  <vtb>""" + vtb + """</vtb>\n"""
    elstr += indent + """  <vte>""" + vte + """</vte>\n"""
    if rr.require_tr:
        elstr += indent + """  <tr>""" + tr + """Z</tr>\n"""
    if rr.require_mod:
        elstr += indent + """  <modified>""" + tr + """Z</modified>\n"""
    if rr.require_location:
        latlon = get_latlon()
        elstr += indent + """  <latitude>""" + latlon[0] + """</latitude>\n"""
        elstr += indent + """  <longitude>""" + latlon[1] + """</longitude>\n"""

    elstr += indent + """  <definition>""" + escape(rr.definition) + """</definition>\n"""
    elstr += Xd_interval(rr.interval, indent)
    if rr.is_normal:
        n = 'true'
    else:
        n = 'false'
    elstr += indent + """  <is-normal>""" + n + """</is-normal>\n"""
    elstr += indent + """</s3m:ms-""" + str(rr.ct_id) + """>\n"""

    return elstr


def cluster(clu, indent, pcs=True):
    indent += '  '
    elstr = ''
    if pcs:
        elstr += indent + """<s3m:ms-""" + str(clu.ct_id) + """>\n"""
    elstr += indent + """  <label>""" + escape(clu.label.strip()) + """</label>\n"""
    if clu.clusters:
        for c in clu.clusters.all():
            elstr += cluster(c, indent)

    if clu.xdboolean:
        for Xd in clu.xdboolean.all():
            elstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            elstr += Xd_boolean(Xd, indent + '  ')
            elstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    if clu.xdlink:
        for Xd in clu.xdlink.all():
            elstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            elstr += Xd_link(Xd, indent + '  ')
            elstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    if clu.xdstring:
        for Xd in clu.xdstring.all():
            elstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            elstr += Xd_string(Xd, indent + '  ')
            elstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    if clu.xdfile:
        for Xd in clu.xdfile.all():
            elstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            elstr += Xd_file(Xd, indent + '  ')
            elstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    if clu.xdordinal:
        for Xd in clu.xdordinal.all():
            elstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            elstr += Xd_ordinal(Xd, indent + '  ')
            elstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    if clu.xdcount:
        for Xd in clu.xdcount.all():
            elstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            elstr += Xd_count(Xd, indent + '  ')
            elstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    if clu.xdquantity:
        for Xd in clu.xdquantity.all():
            elstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            elstr += Xd_quantity(Xd, indent + '  ')
            elstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    if clu.xdratio:
        for Xd in clu.xdratio.all():
            elstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            elstr += Xd_ratio(Xd, indent + '  ')
            elstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    if clu.xdtemporal:
        for Xd in clu.xdtemporal.all():
            elstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            elstr += Xd_temporal(Xd, indent + '  ')
            elstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
    if pcs:
        elstr += indent + """</s3m:ms-""" + str(clu.ct_id) + """>\n"""

    return elstr
