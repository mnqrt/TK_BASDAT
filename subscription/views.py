from django.shortcuts import render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from utils.session_data import get_session_data

def show_offers(request):
    context = get_session_data(request)
    query_str = "SELECT * FROM paket"
    hasil = query(query_str)
    
    return render(request, 'landing/index.html', {'konten': hasil, 'context':context})

@csrf_exempt
def payment_page(request,jenis):
    context = get_session_data(request)
    query_str = f"SELECT harga FROM paket WHERE jenis='{jenis}'"
    hasil = query(query_str)
    return render(request, 'landing/payment.html', {'jenis': jenis, 'harga': hasil[0]['harga'], 'context':context})