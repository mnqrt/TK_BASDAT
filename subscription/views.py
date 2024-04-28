from django.shortcuts import render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
def show_offers(request):
    query_str = "SELECT * FROM paket"
    hasil = query(query_str)
    print(hasil)
    return render(request, 'landing/index.html', {'konten': hasil})

@csrf_exempt
def payment_page(request,jenis):
    query_str = f"SELECT harga FROM paket WHERE jenis='{jenis}'"
    hasil = query(query_str)
    return render(request, 'landing/payment.html', {'jenis': jenis, 'harga': hasil[0]['harga']})