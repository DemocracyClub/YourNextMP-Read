---
layout: default
hero: "Constituencies"
---
<div class="home">
{% for constituency_hash in site.data.mapit-WMC-generation-22 %}
{% assign mapit_id = constituency_hash[0] %}
{% assign constituency = constituency_hash[1] %}
<li><a href="/constituencies/{{mapit_id}}">{{constituency.name}}</a></li>
{% endfor %}
</div>
