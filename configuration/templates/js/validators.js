{% for name, opts in validators.items %}
{% if opts.type == 'regex' %}

$(function() {
    $.validator.addMethod('{{ name }}Checker', function(value) {
	var rule = "{{opts.regex}}";
	return value.match(rule);
    }, '{{ opts.error }}');
});
{% endif %}
{% endfor %}
    $(function() {
	$.validator.addClassRules({
      {% for name, opts in validators.items %}
      {% if opts.type == 'range' %}

      {{ opts.css_class }}: {
			range: [{{ opts.start }}, {{ opts.end }}]
		    },
      {% elif opts.type == 'regex' %}

      {{ opts.css_class }}: {
          {{ name }}Checker: true
		  },
      {% endif %}
      {% endfor %}
	})
    });
