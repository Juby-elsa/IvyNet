import os

def write_template(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip())
    print(f"Successfully wrote {path}")

# Community Feed Template
community_content = """{% extends 'base.html' %}
{% block content %}
<div class="row mb-5 animate-fade-in">
    <div class="col-lg-8">
        <h1 class="display-4 fw-bold mb-3 text-dark">Academic <span style="color: #007bff;">Community</span></h1>
        <p class="lead text-secondary">Connect with fellow researchers and students across the IvyNet network.</p>
    </div>
    <div class="col-lg-4 d-flex align-items-center justify-content-end">
        <a href="{% url 'create_post' %}" class="btn btn-primary py-2 px-4 rounded-pill fw-bold">
            <i class="bi bi-pencil-square me-1"></i> Start a Discussion
        </a>
    </div>
</div>

<div class="row">
    {% for post in posts %}
    <div class="col-lg-12 mb-4">
        <div class="bg-white p-4 rounded-4 border shadow-sm">
            <div class="d-flex align-items-center mb-3">
                <div class="rounded-circle bg-light border border-primary d-flex align-items-center justify-content-center fw-bold me-3 text-primary" style="width: 45px; height: 45px;">
                    {{ post.author.user.username|first|upper }}
                </div>
                <div>
                    <h6 class="fw-bold mb-0 text-dark">{{ post.author.user.username }}</h6>
                    <small class="text-muted">{{ post.created_at|timesince }} ago in {{ post.author.get_domain_interest_display }}</small>
                </div>
            </div>
            <p class="text-secondary mb-4">{{ post.content }}</p>
            <div class="d-flex gap-4 pt-3 border-top">
                <a href="{% url 'like_post' post.pk %}" class="text-decoration-none text-muted small fw-bold"><i class="bi bi-heart me-1"></i> {{ post.likes.count }} Likes</a>
                <a href="#" class="text-decoration-none text-muted small fw-bold"><i class="bi bi-chat me-1"></i> {{ post.comments.count }} Comments</a>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12 text-center py-5">
        <div class="bg-white p-5 rounded-4 border border-dashed">
            <h4 class="text-muted">No community discussions yet. Be the first to start one!</h4>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}"""

write_template('templates_secure/community/feed.html', community_content)
