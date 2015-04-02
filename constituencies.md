---
layout: default
hero: "Constituencies"
---
<div class="home">
{% for constituency_hash in site.data.constituencies.id %}
  {% assign mapit_id = constituency_hash[1][0] %}
  {% assign constituency = constituency_hash[1][0] %}
  <li><a href="/constituencies/{{mapit_id}}">{{constituency.name}}</a></li>
{% endfor %}
</div>
