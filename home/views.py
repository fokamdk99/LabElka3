from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from home.models import Semestr, Przedmiot, Test, Post, Attachment


from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        print(f"index: nie ma takiego uzytkownika")
        #return render(request, "home/index.html")
        return render(request, "home/login.html")
    else:
        print(f"index: uzytkownik istnieje, profession: {request.user.profession}")
        posts = Post.objects.all()
        semesters = Semestr.objects.all()
        usr = request.user
        znajomi = usr.znajomi.all()
        do_wykreslenia = usr.znajomi.all().values('username')
        people = User.objects.all().exclude(username=request.user).order_by('username')
        people = people.exclude(username__in=do_wykreslenia)
        #konwersacje = usr.konwersacja_set.all()
        for idx, semestr in enumerate(semesters):
            print(f"{idx} -> {semestr}")

        #return render(request, "home/user_homepage.html", {"user":request.user, "posts":posts, "semesters":semesters, "people":people, 'znajomi':znajomi})
        return render(request, "home/homepage.html", {"user":request.user, "posts":posts, "semesters":semesters, "people":people, 'znajomi':znajomi})

def upload_post(request, przedmiot, test):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            test = test.replace("-", " ")
            #print(f"upload_post: test wynosi {test}, przedmiot wynosi {przedmiot}, cleaned wynosi: {form.cleaned_data['test']}")
            szukany_przedmiot = Przedmiot.objects.get(subject_name = przedmiot)
            if szukany_przedmiot is not None:
                testy = szukany_przedmiot.testy_z_danego_przedmiotu.all()
                szukany_test = testy.get(test_name=test)
                #nazwa = [x.strip() for x in szukany_test.test_name.split(',')]
                #nazwa = przedmiot + ", " + test
                print(f"nazwa wyszukanego testu: {szukany_test.test_name}")
                #form.cleaned_data['test'] = szukany_test
                #print(f"form cleaned data type: {form.cleaned_data['test'].test_name}, przykladowo cleaned title: {form.cleaned_data['title']}")
                #foremka = form.save(commit = False)
                #foremka.test = szukany_test
                #foremka.save()
                new_post = Post(title=form.cleaned_data['title'], content=form.cleaned_data['content'], attachment = form.cleaned_data['attachment'], test = szukany_test)
                new_post.save()
                return redirect('index')
    else:
        form = PostForm()
        print(f"upload_post: wysylam forme")
        return render(request, 'labelka/upload_post.html', {'form': form})


def upload_post1(request):
    print(f"wchodze w upload_post1")
    if request.method=="POST":
        print(f"jestem w poscie")
        author = request.user
        przedmiocik = request.POST['new-post-przedmiot']
        przedmiot = Przedmiot.objects.get(subject_name=przedmiocik)
        tescik = request.POST['new-post-test']
        test = przedmiot.testy_z_danego_przedmiotu.get(test_name=tescik)
        title=request.POST['new-post-title']
        content=request.POST['new-post-content']
        files = request.FILES.getlist('new-post-attachments')
        print(f"{request.FILES}")
        print(f"autor: {author.username}, tytul: {title}, zawartosc: {content}, test: {tescik}")
        post = Post(author=request.user, title=title, content=content, test=test)
        post.save()
        
        for f in files:
            file=Attachment(att=f, post=post)
            print(f"nazwa pliku: {file.att.name}, url: {file.att.url}")
            file.save()
        return redirect('index')

def semester(request, number):
    print(f"python semester: otrzymalem numer {number}")
    
    semestr = Semestr.objects.get(number=number)
    przedmioty = []
    #for przedmiot in semestr.przedmiot_set.all():
    for przedmiot in semestr.przedmioty_z_danego_semestru.all():
        przedmioty.append(przedmiot.subject_name)

    for przedmiot in przedmioty:
        print(f"nazwa przedmiotu: {przedmiot}")
    #return HttpResponse(f"content nr {number}")
    return JsonResponse(przedmioty, safe=False)

def przedmiot(request, number, nazwa):
    print(f"python przedmiot: otrzymalem numer {number}, nazwa: {nazwa}")

    przedmiot = Przedmiot.objects.get(subject_name=nazwa)
    tests = []
    #for test in przedmiot.test_set.all():
    for test in przedmiot.testy_z_danego_przedmiotu.all():
        tests.append(test.test_name)
    for test in tests:
        print(f"nazwa testu: {test}")

    return JsonResponse(tests, safe=False)

def posts(request, number, nazwa, test):
    print(f"python posts: otrzymalem numer {number}, nazwa: {nazwa}, test: {test}")
    test = test.replace("-", " ")
    print(f"nowa nazwa testu: {test}")
    przedmiot = Przedmiot.objects.get(subject_name=nazwa)
    testy=przedmiot.testy_z_danego_przedmiotu.all()
    for pojedynczy_test in testy:
        if(pojedynczy_test.test_name==test):
            szukany_test=pojedynczy_test
    if szukany_test is not None:
        posty = szukany_test.posty_z_danego_testu.all()
    else:
        print(f"nie znaleziono testu")
    #egzamin = Test.objects.get(test_name = test)

    posts = []

    for post in posty:
        attachments = []
        atts = post.attachments.all()
        for i in atts:
            attachments.append(i.att.url)
        content = {'author':post.author.username, 'title':post.title, 'content':post.content, 'attachments':attachments, 'date':post.date}
        print(f"views.posts --- zawartosc: {post.title}, {post.content}, {post.date}")
        posts.append(content)
    #for post in egzamin.post_set.all():
     #   posts.append(post.content)
    
    return JsonResponse(posts, safe=False)