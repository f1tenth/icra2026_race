---
layout: page
short_title: Gallery
---
<style>
div.gallery {
    margin-bottom: 3rem;
}

div.gallery-flex {
    display: flex;
    flex-flow: row wrap;
    justify-content: space-evenly;
    align-content: space-between;
    gap: 2em;
}

div.gallery a {
    width: 20%;
    min-width: 200px; /* This is maybe not needed. */

    img {
        width: 100%;
    }

    @media screen and (max-width: 1000px) {
        width: 30%;
    }

    @media screen and (max-width: 736px) {
        width: 45%;
    }
}
</style>

{%- for coll in site.collections -%}
{%- if coll.photos -%}
# {{ coll.name }}

<div class="gallery">
<div class="gallery-flex">
{% for file in coll.files %}
    <a class="image" href="{%- if coll.link -%}{{coll.link}}{{file.name}}{%- endif -%}{%- if coll.links and coll.links[file.basename] -%}{{coll.links[file.basename]}}{%- endif -%}" target="_blank">
        <img src="/photos/{{file.name}}" />
    </a>
{% endfor %}
</div>
<div style="text-align: right; font-size: 0.6rem; margin-top: 0.5rem">{{ coll.credit }}</div>
</div>

{%- endif -%}
{%- endfor -%}