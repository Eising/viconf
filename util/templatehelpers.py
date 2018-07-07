def abbr_on_template(template_text, template_tags):
    text = template_text
    for tag, value in template_tags.items():
        text = template_text.replace("{{" + tag + "}}", "<abbr title=\"" + value + "\">{{" + tag + "}}</abbr>")
    text = text.replace("\n", "<br>")

    return text
