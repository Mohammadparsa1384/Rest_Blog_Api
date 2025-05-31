{% extends "mail_templated/base.tpl" %}

{% block subject %}Password Reset{% endblock %}

{% block html %}
Hello {{ user.email }},

We received a request to reset your password. Click the link below to choose a new one:

<a href="{{ reset_url }}">Reset Your Password</a>

If you didn’t request this, please ignore this email.

Thanks,  
Support Team
{% endblock %}
