---
layout: page
short_title: Gallery
---
<style>
div.gallery {
    display: flex;
    flex-flow: row wrap;
    justify-content: space-evenly;
    align-content: space-between;
    gap: 2em;
}

div.gallery a {
    width: 20%;
    min-width: 200px;

    @media screen and (max-width: 736px) {
        width: 30%;
    }
}
</style>

{%- for coll in site.collections -%}
{%- if coll.photos -%}
# {{ coll.name }}

<div class="gallery">
{% for file in coll.files %}
    <a class="image" href="{{coll.link}}{{file.name}}" target="_blank">
        <img src="/photos/{{file.name}}" />
    </a>
{% endfor %}
</div>
<div style="text-align: right; font-size: 0.6rem">{{ coll.credit }}</div>

{%- endif -%}
{%- endfor -%}