from django.shortcuts import render

# Create your views here.

# Templates view

class TemplateList(generic.ListView):
    template_name = "templates/list.djhtml"
    context_object_name = "templates"

    def get_queryset(self):
        return Template.objects.exclude(deleted=True)

class TemplateView(generic.DetailView):
    model = Template
    template_name = "templates/view.djhtml"

def template_delete(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    template.deleted = True
    template.save()
    return HttpResponseRedirect(reverse('templates:index'))


# Form views
