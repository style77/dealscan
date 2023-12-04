from django_components import component

from polls.models import Poll as PollModel


@component.register("poll")
class Poll(component.Component):
    template_name = "poll/poll.html"

    def get_context_data(self, selected_poll_id):
        poll_obj = PollModel.objects.get(id=selected_poll_id)
        return {"poll": poll_obj}

    class Media:
        css = [
            "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0",
            "src/output.css",
        ]
