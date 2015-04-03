---
layout: default
hero: "Constituencies"
---
<div class="home">
{% for constituency_hash in site.data.constituencies.id %}
  {% assign mapit_id = constituency_hash[0] %}
  {% assign constituency = constituency_hash[1] %}
  <li><a href="/constituency/{{mapit_id}}/{{constituency['mapit']['name']| slugify}}">
      {{constituency['mapit']['name'] }}
  </a></li>
{% endfor %}
</div>
