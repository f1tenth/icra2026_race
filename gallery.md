---
layout: page
section: gallery
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
    /*min-width: 200px; /* This is maybe not needed. */

    img {
        width: 100%;
        /*height: 100%;*/
        object-fit: cover;
        aspect-ratio: 1/1;
    }

    @media screen and (max-width: 1000px) {
        width: 29%;
    }

    @media screen and (max-width: 736px) {
        width: 45%;
    }

    @media screen and (max-width: 480px) {
        width: 90%;
        aspect-ratio: 3/2;
    }
}
</style>
{%- assign previous_collection = "" -%}
{%- assign combined_credit = "" -%}
{%- assign sorted_collections = site.collections | sort: "name" | where: "photos", true -%}
{%- for coll in sorted_collections -%}
{%- if coll.photos -%}
{%- if previous_collection != coll.name -%}
{%- unless forloop.first -%}
</div>
<div style="text-align: right; font-size: 0.6rem; margin-top: 0.5rem">{{ combined_credit }}</div>
</div>
{%- endunless -%}
# {{ coll.name }}

<div class="gallery">
<div class="gallery-flex">
{%- assign combined_credit = coll.credit | default: "" -%}
{%- else -%}
{%- if combined_credit == "" or coll.credit == "" -%}
{%- assign combined_credit = coll.credit | default: combined_credit -%}
{%- else -%}
{%- assign combined_credit = combined_credit | append: "<br />" | append: coll.credit -%}
{%- endif -%}
{%- endif -%}
{%- assign coll_oq_label = coll.label | append: "_oq" -%}
{%- assign coll_oq = site.collections | where: "label", coll_oq_label | first -%}
{% for file in coll.files %}
    {%- assign oq_available = false -%}
    {%- unless coll_oq == null -%}
        {%- assign oq_files = coll_oq.files | where: "name", file.name -%}
        {%- if oq_files.size > 0 -%}
            {%- assign oq_available = true -%}
        {%- endif -%}
    {%- endunless -%}
    {%- unless oq_available -%}
    <a class="image" {% if coll.link %}href="{{coll.link}}{{file.name}}"{% endif %} {% if coll.links and coll.links[file.basename] %}href="{{coll.links[file.basename]}}"{% endif %} target="_blank">
    {%- else -%}
    <a class="image" href="/photos_oq/{{file.name}}" target="_blank">
    {%- endunless -%}
        <img src="/photos/{{file.name}}" />
    </a>
{% endfor %}
{% if forloop.last %}
</div>
<div style="text-align: right; font-size: 0.6rem; margin-top: 0.5rem">{{ combined_credit }}</div>
</div>
{% endif %}
{%- assign previous_collection = coll.name -%}
{%- endif -%}
{%- endfor -%}

<br />

<div style="font-size: smaller">
More photos and videos are available here:

<ul>
{% assign links = "" %}
{%- for coll in sorted_collections -%}
{%- if coll.source -%}
{% unless links contains coll.source %}
{%- assign links = links | append: coll.source -%}
<li><a href="{{coll.source}}">{{coll.source}}</a></li>
{% endunless %}
{%- endif -%}
{%- endfor -%}
</ul>
</div>