from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth.decorators import login_required

from .models import Member
from .forms import MemberForm

@login_required
def member_detail(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    return render(request, 'members/detail.html', {
        'member': member
    })

@login_required
def list_members(request):
    members = Member.objects.order_by('last_name').all()
    return render(request, 'members/list.html', {
        'members': members
    })

@login_required
def update_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.phone_number = form.cleaned_data['phone_number']
            request.user.website = form.cleaned_data['website']
            request.user.instagram_url = form.cleaned_data['instagram_url']
            request.user.facebook_url = form.cleaned_data['facebook_url']
            request.user.privacy_mode = form.cleaned_data['privacy_mode']
            request.user.vessel.name = form.cleaned_data['boat_name']
            request.user.vessel.make_and_model = form.cleaned_data['make_and_model']
            request.user.vessel.year_built = form.cleaned_data['year_built']
            request.user.vessel.mmsi = form.cleaned_data['boat_mmsi']
            request.user.vessel.tracking_url = form.cleaned_data['boat_tracking_url']
            request.user.vessel.privacy_mode = form.cleaned_data['boat_privacy_mode']
            request.user.vessel.save()
            request.user.save()
            return HttpResponseRedirect(reverse('update_member'))

    else:
        member = get_object_or_404(Member, id=request.user.id)
        form = MemberForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone_number': request.user.phone_number,
            'website': request.user.website,
            'instagram_url': request.user.instagram_url,
            'facebook_url': request.user.facebook_url,
            'boat_name': request.user.vessel.name,
            'make_and_model': request.user.vessel.make_and_model,
            'year_built': request.user.vessel.year_built,
            'boat_mmsi': request.user.vessel.mmsi,
            'boat_tracking_url': request.user.vessel.tracking_url,
            'privacy_mode': request.user.privacy_mode,
            'boat_privacy_mode': request.user.vessel.privacy_mode
        })

    return render(request, 'members/update.html', {'form': form})

