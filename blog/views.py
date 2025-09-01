from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.contrib import messages
from .forms import PostForm
from .models import Post



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
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Postingan berhasil dibuat")
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)  # cari post berdasarkan id/primary key
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)  # pake instance biar edit bukan bikin baru
        if form.is_valid():
            form.save()
            messages.success(request, "Postingan berhasil diupdate")
            return redirect('post_list')  # balik ke daftar post setelah update
    else:
        form = PostForm(instance=post)  # tampilkan data lama di form

    return render(request, 'blog/post_update.html', {'form': form})


def post_delete(request, post_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM blog_post WHERE id = %s", [post_id])
        messages.error(request, "Postingan berhasil dihapus")
    return redirect('post_list')
