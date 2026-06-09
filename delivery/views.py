from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import DeliveryAssignment

def is_delivery(user): return user.role == 'delivery'

@login_required
@user_passes_test(is_delivery)
def delivery_dashboard(request):
    profile = request.user.delivery_profile
    if not profile.is_approved:
        return render(request, 'dashboard/not_approved.html')
        
    if request.method == 'POST':
        assignment_id = request.POST.get('assignment_id')
        new_status = request.POST.get('status')
        order_status = request.POST.get('order_status')
        
        if assignment_id:
            assignment = get_object_or_404(DeliveryAssignment, id=assignment_id)
            if new_status:
                assignment.status = new_status
                if new_status in ['completed', 'delivered']:
                    assignment.completed_at = timezone.now()
                assignment.save()
            if order_status:
                assignment.order.status = order_status
                assignment.order.save()
            return redirect('delivery:dashboard')
            
    active_assignments = DeliveryAssignment.objects.filter(agent=profile).exclude(status__in=['completed', 'delivered', 'cancelled']).order_by('-assigned_at')

    context = {
        'assignments': active_assignments,
    }
    return render(request, 'delivery/dashboard.html', context)

@login_required
@user_passes_test(is_delivery)
def delivery_history(request):
    profile = request.user.delivery_profile
    if not profile.is_approved:
        return render(request, 'dashboard/not_approved.html')
        
    history_assignments = DeliveryAssignment.objects.filter(agent=profile, status__in=['completed', 'delivered', 'cancelled']).order_by('-assigned_at')

    context = {
        'history_assignments': history_assignments
    }
    return render(request, 'delivery/history.html', context)
