from django.shortcuts import render, get_object_or_404, redirect
from products.models import Cake
from .models import Review
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def add_review(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.cake = cake
            review.save()
            messages.success(request, f"Thank you for reviewing {cake.name}!")
            return redirect('dashboard:customer')
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/add.html', {'form': form, 'cake': cake})

@login_required
def my_reviews(request):
    reviews = Review.objects.filter(customer=request.user)
    return render(request, 'reviews/my_reviews.html', {'reviews': reviews})
