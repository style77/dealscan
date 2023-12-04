import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import View
from .models import PollAnswer, Poll
from django.contrib.auth.mixins import LoginRequiredMixin


class SubmitAnswerView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user

        body = json.loads(request.body.decode('utf-8'))

        poll_id = body.get('poll_id')
        answer_text = body.get('answer')
        if len(answer_text) <= 3:
            return JsonResponse({'status': 'error', 'message': 'Answer needs to be longer than 3 characters.'}, status=400)

        poll = get_object_or_404(Poll, pk=poll_id)

        if PollAnswer.objects.filter(user=user, poll=poll).exists():
            return JsonResponse({'status': 'error', 'message': 'You have already answered this poll.'}, status=400)

        answer = PollAnswer.objects.create(user=user, poll=poll, answer=answer_text)
        return JsonResponse({'status': 'success', 'message': 'Answer submitted successfully.'})
