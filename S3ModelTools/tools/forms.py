"""
Form definitions.
"""
from cuid import cuid

from django.utils.translation import gettext_lazy as _
from S3ModelTools.settings import BASE_DIR

# ModelMultipleChoiceField(queryset=Thing.objects.all(), widget=Select2MultipleWidget)

from django import forms
from django_select2.forms import Select2MultipleWidget

from .models import XdBoolean, XdCount, XdFile, XdInterval, XdLink, XdOrdinal, XdQuantity, XdFloat, XdRatio, XdString, XdTemporal, Units, PredObj, \
     Cluster, DM, Attestation, Audit, Participation, Party, ReferenceRange, SimpleReferenceRange, Modeler

# TODO: put this in a utils module.


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

# tools forms


class XdBooleanAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(XdBooleanAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(XdBooleanAdminForm, self).clean()
        print(cleaned_data)

        return

    class Meta:
        model = XdBoolean
        fields = '__all__'


class XdStringAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(XdStringAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(XdStringAdminForm, self).clean()
        # are the number of enums and enums_Def correct?
        if cleaned_data['enums'] and not cleaned_data['definitions']:
            raise forms.ValidationError(_("You have enumerations but your annotations seem to be missing."))
        elif cleaned_data['enums'] and cleaned_data['definitions']:
            enums = cleaned_data['enums']
            definitions = cleaned_data['definitions']

            if len(enums.splitlines()) != len(definitions.splitlines()):
                # allow one def to be replicated for all enums
                if len(definitions.splitlines()) == 1:
                    ed = definitions.splitlines()[0]
                    new_defs = []
                    for x in range(0, len(enums.splitlines())):
                        new_defs.append(ed)
                    cleaned_data['definitions'] = '\n'.join(new_defs)
                else:
                    raise forms.ValidationError("The number of 'Enumerations' and 'Enumeration Annotations' must be exactly the same. Check for empty lines.")
        # check the exact, min and max lengths
        if cleaned_data['min_length']:
            if cleaned_data['min_length'] < 0:
                raise forms.ValidationError("The minimum length cannot be less than zero.")

        if cleaned_data['max_length']:
            if cleaned_data['max_length'] < 0:
                raise forms.ValidationError("The maximum length cannot be less than zero.")

        if cleaned_data['exact_length']:
            if cleaned_data['exact_length'] < 0:
                raise forms.ValidationError("The exact length cannot be less than zero.")

        if cleaned_data['min_length'] and cleaned_data['exact_length']:
            raise forms.ValidationError("It is not valid to set exact length and a minimum length.")

        if cleaned_data['max_length'] and cleaned_data['exact_length']:
            raise forms.ValidationError("It is not valid to set exact length and a maximum length.")

        return

    class Meta:
        model = XdString
        fields = '__all__'


class UnitsAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UnitsAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(UnitsAdminForm, self).clean()
        # are the number of enums and enums_Def correct?
        if cleaned_data['enums'] and not cleaned_data['definitions']:
            raise forms.ValidationError(
                "You have enumerations but your annotations seem to be missing.")
        elif cleaned_data['enums'] and cleaned_data['definitions']:
            enums = cleaned_data['enums']
            definitions = cleaned_data['definitions']

            if len(enums.splitlines()) != len(definitions.splitlines()):
                # allow one def to be replicated for all enums
                if len(definitions.splitlines()) == 1:
                    ed = definitions.splitlines()[0]
                    new_defs = []
                    for x in range(0, len(enums.splitlines())):
                        new_defs.append(ed)
                    cleaned_data['definitions'] = '\n'.join(new_defs)
                else:
                    raise forms.ValidationError("The number of 'Enumerations' and 'Enumeration Annotations' must be exactly the same. Check for empty lines.")

        return

    class Meta:
        model = Units
        fields = '__all__'


class XdTemporalAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(XdTemporalAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(
                project=instance.project)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(XdTemporalAdminForm, self).clean()

        # if there is a duration, you cannot have any other temporal elements.
        if cleaned_data['allow_duration']  and (cleaned_data['allow_date'] or cleaned_data['allow_time'] or cleaned_data['allow_datetime'] or
                cleaned_data['allow_day'] or cleaned_data['allow_month'] or cleaned_data['allow_year'] or  cleaned_data['allow_year_month'] or cleaned_data['allow_month_day']):
            raise forms.ValidationError("You cannot have a duration mixed with other temporal types.")

        return

    class Meta:
        model = XdTemporal
        fields = '__all__'


class XdFileAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(XdFileAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(XdFileAdminForm, self).clean()
        cleaned_data['language'] = cleaned_data['lang']

        if cleaned_data['content_mode'] == 'select':
            raise forms.ValidationError("You must select a Content Mode.")

        return

    class Meta:
        model = XdFile
        fields = '__all__'


class XdLinkAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(XdLinkAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(XdLinkAdminForm, self).clean()
        # do something useful here
        return

    class Meta:
        model = XdLink
        fields = '__all__'


class XdOrdinalAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(XdOrdinalAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(XdOrdinalAdminForm, self).clean()
        o = cleaned_data['ordinals']
        # test that the ordinals are really ints
        for n in o.splitlines():
            try:
                x = int(n)
            except:
                raise forms.ValidationError("You MUST use numbers for the Ordinal indicators. It seems one or more of yours is not.")

        # are the number of symbols and definitions correct?
        symbols = cleaned_data['symbols']
        sym_def = cleaned_data['annotations']
        if len(symbols.splitlines()) != len(sym_def.splitlines()):
            if len(sym_def.splitlines()) == 1:  # allow one def to be replicated for all enums
                sd = sym_def.splitlines()[0]
                new_defs = []
                for x in range(0, len(symbols.splitlines())):
                    new_defs.append(sd)
                cleaned_data['annotations'] = '\n'.join(new_defs)
            else:
                raise forms.ValidationError("The number of 'Symbols' and 'Symbol definitions' must be exactly the same. Check for empty lines.")

        return

    class Meta:
        model = XdOrdinal
        fields = '__all__'


class XdCountAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(XdCountAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=instance.project)
            self.fields['units'].queryset = Units.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
            self.fields['units'].queryset = Units.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)
            self.fields['units'].queryset = Units.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(XdCountAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = XdCount
        fields = '__all__'


class XdQuantityAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(XdQuantityAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=instance.project)
            self.fields['units'].queryset = Units.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
            self.fields['units'].queryset = Units.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)
            self.fields['units'].queryset = Units.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(XdQuantityAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = XdQuantity
        fields = '__all__'


class XdFloatAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(XdFloatAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=instance.project)
            self.fields['units'].queryset = Units.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
            self.fields['units'].queryset = Units.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)
            self.fields['units'].queryset = Units.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(XdFloatAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = XdFloat
        fields = '__all__'


class XdRatioAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(XdRatioAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(
                project=instance.project)
            self.fields['num_units'].queryset = Units.objects.filter(project=instance.project)
            self.fields['den_units'].queryset = Units.objects.filter(project=instance.project)
            self.fields['ratio_units'].queryset = Units.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
            self.fields['num_units'].queryset = Units.objects.all()
            self.fields['den_units'].queryset = Units.objects.all()
            self.fields['ratio_units'].queryset = Units.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)
            self.fields['num_units'].queryset = Units.objects.filter(project=self.default_prj)
            self.fields['den_units'].queryset = Units.objects.filter(project=self.default_prj)
            self.fields['ratio_units'].queryset = Units.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(XdRatioAdminForm, self).clean()
        nmini = cleaned_data['num_min_inclusive']
        nmine = cleaned_data['num_min_exclusive']
        nmaxi = cleaned_data['num_max_inclusive']
        nmaxe = cleaned_data['num_max_exclusive']
        dmini = cleaned_data['den_min_inclusive']
        dmine = cleaned_data['den_min_exclusive']
        dmaxi = cleaned_data['den_max_inclusive']
        dmaxe = cleaned_data['den_max_exclusive']

        # tests for proper modelling
        if (nmini and nmine) or (nmaxi and nmaxe):
            raise forms.ValidationError("There is ambiguity in your numerator constraints for min/max. Please use EITHER minimum or maximum values, not both.")
        if (dmini and dmine) or (dmaxi and dmaxe):
            raise forms.ValidationError("There is ambiguity in your denominator constraints for min/max. Please use EITHER minimum or maximum values, not both.")

        return

    class Meta:
        model = XdRatio
        fields = '__all__'


class XdIntervalAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(XdIntervalAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(XdIntervalAdminForm, self).clean()

        if cleaned_data['interval_type'] == 'None':
            raise forms.ValidationError("You must select an Interval Type.")

        if 'lower' in cleaned_data:
            l = cleaned_data['lower']
        else:
            l = None

        if 'upper' in cleaned_data:
            u = cleaned_data['upper']
        else:
            u = None

        # check for modelling errors
        if cleaned_data['lower_bounded'] and (l is None or cleaned_data['lower'] == ''):
            raise forms.ValidationError("Enter lower value or uncheck the lower bounded box.")
        if cleaned_data['upper_bounded'] and (u is None or cleaned_data['upper'] == ''):
            raise forms.ValidationError("Enter upper value or uncheck the upper bounded box.")

        if not cleaned_data['lower_bounded'] and l:
            raise forms.ValidationError("Remove lower value or check the lower bounded box.")
        if not cleaned_data['upper_bounded'] and u:
            raise forms.ValidationError("Remove upper value or check the upper bounded box.")

        if cleaned_data['interval_type'] == 'duration':
            if u and not u.startswith('P'):
                raise forms.ValidationError("Durations must begin with the character 'P' (Upper value)")
            if l and not l.startswith('P'):
                raise forms.ValidationError("Durations must begin with the upper case character 'P' (Lower value)")

        # check valid decimals and if the user used a comma as a decimal
        # separator then replace it with a period.
        if cleaned_data['interval_type'] == 'decimal':
            if l and "," in l:
                l = l.replace(",", ".")
            if u and "," in u:
                u = u.replace(",", ".")
            if l and not is_number(l):
                raise forms.ValidationError("The lower value must be a number.")
            if u and not is_number(u):
                raise forms.ValidationError("The upper value must be a number.")

        # check for valid integers
        if cleaned_data['interval_type'] == 'int':
            if l and not is_number(l):
                raise forms.ValidationError("The lower value must be a number.")
            if u and not is_number(u):
                raise forms.ValidationError("The upper value must be a number.")

        # TODO: check for valid dates

        # TODO: check for valid dateTimes
        # TODO: check for valid times

        cleaned_data['upper'] = u
        cleaned_data['lower'] = l

        # if units are defined insure there is a URI as well.
        if cleaned_data['units_name'] and len(cleaned_data['units_name']) > 0:
            if len(cleaned_data['units_uri']) == 0:
                raise forms.ValidationError("The Units definition must have both a name and a URI.")
        if cleaned_data['units_uri'] and len(cleaned_data['units_uri']) > 0:
            if len(cleaned_data['units_name']) == 0:
                raise forms.ValidationError("The Units definition must have both a name and a URI.")
        return

    class Meta:
        model = XdInterval
        fields = '__all__'


class ReferenceRangeAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReferenceRangeAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['interval'].queryset = XdInterval.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['interval'].queryset = XdInterval.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['interval'].queryset = XdInterval.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(ReferenceRangeAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = ReferenceRange
        fields = '__all__'


class SimpleRRAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SimpleRRAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(SimpleRRAdminForm, self).clean()
        # do something here if needed.

        return cleaned_data

    class Meta:
        model = SimpleReferenceRange
        fields = '__all__'


class ClusterAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClusterAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['clusters'].queryset = Cluster.objects.filter(project=instance.project)
            self.fields['xdboolean'].queryset = XdBoolean.objects.filter(project=instance.project)
            self.fields['xdlink'].queryset = XdLink.objects.filter(project=instance.project)
            self.fields['xdstring'].queryset = XdString.objects.filter(project=instance.project)
            self.fields['xdfile'].queryset = XdFile.objects.filter(project=instance.project)
            self.fields['xdordinal'].queryset = XdOrdinal.objects.filter(project=instance.project)
            self.fields['xdcount'].queryset = XdCount.objects.filter(project=instance.project)
            self.fields['xdquantity'].queryset = XdQuantity.objects.filter(project=instance.project)
            self.fields['xdratio'].queryset = XdRatio.objects.filter(project=instance.project)
            self.fields['xdtemporal'].queryset = XdTemporal.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['clusters'].queryset = Cluster.objects.all()
                self.fields['xdboolean'].queryset = XdBoolean.objects.all()
                self.fields['xdlink'].queryset = XdLink.objects.all()
                self.fields['xdstring'].queryset = XdString.objects.all()
                self.fields['xdfile'].queryset = XdFile.objects.all()
                self.fields['xdordinal'].queryset = XdOrdinal.objects.all()
                self.fields['xdcount'].queryset = XdCount.objects.all()
                self.fields['xdquantity'].queryset = XdQuantity.objects.all()
                self.fields['xdratio'].queryset = XdRatio.objects.all()
                self.fields['xdtemporal'].queryset = XdTemporal.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['clusters'].queryset = Cluster.objects.filter(project=self.default_prj)
            self.fields['xdboolean'].queryset = XdBoolean.objects.filter(project=self.default_prj)
            self.fields['xdlink'].queryset = XdLink.objects.filter(project=self.default_prj)
            self.fields['xdstring'].queryset = XdString.objects.filter(project=self.default_prj)
            self.fields['xdfile'].queryset = XdFile.objects.filter(project=self.default_prj)
            self.fields['xdordinal'].queryset = XdOrdinal.objects.filter(project=self.default_prj)
            self.fields['xdcount'].queryset = XdCount.objects.filter(project=self.default_prj)
            self.fields['xdquantity'].queryset = XdQuantity.objects.filter(project=self.default_prj)
            self.fields['xdratio'].queryset = XdRatio.objects.filter(project=self.default_prj)
            self.fields['xdtemporal'].queryset = XdTemporal.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(ClusterAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Cluster
        fields = '__all__'


class DMAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DMAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published is True:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['participations'].queryset = Participation.objects.filter(project=instance.project)
            self.fields['links'].queryset = XdLink.objects.filter(project=instance.project)
            self.fields['protocol'].queryset = XdString.objects.filter(project=instance.project)
            self.fields['workflow'].queryset = XdLink.objects.filter(project=instance.project)
            self.fields['attestation'].queryset = Attestation.objects.filter(project=instance.project)
            self.fields['audit'].queryset = Audit.objects.filter(project=instance.project)
            self.fields['data'].queryset = Cluster.objects.filter(project=instance.project)
            self.fields['subject'].queryset = Party.objects.filter(project=instance.project)
            self.fields['provider'].queryset = Party.objects.filter(project=instance.project)

        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['participations'].queryset = Participation.objects.all()
            self.fields['links'].queryset = XdLink.objects.all()
            self.fields['protocol'].queryset = XdString.objects.all()
            self.fields['workflow'].queryset = XdLink.objects.all()
            self.fields['attestation'].queryset = Attestation.objects.all()
            self.fields['audit'].queryset = Audit.objects.all()
            self.fields['data'].queryset = Cluster.objects.all()
            self.fields['subject'].queryset = Party.objects.all()
            self.fields['provider'].queryset = Party.objects.all()

        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['participations'].queryset = Participation.objects.filter(project=self.default_prj)
            self.fields['links'].queryset = XdLink.objects.filter(project=self.default_prj)
            self.fields['protocol'].queryset = XdString.objects.filter(project=self.default_prj)
            self.fields['workflow'].queryset = XdLink.objects.filter(project=self.default_prj)
            self.fields['attestation'].queryset = Attestation.objects.filter(project=self.default_prj)
            self.fields['audit'].queryset = Audit.objects.filter(project=self.default_prj)
            self.fields['data'].queryset = Cluster.objects.filter(project=self.default_prj)
            self.fields['subject'].queryset = Party.objects.filter(project=self.default_prj)
            self.fields['provider'].queryset = Party.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(DMAdminForm, self).clean()

        return

    class Meta:
        model = DM
        fields = '__all__'
        widgets = {
            'links': forms.SelectMultiple(attrs={'size': 12}),
            'participations': forms.SelectMultiple(attrs={'size': 12}),
                }


class DMAdminSUForm(forms.ModelForm):
    """
    Superuser form to reset/republish the DM.
    Not used, see notes in DMAdmin
    """

    def __init__(self, *args, **kwargs):
        super(DMAdminSUForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published is True:
            instance.published = False
            instance.ct_id = cuid()
            instance.html_file.delete()
            instance.xml_file.delete()
            instance.json_file.delete()
            instance.xsd_file.delete()
            instance.sha1_file.delete()
            instance.zip_file.delete()

    def clean(self):
        cleaned_data = super(DMAdminSUForm, self).clean()

        return

    class Meta:
        model = DM
        fields = '__all__'


class AuditAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AuditAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['system_id'].queryset = XdString.objects.filter(project=instance.project)
            self.fields['system_user'].queryset = Party.objects.filter(project=instance.project)
            self.fields['location'].queryset = Cluster.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['system_id'].queryset = XdString.objects.all()
            self.fields['system_user'].queryset = Party.objects.all()
            self.fields['location'].queryset = Cluster.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['system_id'].queryset = XdString.objects.filter(project=self.default_prj)
            self.fields['system_user'].queryset = Party.objects.filter(project=self.default_prj)
            self.fields['location'].queryset = Cluster.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(AuditAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Audit
        fields = '__all__'


class ParticipationAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ParticipationAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['performer'].queryset = Party.objects.filter(project=instance.project)
            self.fields['function'].queryset = XdString.objects.filter(project=instance.project)
            self.fields['mode'].queryset = XdString.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['performer'].queryset = Party.objects.all()
            self.fields['function'].queryset = XdString.objects.all()
            self.fields['mode'].queryset = XdString.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['performer'].queryset = Party.objects.filter(project=self.default_prj)
            self.fields['function'].queryset = XdString.objects.filter(project=self.default_prj)
            self.fields['mode'].queryset = XdString.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(ParticipationAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Participation
        fields = '__all__'


class PartyAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PartyAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['details'].queryset = Cluster.objects.filter(project=instance.project)
            self.fields['external_ref'].queryset = XdLink.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['details'].queryset = Cluster.objects.all()
            self.fields['external_ref'].queryset = XdLink.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['details'].queryset = Cluster.objects.filter(project=self.default_prj)
            self.fields['external_ref'].queryset = XdLink.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(PartyAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Party
        fields = '__all__'


class AttestationAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AttestationAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            self.fields['view'].queryset = XdFile.objects.filter(project=instance.project)
            self.fields['proof'].queryset = XdFile.objects.filter(project=instance.project)
            self.fields['reason'].queryset = XdString.objects.filter(project=instance.project)
            self.fields['committer'].queryset = Party.objects.filter(project=instance.project)
        elif instance.pk is None and self.default_prj is None:
            self.fields['pred_obj'].queryset = PredObj.objects.all()
            self.fields['view'].queryset = XdFile.objects.all()
            self.fields['proof'].queryset = XdFile.objects.all()
            self.fields['reason'].queryset = XdString.objects.all()
            self.fields['committer'].queryset = Party.objects.all()
        else:
            self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            self.fields['view'].queryset = XdFile.objects.filter(project=self.default_prj)
            self.fields['proof'].queryset = XdFile.objects.filter(project=self.default_prj)
            self.fields['reason'].queryset = XdString.objects.filter(project=self.default_prj)
            self.fields['committer'].queryset = Party.objects.filter(project=self.default_prj)

    def clean(self):
        cleaned_data = super(AttestationAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Attestation
        fields = '__all__'


# ***************************************************
class ContactForm(forms.Form):
    # example
    full_name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField()


class SignUpForm(forms.ModelForm):
    # example
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        #write validation code.
        return full_name

# *********************************************
class ModelerForm(forms.ModelForm):
    class Meta:
        model = Modeler
        fields = ['name', 'email', 'project', 'prj_filter']


class AttestationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(AttestationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None: # existing record
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['view'].queryset = XdFile.objects.filter(project=instance.project)
                self.fields['proof'].queryset = XdFile.objects.filter(project=instance.project)
                self.fields['reason'].queryset = XdString.objects.filter(project=instance.project)
                self.fields['committer'].queryset = Party.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['view'].queryset = XdFile.objects.all()
                self.fields['proof'].queryset = XdFile.objects.all()
                self.fields['reason'].queryset = XdString.objects.all()
                self.fields['committer'].queryset = Party.objects.all()
        else:  # new record
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['view'].queryset = XdFile.objects.filter(project=self.default_prj)
                self.fields['proof'].queryset = XdFile.objects.filter(project=self.default_prj)
                self.fields['reason'].queryset = XdString.objects.filter(project=self.default_prj)
                self.fields['committer'].queryset = Party.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['view'].queryset = XdFile.objects.all()
                self.fields['proof'].queryset = XdFile.objects.all()
                self.fields['reason'].queryset = XdString.objects.all()
                self.fields['committer'].queryset = Party.objects.all()

    def clean(self):
        cleaned_data = super(AttestationForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Attestation
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'seq', 'view', 'proof', 'reason', 'committer']


class AuditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(AuditForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

        if instance.pk is not None: # existing record
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['system_id'].queryset = XdString.objects.filter(project=instance.project)
                self.fields['system_user'].queryset = Party.objects.filter(project=instance.project)
                self.fields['location'].queryset = Cluster.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['system_id'].queryset = XdString.objects.all()
                self.fields['system_user'].queryset = Party.objects.all()
                self.fields['location'].queryset = Cluster.objects.all()
        else:  # new record
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['system_id'].queryset = XdString.objects.filter(project=self.default_prj)
                self.fields['system_user'].queryset = Party.objects.filter(project=self.default_prj)
                self.fields['location'].queryset = Cluster.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['system_id'].queryset = XdString.objects.all()
                self.fields['system_user'].queryset = Party.objects.all()
                self.fields['location'].queryset = Cluster.objects.all()

    def clean(self):
        cleaned_data = super(AuditForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Audit
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'seq', 'system_id', 'system_user', 'location']


class BooleanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(BooleanForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

        if instance.pk is not None:
            if self.filter_prj:
                qs = PredObj.objects.filter(project=instance.project)
            else:
                qs = PredObj.objects.all()
        else:
            if self.filter_prj:
                qs = PredObj.objects.filter(project=self.default_prj)
            else:
                qs = PredObj.objects.all()

        self.fields['pred_obj'] = forms.ModelMultipleChoiceField(queryset = qs, widget=Select2MultipleWidget)


    def clean(self):
        cleaned_data = super(BooleanForm, self).clean()

        return

    class Meta:
        model = XdBoolean
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'ui_type', 'seq', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'trues', 'falses']
        widgets = {
                    'description': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
                    'label': forms.TextInput(attrs={'size': 50})
                }


class ClusterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(ClusterForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['clusters'].queryset = Cluster.objects.filter(project=instance.project)
                self.fields['xdboolean'].queryset = XdBoolean.objects.filter(project=instance.project)
                self.fields['xdlink'].queryset = XdLink.objects.filter(project=instance.project)
                self.fields['xdstring'].queryset = XdString.objects.filter(project=instance.project)
                self.fields['xdfile'].queryset = XdFile.objects.filter(project=instance.project)
                self.fields['xdordinal'].queryset = XdOrdinal.objects.filter(project=instance.project)
                self.fields['xdcount'].queryset = XdCount.objects.filter(project=instance.project)
                self.fields['xdquantity'].queryset = XdQuantity.objects.filter(project=instance.project)
                self.fields['xdratio'].queryset = XdRatio.objects.filter(project=instance.project)
                self.fields['xdtemporal'].queryset = XdTemporal.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['clusters'].queryset = Cluster.objects.all()
                self.fields['xdboolean'].queryset = XdBoolean.objects.all()
                self.fields['xdlink'].queryset = XdLink.objects.all()
                self.fields['xdstring'].queryset = XdString.objects.all()
                self.fields['xdfile'].queryset = XdFile.objects.all()
                self.fields['xdordinal'].queryset = XdOrdinal.objects.all()
                self.fields['xdcount'].queryset = XdCount.objects.all()
                self.fields['xdquantity'].queryset = XdQuantity.objects.all()
                self.fields['xdratio'].queryset = XdRatio.objects.all()
                self.fields['xdtemporal'].queryset = XdTemporal.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['clusters'].queryset = Cluster.objects.filter(project=self.default_prj)
                self.fields['xdboolean'].queryset = XdBoolean.objects.filter(project=self.default_prj)
                self.fields['xdlink'].queryset = XdLink.objects.filter(project=self.default_prj)
                self.fields['xdstring'].queryset = XdString.objects.filter(project=self.default_prj)
                self.fields['xdfile'].queryset = XdFile.objects.filter(project=self.default_prj)
                self.fields['xdordinal'].queryset = XdOrdinal.objects.filter(project=self.default_prj)
                self.fields['xdcount'].queryset = XdCount.objects.filter(project=self.default_prj)
                self.fields['xdquantity'].queryset = XdQuantity.objects.filter(project=self.default_prj)
                self.fields['xdratio'].queryset = XdRatio.objects.filter(project=self.default_prj)
                self.fields['xdtemporal'].queryset = XdTemporal.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['clusters'].queryset = Cluster.objects.all()
                self.fields['xdboolean'].queryset = XdBoolean.objects.all()
                self.fields['xdlink'].queryset = XdLink.objects.all()
                self.fields['xdstring'].queryset = XdString.objects.all()
                self.fields['xdfile'].queryset = XdFile.objects.all()
                self.fields['xdordinal'].queryset = XdOrdinal.objects.all()
                self.fields['xdcount'].queryset = XdCount.objects.all()
                self.fields['xdquantity'].queryset = XdQuantity.objects.all()
                self.fields['xdratio'].queryset = XdRatio.objects.all()
                self.fields['xdtemporal'].queryset = XdTemporalj.objects.all()

    def clean(self):
        cleaned_data = super(ClusterForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Cluster
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'seq', 'clusters', 'xdboolean', 'xdlink', 'xdstring', 'xdfile', 'xdordinal', 'xdcount', 'xdquantity', 'xdfloat', 'xdratio', 'xdtemporal']


class CountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(CountForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=instance.project)
                self.fields['units'].queryset = Units.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
                self.fields['units'].queryset = Units.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)
                self.fields['units'].queryset = Units.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
                self.fields['units'].queryset = Units.objects.all()

    def clean(self):
        cleaned_data = super(CountForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = XdCount
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'ui_type', 'seq', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'normal_status', 'min_magnitude', 'max_magnitude', 'min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive', 'total_digits', 'reference_ranges', 'units']



class DMForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(DMForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance.published is True:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['participations'].queryset = Participation.objects.filter(project=instance.project)
                self.fields['links'].queryset = XdLink.objects.filter(project=instance.project)
                self.fields['protocol'].queryset = XdString.objects.filter(project=instance.project)
                self.fields['workflow'].queryset = XdLink.objects.filter(project=instance.project)
                self.fields['attestation'].queryset = Attestation.objects.filter(project=instance.project)
                self.fields['audit'].queryset = Audit.objects.filter(project=instance.project)
                self.fields['data'].queryset = Cluster.objects.filter(project=instance.project)
                self.fields['subject'].queryset = Party.objects.filter(project=instance.project)
                self.fields['provider'].queryset = Party.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['participations'].queryset = Participation.objects.all()
                self.fields['links'].queryset = XdLink.objects.all()
                self.fields['protocol'].queryset = XdString.objects.all()
                self.fields['workflow'].queryset = XdLink.objects.all()
                self.fields['attestation'].queryset = Attestation.objects.all()
                self.fields['audit'].queryset = Audit.objects.all()
                self.fields['data'].queryset = Cluster.objects.all()
                self.fields['subject'].queryset = Party.objects.all()
                self.fields['provider'].queryset = Party.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['participations'].queryset = Participation.objects.filter(project=self.default_prj)
                self.fields['links'].queryset = XdLink.objects.filter(project=self.default_prj)
                self.fields['protocol'].queryset = XdString.objects.filter(project=self.default_prj)
                self.fields['workflow'].queryset = XdLink.objects.filter(project=self.default_prj)
                self.fields['attestation'].queryset = Attestation.objects.filter(project=self.default_prj)
                self.fields['audit'].queryset = Audit.objects.filter(project=self.default_prj)
                self.fields['data'].queryset = Cluster.objects.filter(project=self.default_prj)
                self.fields['subject'].queryset = Party.objects.filter(project=self.default_prj)
                self.fields['provider'].queryset = Party.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['participations'].queryset = Participation.objects.all()
                self.fields['links'].queryset = XdLink.objects.all()
                self.fields['protocol'].queryset = XdString.objects.all()
                self.fields['workflow'].queryset = XdLink.objects.all()
                self.fields['attestation'].queryset = Attestation.objects.all()
                self.fields['audit'].queryset = Audit.objects.all()
                self.fields['data'].queryset = Cluster.objects.all()
                self.fields['subject'].queryset = Party.objects.all()
                self.fields['provider'].queryset = Party.objects.all()

    def clean(self):
        cleaned_data = super(DMForm, self).clean()

        return

    class Meta:
        model = DM
        fields = ['project', 'pred_obj', 'title', 'published', 'description', 'author', 'contrib', 'dc_subject', 'state', 'data', 'subject', 'provider', 'participations', 'protocol', 'workflow', 'audit', 'attestation', 'links', 'acs', 'published', 'about', 'source', 'rights', 'relation', 'coverage', 'publisher', 'dc_language', 'language', 'encoding']
        widgets = {
            'links': forms.SelectMultiple(attrs={'size': 12}),
            'participations': forms.SelectMultiple(attrs={'size': 12}),
                }


class FileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(FileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()

    def clean(self):
        cleaned_data = super(FileForm, self).clean()
        if cleaned_data['content_mode'] == 'select':
            raise forms.ValidationError("You must select a Content Mode.")

        return

    class Meta:
        model = XdFile
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'ui_type', 'seq', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'media_type', 'encoding', 'language', 'content_mode']


class FloatForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(FloatForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=instance.project)
                self.fields['units'].queryset = Units.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
                self.fields['units'].queryset = Units.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)
                self.fields['units'].queryset = Units.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
                self.fields['units'].queryset = Units.objects.all()

    def clean(self):
        cleaned_data = super(FloatForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = XdFloat
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'ui_type', 'seq', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'normal_status', 'min_magnitude', 'max_magnitude', 'min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive', 'total_digits', 'reference_ranges', 'units']


class IntervalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(IntervalForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()

    def clean(self):
        cleaned_data = super(IntervalForm, self).clean()

        if cleaned_data['interval_type'] == 'None':
            raise forms.ValidationError("You must select an Interval Type.")

        if 'lower' in cleaned_data:
            l = cleaned_data['lower']
        else:
            l = None

        if 'upper' in cleaned_data:
            u = cleaned_data['upper']
        else:
            u = None

        # check for modelling errors
        if cleaned_data['lower_bounded'] and (l is None or cleaned_data['lower'] == ''):
            raise forms.ValidationError("Enter lower value or uncheck the lower bounded box.")
        if cleaned_data['upper_bounded'] and (u is None or cleaned_data['upper'] == ''):
            raise forms.ValidationError("Enter upper value or uncheck the upper bounded box.")

        if not cleaned_data['lower_bounded'] and l:
            raise forms.ValidationError("Remove lower value or check the lower bounded box.")
        if not cleaned_data['upper_bounded'] and u:
            raise forms.ValidationError("Remove upper value or check the upper bounded box.")

        if cleaned_data['interval_type'] == 'duration':
            if u and not u.startswith('P'):
                raise forms.ValidationError("Durations must begin with the character 'P' (Upper value)")
            if l and not l.startswith('P'):
                raise forms.ValidationError("Durations must begin with the upper case character 'P' (Lower value)")

        # check valid decimals and if the user used a comma as a decimal
        # separator then replace it with a period.
        if cleaned_data['interval_type'] == 'decimal':
            if l and "," in l:
                l = l.replace(",", ".")
            if u and "," in u:
                u = u.replace(",", ".")
            if l and not is_number(l):
                raise forms.ValidationError("The lower value must be a number.")
            if u and not is_number(u):
                raise forms.ValidationError("The upper value must be a number.")

        # check for valid integers
        if cleaned_data['interval_type'] == 'int':
            if l and not is_number(l):
                raise forms.ValidationError("The lower value must be a number.")
            if u and not is_number(u):
                raise forms.ValidationError("The upper value must be a number.")

        # TODO: check for valid dates

        # TODO: check for valid dateTimes
        # TODO: check for valid times

        cleaned_data['upper'] = u
        cleaned_data['lower'] = l

        # if units are defined insure there is a URI as well.
        if cleaned_data['units_name'] and len(cleaned_data['units_name']) > 0:
            if len(cleaned_data['units_uri']) == 0:
                raise forms.ValidationError("The Units definition must have both a name and a URI.")
        if cleaned_data['units_uri'] and len(cleaned_data['units_uri']) > 0:
            if len(cleaned_data['units_name']) == 0:
                raise forms.ValidationError("The Units definition must have both a name and a URI.")
        return

    class Meta:
        model = XdInterval
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'lower', 'upper', 'interval_type', 'lower_included', 'upper_included', 'lower_bounded', 'upper_bounded', 'units_name', 'units_uri']


class LinkForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(LinkForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()

    def clean(self):
        cleaned_data = super(LinkForm, self).clean()
        # do something useful here
        return

    class Meta:
        model = XdLink
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'ui_type', 'seq', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'link', 'relation', 'relation_uri']

class OrdinalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(OrdinalForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()

    def clean(self):
        cleaned_data = super(OrdinalForm, self).clean()
        o = cleaned_data['ordinals']
        # test that the ordinals are really ints
        for n in o.splitlines():
            try:
                x = int(n)
            except:
                raise forms.ValidationError("You MUST use numbers for the Ordinal indicators. It seems one or more of yours is not.")

        # are the number of symbols and definitions correct?
        symbols = cleaned_data['symbols']
        sym_def = cleaned_data['annotations']
        if len(symbols.splitlines()) != len(sym_def.splitlines()):
            if len(sym_def.splitlines()) == 1:  # allow one def to be replicated for all enums
                sd = sym_def.splitlines()[0]
                new_defs = []
                for x in range(0, len(symbols.splitlines())):
                    new_defs.append(sd)
                cleaned_data['annotations'] = '\n'.join(new_defs)
            else:
                raise forms.ValidationError("The number of 'Symbols' and 'Symbol definitions' must be exactly the same. Check for empty lines.")

        return

    class Meta:
        model = XdOrdinal
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'ui_type', 'seq', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'reference_ranges', 'normal_status', 'ordinals', 'symbols', 'annotations']


class ParticipationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(ParticipationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['performer'].queryset = Party.objects.filter(project=instance.project)
                self.fields['function'].queryset = XdString.objects.filter(project=instance.project)
                self.fields['mode'].queryset = XdString.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['performer'].queryset = Party.objects.all()
                self.fields['function'].queryset = XdString.objects.all()
                self.fields['mode'].queryset = XdString.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['performer'].queryset = Party.objects.filter(project=self.default_prj)
                self.fields['function'].queryset = XdString.objects.filter(project=self.default_prj)
                self.fields['mode'].queryset = XdString.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['performer'].queryset = Party.objects.all()
                self.fields['function'].queryset = XdString.objects.all()
                self.fields['mode'].queryset = XdString.objects.all()

    def clean(self):
        cleaned_data = super(ParticipationForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Participation
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'seq', 'performer', 'function', 'mode']


class PartyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(PartyForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['details'].queryset = Cluster.objects.filter(project=instance.project)
                self.fields['external_ref'].queryset = XdLink.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['details'].queryset = Cluster.objects.all()
                self.fields['external_ref'].queryset = XdLink.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['details'].queryset = Cluster.objects.filter(project=self.default_prj)
                self.fields['external_ref'].queryset = XdLink.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['details'].queryset = Cluster.objects.all()
                self.fields['external_ref'].queryset = XdLink.objects.all()

    def clean(self):
        cleaned_data = super(PartyForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Party
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'seq', 'external_ref', 'details']


class QuantityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(QuantityForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)

        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=instance.project)
                self.fields['units'].queryset = Units.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
                self.fields['units'].queryset = Units.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)
                self.fields['units'].queryset = Units.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
                self.fields['units'].queryset = Units.objects.all()

    def clean(self):
        cleaned_data = super(QuantityForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = XdQuantity
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'ui_type', 'seq', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'normal_status', 'min_magnitude', 'max_magnitude', 'min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive', 'total_digits', 'fraction_digits', 'reference_ranges', 'units']


class RatioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(RatioForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=instance.project)
                self.fields['num_units'].queryset = Units.objects.filter(project=instance.project)
                self.fields['den_units'].queryset = Units.objects.filter(project=instance.project)
                self.fields['ratio_units'].queryset = Units.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
                self.fields['num_units'].queryset = Units.objects.all()
                self.fields['den_units'].queryset = Units.objects.all()
                self.fields['ratio_units'].queryset = Units.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)
                self.fields['num_units'].queryset = Units.objects.filter(project=self.default_prj)
                self.fields['den_units'].queryset = Units.objects.filter(project=self.default_prj)
                self.fields['ratio_units'].queryset = Units.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
                self.fields['num_units'].queryset = Units.objects.all()
                self.fields['den_units'].queryset = Units.objects.all()
                self.fields['ratio_units'].queryset = Units.objects.all()

    def clean(self):
        cleaned_data = super(RatioForm, self).clean()
        nmini = cleaned_data['num_min_inclusive']
        nmine = cleaned_data['num_min_exclusive']
        nmaxi = cleaned_data['num_max_inclusive']
        nmaxe = cleaned_data['num_max_exclusive']
        dmini = cleaned_data['den_min_inclusive']
        dmine = cleaned_data['den_min_exclusive']
        dmaxi = cleaned_data['den_max_inclusive']
        dmaxe = cleaned_data['den_max_exclusive']

        # tests for proper modelling
        if (nmini and nmine) or (nmaxi and nmaxe):
            raise forms.ValidationError("There is ambiguity in your numerator constraints for min/max. Please use EITHER minimum or maximum values, not both.")
        if (dmini and dmine) or (dmaxi and dmaxe):
            raise forms.ValidationError("There is ambiguity in your denominator constraints for min/max. Please use EITHER minimum or maximum values, not both.")

        return

    class Meta:
        model = XdRatio
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'ui_type', 'seq', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'normal_status', 'reference_ranges', \
                  'num_min_inclusive', 'num_min_exclusive', 'num_max_inclusive', 'num_max_exclusive', 'den_min_inclusive', 'den_min_exclusive', 'den_max_inclusive', 'den_max_exclusive', \
                  'min_magnitude', 'max_magnitude', 'min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive', 'total_digits', 'ratio_type', 'num_units', 'den_units', 'ratio_units']


class ReferenceRangeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(ReferenceRangeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['interval'].queryset = XdInterval.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['interval'].queryset = XdInterval.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['interval'].queryset = XdInterval.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['interval'].queryset = XdInterval.objects.all()

    def clean(self):
        cleaned_data = super(ReferenceRangeForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = ReferenceRange
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'definition', 'is_normal', 'interval']


class StringForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(StringForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()

    def clean(self):
        cleaned_data = super(StringForm, self).clean()
        # are the number of enums and enums_Def correct?
        if cleaned_data['enums'] and not cleaned_data['definitions']:
            raise forms.ValidationError(_("You have enumerations but your annotations seem to be missing."))
        elif cleaned_data['enums'] and cleaned_data['definitions']:
            enums = cleaned_data['enums']
            definitions = cleaned_data['definitions']

            if len(enums.splitlines()) != len(definitions.splitlines()):
                # allow one def to be replicated for all enums
                if len(definitions.splitlines()) == 1:
                    ed = definitions.splitlines()[0]
                    new_defs = []
                    for x in range(0, len(enums.splitlines())):
                        new_defs.append(ed)
                    cleaned_data['definitions'] = '\n'.join(new_defs)
                else:
                    raise forms.ValidationError("The number of 'Enumerations' and 'Enumeration Annotations' must be exactly the same. Check for empty lines.")
        # check the exact, min and max lengths
        if cleaned_data['min_length']:
            if cleaned_data['min_length'] < 0:
                raise forms.ValidationError("The minimum length cannot be less than zero.")

        if cleaned_data['max_length']:
            if cleaned_data['max_length'] < 0:
                raise forms.ValidationError("The maximum length cannot be less than zero.")

        if cleaned_data['exact_length']:
            if cleaned_data['exact_length'] < 0:
                raise forms.ValidationError("The exact length cannot be less than zero.")

        if cleaned_data['min_length'] and cleaned_data['exact_length']:
            raise forms.ValidationError("It is not valid to set exact length and a minimum length.")

        if cleaned_data['max_length'] and cleaned_data['exact_length']:
            raise forms.ValidationError("It is not valid to set exact length and a maximum length.")

        return

    class Meta:
        model = XdString
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'ui_type', 'seq', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'min_length', 'max_length', 'exact_length', 'enums', 'definitions', 'def_val', 'str_fmt']


class TemporalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(TemporalForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
                self.fields['reference_ranges'].queryset = ReferenceRange.objects.all()

    def clean(self):
        cleaned_data = super(TemporalForm, self).clean()

        # if there is a duration, you cannot have any other temporal elements.
        if cleaned_data['allow_duration']  and (cleaned_data['allow_date'] or cleaned_data['allow_time'] or cleaned_data['allow_datetime'] or
                cleaned_data['allow_day'] or cleaned_data['allow_month'] or cleaned_data['allow_year'] or  cleaned_data['allow_year_month'] or cleaned_data['allow_month_day']):
            raise forms.ValidationError("You cannot have a duration mixed with other temporal types.")

        return

    class Meta:
        model = XdTemporal
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'ui_type', 'seq', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'normal_status', 'reference_ranges', 'allow_duration', \
                  'allow_date', 'allow_time', 'allow_datetime', 'allow_day', 'allow_month', 'allow_year', 'allow_year_month', 'allow_month_day']


class UnitsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.default_prj = kwargs.pop('default_prj', None)
        self.filter_prj = kwargs.pop('filter_prj', None)

        super(UnitsForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
        if instance.pk is not None:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=instance.project)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()
        else:
            if self.filter_prj:
                self.fields['pred_obj'].queryset = PredObj.objects.filter(project=self.default_prj)
            else:
                self.fields['pred_obj'].queryset = PredObj.objects.all()

    def clean(self):
        cleaned_data = super(UnitsForm, self).clean()
        # are the number of enums and enums_Def correct?
        if cleaned_data['enums'] and not cleaned_data['definitions']:
            raise forms.ValidationError(_("You have enumerations but your annotations seem to be missing."))
        elif cleaned_data['enums'] and cleaned_data['definitions']:
            enums = cleaned_data['enums']
            definitions = cleaned_data['definitions']

            if len(enums.splitlines()) != len(definitions.splitlines()):
                # allow one def to be replicated for all enums
                if len(definitions.splitlines()) == 1:
                    ed = definitions.splitlines()[0]
                    new_defs = []
                    for x in range(0, len(enums.splitlines())):
                        new_defs.append(ed)
                    cleaned_data['definitions'] = '\n'.join(new_defs)
                else:
                    raise forms.ValidationError("The number of 'Enumerations' and 'Enumeration Annotations' must be exactly the same. Check for empty lines.")
        # check the exact, min and max lengths
        if cleaned_data['min_length']:
            if cleaned_data['min_length'] < 0:
                raise forms.ValidationError("The minimum length cannot be less than zero.")

        if cleaned_data['max_length']:
            if cleaned_data['max_length'] < 0:
                raise forms.ValidationError("The maximum length cannot be less than zero.")

        if cleaned_data['exact_length']:
            if cleaned_data['exact_length'] < 0:
                raise forms.ValidationError("The exact length cannot be less than zero.")

        if cleaned_data['min_length'] and cleaned_data['exact_length']:
            raise forms.ValidationError("It is not valid to set exact length and a minimum length.")

        if cleaned_data['max_length'] and cleaned_data['exact_length']:
            raise forms.ValidationError("It is not valid to set exact length and a maximum length.")

        return

    class Meta:
        model = Units
        fields = ['project', 'pred_obj', 'label', 'published', 'description', 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'enums', 'definitions', 'def_val']

