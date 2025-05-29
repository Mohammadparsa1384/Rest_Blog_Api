{% extends "mail_templated/base.tpl" %}

{% block subject %}Activate Your Account{% endblock %}

{% block html %}
Hello {{ user.username }},

Please activate your account by clicking the link below:

<a href="http://127.0.0.1:8000/accounts/api/v1/activation/confirm/?token={{ token }}">Activate Account</a>

If you did not request this email, please ignore it.

Thanks,  
Support Team
{% endblock %}
