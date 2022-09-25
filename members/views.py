from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth.decorators import login_required

from .models import Member
from .forms import MemberForm

@login_required
def list_members(request):
    members = Member.objects.order_by('last_name').all()
    return render(request, 'members/list_members.html', {
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
            request.user.vessel.name = form.cleaned_data['boat_name']
            request.user.vessel.mmsi = form.cleaned_data['boat_mmsi']
            request.user.vessel.tracking_url = form.cleaned_data['boat_tracking_url']
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
            'boat_mmsi': request.user.vessel.mmsi,
            'boat_tracking_url': request.user.vessel.tracking_url,
        })

    return render(request, 'members/update_member.html', {'form': form})

