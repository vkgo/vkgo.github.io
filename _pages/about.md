---
layout: about
title: about
permalink: /
subtitle: <a href='https://www.sysu.edu.cn/'>Sun Yat-sen University</a>. Ph.D. Student in Computer Science and Technology.

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p>Ph.D. Student</p>
    <p>Sun Yat-sen University</p>
    <p>Guangzhou, Guangdong, China</p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: true # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

I am currently a Ph.D. student at Sun Yat-sen University, specializing in Humanoid Learning and Video Action Understanding.

I have a strong interest in deep learning and computer vision, with my current research focus on temporal action understanding. I have a deep passion for all computer science things, and I aim to make significant contributions to the field through extensive and meaningful research.

Before starting my Ph.D., I was an undergraduate student at South China University of Technology studying Network Engineering. During my undergraduate studies, I was heavily involved in algorithm competitions and research internships, gaining valuable experience in AI, computer vision, natural language processing, and multimodality. I have won several awards including National Scholarship, Kaggle Silver medals, and various competition prizes.

Feel free to reach out for research collaborations or academic discussions!

## Education

{% assign edu = site.data.cv | where: 'title', 'Education' | first %}
{% if edu %}
<div class="card mt-3 p-3">
  {% assign entry = edu %}
  {% include cv/time_table.liquid %}
</div>
{% endif %}
