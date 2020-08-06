from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from warranty_parts.forms import AddCommentForm, AddIssueForm
from warranty_parts.wp_modules import db_save as wp_db_save
from warranty_parts.wp_modules import wp_emails


@staff_member_required
def add_issue(request):
    if request.method == 'POST':
        form = AddIssueForm(request.POST or None)
        if form.is_valid():
            form_input = form.cleaned_data
            issue, machine = wp_db_save.save_issues(form_input)
            wp_emails.send_new_issue_notification(issue, machine)
        else:
            form = AddIssueForm(request.POST)
            return render(request, 'warranty_parts/add_issue.html', {'form': form})
        return redirect('warranty_parts:add_issue')
    else:
        form = AddIssueForm()
    return render(request, 'warranty_parts/add_issue.html', {'form': form})


@staff_member_required
def add_comment(request, issue_id):
    current_user = request.user
    if request.method == 'POST':
        default_data = {'user': request.user}
        form = AddCommentForm(request.POST, default_data)
        if form.is_valid():
            form_input = form.cleaned_data
            comment = wp_db_save.save_comment(form_input['body'],issue_id, current_user)
            if form_input['inform_all']:
                wp_emails.send_new_comment_notification(issue_id, comment)
        return HttpResponseRedirect(reverse('admin:warranty_parts_issues_change',
                                            args=(issue_id,),
                                            current_app='warranty_parts'))
    else:
        form = AddCommentForm()
    return render(request, 'warranty_parts/add_comment.html', {'form': form,
                                                               'issue_id': issue_id,
                                                               'user': current_user,})
