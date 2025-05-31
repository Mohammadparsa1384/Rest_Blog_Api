{% extends "mail_templated/base.tpl" %}

{% block subject %}Activate Your Account{% endblock %}

{% block html %}
Hello {{ user.email }},

Please activate your account by clicking the link below:

<a href="{{ activation_url }}">Activate Account</a>

If you did not request this email, please ignore it.

Thanks,  
Support Team
{% endblock %}
