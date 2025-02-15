from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Category,Comment,PostAttachment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm,CommentForm,ContactForm,PostAttachmentEditForm,PostEditForm
from django.views.decorators.http import require_POST
from django.forms import modelformset_factory
import redis
from django.conf import settings
from django.core.mail import EmailMessage


r = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)


def home(request):
    all_posts = Post.published.prefetch_related('attachments').all()[:2]
    categories = Category.objects.all()
    latest_posts = Post.published.prefetch_related('attachments').all()[:3]
    all_tags = Post.tags.all()
    context = {
        'all_posts':all_posts,
        'categories':categories,
        'latest_posts':latest_posts,
        'all_tags':all_tags
    }
    return render(request,'index.html',context)



@login_required
def base(request, category_slug=None):
    category = None
    tags = request.GET.get('tags')
    categories = Category.objects.all()
    all_posts = Post.published.prefetch_related('attachments').all()
    latest_posts = Post.published.prefetch_related('attachments').all()[:4]

    if category_slug:
        category = get_object_or_404(Category, category_slug=category_slug)
        all_posts = all_posts.filter(category=category)
    if tags:
        tag_list = tags.split(',')
        posts = posts.filter(tags__name__in=tag_list).distinct()
    

    paginator = Paginator(all_posts, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category': category,
        'all_posts': all_posts,
        'categories': categories,
        'latest_posts': latest_posts,
        'selected_tags': tags.split(',') if tags else []

    }

    return render(request, 'base.html', context)


@login_required
def post_detail(request,id):
    form = CommentForm(request.POST)
    user_key = f"user:{request.user.id}" if request.user.is_authenticated else f"anon:{request.session.session_key}"
    post_views_key = f'post:{id}:views'
    r.sadd(post_views_key,user_key)
    views = r.scard(post_views_key)
    post = get_object_or_404(Post,id=id,status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('post:detail',id=post.id)
    return render(request,'detail.html',{'post':post,'form':form,'comments':comments,'views':views})



@login_required
def create_post(request):
    
    AttachmentFormSet = modelformset_factory(
        PostAttachment,
        fields=('photo', 'caption'), 
        extra=3,
    )
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        attachment_formset = AttachmentFormSet(request.POST, request.FILES, queryset=PostAttachment.objects.none())
        if post_form.is_valid() and attachment_formset.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            for form in attachment_formset:
                if form.cleaned_data:
                    attachment = form.save(commit=False)
                    attachment.post = post
                    attachment.save()
            return redirect(post.get_absolute_url())
    else:
        post_form = PostForm()
        attachment_formset = AttachmentFormSet(queryset=PostAttachment.objects.none())
    return render(request, 'postform.html', {
        'post_form': post_form,
        'attachment_formset': attachment_formset,
    })



def about(request):
    return render(request,'about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            full_message = (
                f"Сообщение от: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
                f"{form.cleaned_data['message']}"
            )

            email = EmailMessage(
                subject=form.cleaned_data['subject'],
                body=full_message,
                from_email=settings.EMAIL_HOST_USER,  # адрес вашего аккаунта
                to=[settings.EMAIL_HOST_USER],          # письмо придёт к вам
                reply_to=[form.cleaned_data['email']],  # при ответе письмо пойдёт на email пользователя
            )
            email.send(fail_silently=False)
            return redirect('post:contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

@login_required
def post_edit_form(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author == request.user and request.method == 'POST':
        post_form = PostEditForm(request.POST, instance=post)
       
        attachment = post.attachments.first()  
        attachment_form = PostAttachmentEditForm(request.POST, request.FILES, instance=attachment)

        if post_form.is_valid() and attachment_form.is_valid():
            post_form.save()
            attachment_form.save() 
            return redirect('post:detail', id=post.id)
    else:
        post_form = PostEditForm(instance=post)
       
        attachment = post.attachments.first() 
        attachment_form = PostAttachmentEditForm(instance=attachment)

    return render(request, 'edit_postform.html', {'post_form': post_form, 'attachment_form': attachment_form, 'post': post})
