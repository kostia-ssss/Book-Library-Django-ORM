from django.shortcuts import render, redirect

from schedule.models import *

def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    # Доступные книги (статус = 'a')
    num_authors=Author.objects.count()  
    num_readers=Reader.objects.count() # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_authors':num_authors,'num_readers':num_readers},
    )

def read(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    readers = Reader.objects.all()

    loans = [str(l) for l in Loan.objects.all()]

    context = {
        'books': books,
        'authors': authors,
        'readers': readers,
        'loans': loans,
    }

    return render(request, 'read.html', context)

def add(request):

    books = Book.objects.all()
    readers = Reader.objects.all()

    if request.method == "POST":

        form_type = request.POST.get("type")

        # ---------- BOOK ----------
        if form_type == "book":

            Book.objects.create(
                name=request.POST.get("name"),
                description=request.POST.get("desc")
            )

            return redirect("add")

        # ---------- AUTHOR ----------
        elif form_type == "author":

            book = Book.objects.get(id=request.POST.get("book"))

            Author.objects.create(
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                book=book
            )

            return redirect("add")

        # ---------- READER ----------
        elif form_type == "reader":

            Reader.objects.create(
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name")
            )

            return redirect("add")

        # ---------- LOAN ----------
        elif form_type == "loan":

            book = Book.objects.get(id=request.POST.get("book"))
            reader = Reader.objects.get(id=request.POST.get("reader"))

            Loan.objects.create(
                book=book,
                reader=reader
            )

            return redirect("add")

    return render(
        request,
        "add.html",
        context={
            "books": books,
            "readers": readers
        }
    )

def edit(request):

    books = Book.objects.all()
    readers = Reader.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":

        form_type = request.POST.get("type")

        # ---------- BOOK ----------
        if form_type == "book":

            b = Book.objects.get(name=request.POST.get("old_name"))
            b.name = request.POST.get("name")
            b.description = request.POST.get("desc")
            b.save()

            return redirect("edit")

        # ---------- AUTHOR ----------
        elif form_type == "author":

            b = Book.objects.get(id=request.POST.get("book"))

            a = Author.objects.get(first_name=request.POST.get("old_first_name"))
            a.first_name = request.POST.get("first_name")
            a.last_name = request.POST.get("last_name")
            a.book = b
            a.save()

            return redirect("edit")

        # ---------- READER ----------
        elif form_type == "reader":

            r = Reader.objects.get(first_name=request.POST.get("old_first_name"))
            r.first_name = request.POST.get("first_name")
            r.last_name = request.POST.get("last_name")
            r.save()

            return redirect("edit")

    return render(
        request,
        "edit.html",
        context={
            "books": books,
            "readers": readers
        }
    )