from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import get_object_or_404, render
from smartpollution.forms import *
from .models import Device, Metric, Template, Threshold, Contract
from .views import *
from .read_eth_chain import *
from .generate_smartcontract import *
from django.utils.text import slugify



def add_metric_to_device(request, pk):
    """
    return the arguments to rendere the add_metric_view
    :param request: 
    :param pk: pk of a device
    :return: all metrics possible to add to the device
    """
    try:
        arguments = {}
        arguments['pk'] = pk
        pot_met = Metric.objects.all()
        arguments['metrics']=[]
        arguments['device']=Device.objects.get(id=pk)
        for met in pot_met:
            if met not in Device.objects.get(id=pk).metrics.all():
                arguments['metrics'].append(met)
        return render(request, 'smartpollution/addmetrictodevice.html', arguments)
    except:
        return return_problem_page(request)



def add_template_to_device(request, pk):
    """
    returns arguments to rendere the add_template_view
    :param request: 
    :param pk:  pk of a device
    :return: returns all metrics which the device can capture
    """
    try:
        arguments = {}
        arguments['pk'] = pk
        arguments['metrics_of_device'] = Device.objects.get(id=pk).metrics.all()
        return render(request, 'smartpollution/addtemplatetodevice.html', arguments)
    except:
        return return_problem_page(request)



def add_device(request):
    """
    adds the device to the db
    :param request: the device data to save
    :return: redirect user to mainpage
    """
    try:
        redirect_id=1;
        if request.POST:
            form = RegisterDeviceForm(request.POST)
            if form.is_valid():
                device_n = form.cleaned_data['device_name']
                manufacturing_c = form.cleaned_data['manufacturing_company']
                device = Device(manufacturing_company=manufacturing_c.replace(' ',''), device_name=device_n.replace(' ',''))
                device.save()
                redirect_id=device.id;
        return detail_view(request,redirect_id)
    except Exception as e:
        print(e)
        return return_problem_page(request)

def add_contract(request):
    try:
        redirect_id=1;
        if request.POST:
            form = RegisterContractForm(request.POST)
            if form.is_valid():
                contract_name= form.cleaned_data['contract_name']
                contract_address=form.cleaned_data['contract_address']
                contract_abi=form.cleaned_data['contract_abi']
                contract = Contract(contract_name=contract_name, contract_address=contract_address, contract_abi=contract_abi)
                contract.save()
                redirect_id=contract.id
        return detail_contract_view(request, redirect_id)
    except:
        return return_problem_page(request)



def save_metric_to_device(request, pk):
    """
    this refrences a metric to a device
    :param request: the pk of the metrics to associate with the device
    :param pk: pk of device
    :return: redirect user to mainpage
    """
    try:
        redirect_id=1
        if request.POST:
            for key, value in request.POST.items():
                if key.isdigit():
                    met = Metric.objects.get(id=key)
                    dev = Device.objects.get(id=pk)
                    dev.metrics.add(met)
                    dev.save();
                    redirect_id=dev.id
        return detail_view(request, redirect_id)
    except:
        return return_problem_page(request)


def save_template_to_device(request, pk):
    """
    saves the template to the device and db
    :param request: the template data to save
    :param pk: pk of the device
    :return: redirect user to mainpage
    """
    try:
        print('Adding a template')
        redirect_id = 1;
        if request.POST:
            device = Device.objects.get(id=pk)
            template = Template(device=device)
            template.save()
            for key, value in request.POST.items():
                if len(value) > 0:
                    if "lower:" in key or "upper:" in key:
                        metric = Metric.objects.get(id=key.strip("lower:").strip("upper:"))
                        if Threshold.objects.filter(template=template, metric=metric).exists():
                            threshold = Threshold.objects.get(template=template, metric=metric)
                            if "lower:" in key:
                                threshold.lower_trigger = value
                            if "upper:" in key:
                                threshold.upper_trigger = value
                            threshold.save()
                        else:
                            threshold = Threshold(template=template, metric=metric)
                            if "lower:" in key:
                                threshold.lower_trigger = value
                            if "upper:" in key:
                                threshold.upper_trigger = value
                            threshold.save()
                    if "template_name" in key:
                        template.template_name = value.replace(' ','')
                        template.save()
                        redirect_id=template.id
            #Estimate gas costs
            try:
                print("STARTING GAS CALCULATIONS")
                templ = Template.objects.get(id=redirect_id)
                temp_name = str(slugify(
                    templ.template_name))
                all_thres = Threshold.objects.filter(template=templ)
                #do it for threshold template

                path = create_new_smart_contract_with_thresholds(template_name=temp_name, thresholds=all_thres)
                gas_estimate=get_contract_gas(path)
                template.gas_estimate_thres=gas_estimate
                os.remove(path)
                template.save()
                #do it for none threshold template
                mets = []
                device = Device.objects.get(id=pk)

                mets_quarry = device.metrics.all()

                for met in mets_quarry:
                    mets.append(str(met.physical_property) + str(met.unit_of_measurement))
                path = create_new_smart_contract(template_name=temp_name, metrics=mets)
                template.gas_estimate_no_thres=get_contract_gas(path)
                os.remove(path)
                template.save()
            except:
                print("No Blockchain found...")
                #If node is not instaleld or blockchain is not available just add the deploy default value
                templ = Template.objects.get(id=redirect_id)
                temp_name = str(slugify(
                    templ.template_name))
                all_thres = Threshold.objects.filter(template=templ)
                #do it for threshold template

                template.gas_estimate_thres=53001
                template.save()
                #do it for none threshold template
                mets = []
                device = Device.objects.get(id=pk)
                mets_quarry = device.metrics.all()

                for met in mets_quarry:
                    mets.append(str(met.physical_property) + str(met.unit_of_measurement))
                template.gas_estimate_no_thres=53001
                template.save()
                pass
            create_new_smart_contract_with_thresholds(os.getcwd())

        return detail_template_view(request, redirect_id);
    except:
        return return_problem_page(request)



def add_metric(request):
    """
    Adds a metric to the db
    :param request: the metric data to save
    :return: 
    """
    try:
        if request.POST:
            form = RegisterMetricForm(request.POST)
            if form.is_valid():
                physical_p = form.cleaned_data['physical_property']
                unit_of_m = form.cleaned_data['unit_of_measurement']
                metric = Metric(physical_property=physical_p.replace(' ',''), unit_of_measurement=unit_of_m.replace(' ',''))
                metric.save()
        return redirect('smartpollution:index')
    except:
        return return_problem_page(request)


def add_metric_silent(request, pk):
    """
    Adds a metric to the db from add metrics to device view
    :param request: the metric data to save
    :return: 
    """
    try:
        if request.POST:
            form = RegisterMetricForm(request.POST)
            if form.is_valid():
                physical_p = form.cleaned_data['physical_property']
                unit_of_m = form.cleaned_data['unit_of_measurement']
                metric = Metric(physical_property=physical_p.replace(' ',''), unit_of_measurement=unit_of_m.replace(' ',''))
                metric.save()
        return add_metric_to_device(request, pk)
    except:
        return return_problem_page(request)