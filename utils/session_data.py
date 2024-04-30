
def get_session_data(request)->dict:
    context = {}
    context['is_active'] = request.session.get('is_active',False)
    context['email'] = request.session.get('email',None)
    context['is_label'] = request.session.get('is_label',False)
    context['is_premium'] = request.session.get('is_premium',False)
    context['is_podcaster'] = request.session.get('is_podcaster',False)
    context['is_artist'] = request.session.get('is_artist',False)
    context['is_songwriter'] = request.session.get('is_songwritter',False)
    return context