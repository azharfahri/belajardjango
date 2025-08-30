from django.shortcuts import render, redirect
from django.db import connection


def home(request):
    return render(request, 'home.html')

def post_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, content, created_at FROM blog_post ORDER BY created_at DESC")
        rows = cursor.fetchall()

    # ubah hasil tuple ke dictionary
    posts = [
        {'id': row[0], 'title': row[1], 'content': row[2], 'created_at': row[3]}
        for row in rows
    ]

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, content, created_at FROM blog_post WHERE id = %s", [post_id])
        row = cursor.fetchone()

    if row:
        post = {'id': row[0], 'title': row[1], 'content': row[2], 'created_at': row[3]}
    else:
        post = None

    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO blog_post (title, content, created_at) VALUES (%s, %s, NOW())",
                [title, content]
            )

        return redirect('post_list')

    return render(request, 'blog/post_create.html')

def post_update(request, post_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, content FROM blog_post WHERE id = %s", [post_id])
        post = cursor.fetchone()

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE blog_post SET title = %s, content = %s WHERE id = %s",
                [title, content, post_id]
            )

        return redirect('post_list')

    return render(request, 'blog/post_update.html', {'post': post})


def post_delete(request, post_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM blog_post WHERE id = %s", [post_id])
    return redirect('post_list')
