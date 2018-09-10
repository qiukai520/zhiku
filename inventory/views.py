from django.shortcuts import render

# Create your views here.


def supplier_list(request):
    pass
    return render(request,'inventory/supplier_list.html')



def supplier_edit(request):
    return render(request,'inventory/supplier_edit.html')
