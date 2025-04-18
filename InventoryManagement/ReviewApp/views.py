from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AppReview

@login_required
def submit_and_list_reviews(request):
    edit_review = None

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        review_id = request.POST.get('review_id')

        if not comment:
            reviews = AppReview.objects.all()
            return render(request, 'submit_and_list.html', {
                'reviews': reviews,
                'error': 'Comment is required.',
                'edit_review': None,
            })

        if review_id:  # Update existing review
            review = AppReview.objects.filter(id=review_id, user=request.user).first()
            if review:
                review.rating = rating
                review.comment = comment
                review.save()
                messages.success(request, "Review updated successfully.")
        else:  # New review
            AppReview.objects.create(
                user=request.user,
                rating=rating,
                comment=comment
            )

            messages.success(request, "Comment Added successfully.")
            

        return redirect('submit_and_list_reviews')

    # Handle GET request
    edit_review_id = request.GET.get('edit')
    if edit_review_id:
        edit_review = AppReview.objects.filter(id=edit_review_id, user=request.user).first()

    reviews = AppReview.objects.all()
    return render(request, 'submit_and_list.html', {
        'reviews': reviews,
        'edit_review': edit_review
    })


@login_required
def delete_review(request, review_id):
    review = AppReview.objects.filter(id=review_id, user=request.user).first()
    if review:
        review.delete()
        messages.success(request, "Review deleted successfully.")
    return redirect('submit_and_list_reviews')
