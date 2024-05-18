from django.shortcuts import render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from utils.session_data import get_session_data
from django.http import HttpResponse, QueryDict
import datetime;
from dateutil.relativedelta import relativedelta
import uuid

MAP_TYPE = {'1 bulan':1,
            '3 bulan':3,
            '6 bulan':6,
            '1 tahun':12}

def show_offers(request):
    context = get_session_data(request)
    query_str = "SELECT * FROM paket"
    hasil = query(query_str)
    
    return render(request, 'landing/index.html', {'konten': hasil, 'context':context})

@csrf_exempt
def payment_page(request,jenis):
    context = get_session_data(request)
    jenis = jenis.replace("%20"," ")
    query_str = f"SELECT harga FROM paket WHERE jenis='{jenis}'"
    hasil = query(query_str)
    return render(request, 'landing/payment.html', {'jenis': jenis, 'harga': hasil[0]['harga'], 'context':context})

@csrf_exempt
def process(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = QueryDict(body_unicode)
        
        
        
        # Insert into
        price = body_data.get('price')
        pay_type = body_data.get('type')
        method = body_data.get('method')
        email = body_data.get('email')
        
        month = MAP_TYPE[pay_type]
        start_date = datetime.datetime.now().replace(microsecond=0)
        end_date = start_date + relativedelta(months=month)

        query_check_premium =  f"SELECT is_premium_user('{email}');"
        active = query(query_check_premium)
       
        if not active.pop()['is_premium_user']:
            query_insert_transaction = f"""INSERT INTO TRANSACTION (
                                            id, 
                                            jenis_paket, 
                                            email, 
                                            timestamp_dimulai, 
                                            timestamp_berakhir, 
                                            metode_bayar, 
                                            nominal
                                        ) VALUES (
                                            '{str(uuid.uuid4())}', 
                                            '{pay_type}', 
                                            '{email}', 
                                            '{start_date}', 
                                            '{end_date}', 
                                            '{method}', 
                                            {int(price)}
                                        );"""
            
            query_insert_premium =  f"INSERT INTO PREMIUM (email) VALUES ('{email}');"
            query(query_insert_premium)
            query(query_insert_transaction)
            request.session["is_premium"] = True
            return HttpResponse("Payment Success", status=200)
        else:
            return HttpResponse("User telah premium!", status=400)
    else:
        return HttpResponse("Payment failed", status=400)