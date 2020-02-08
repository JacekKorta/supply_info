from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from warranty_parts.forms import AddIssueForm
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
