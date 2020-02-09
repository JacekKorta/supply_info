from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from warranty_parts.forms import AddCommentForm, AddIssueForm
from warranty_parts.wp_modules import db_save as wp_db_save


def add_issue(request):
    if request.method == 'POST':
        form = AddIssueForm(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
            wp_db_save.save_issues(form_input)
        return redirect('warranty_parts:add_issue')
    else:
        form = AddIssueForm()
    return render(request, 'warranty_parts/add_issue.html', {'form': form})


def add_comment(request, issue_id):
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
        return redirect('admin:warranty_parts_issues_<issue_id>_change')
    else:
        form = AddCommentForm()
    return render(request, 'warranty_parts/add_issue.html', {'form': form,
                                                             'issue_id': issue_id,
                                                             'title': 'Dodaj komentarz'})
