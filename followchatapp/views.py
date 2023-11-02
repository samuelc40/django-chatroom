from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import login, authenticate, logout
from .models import *
from .forms import ChatMessageForm
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json



# Create your views here.



@login_required(login_url='login')
def index(request):
    context = {}

    try:
        user_profile = Profile.objects.get(user=request.user)
        context['user_profile'] = user_profile

        # Get the user objects of the user's friends
        user_friends = user_profile.friends.all()

        all_users = Profile.objects.all()

        # Exclude users who are friends from suggested friends
        suggested_friends = get_user_model().objects.exclude(id__in=user_friends).exclude(id=request.user.id)

        friend_requests = FriendRequest.objects.filter(receiver__in=suggested_friends, sender=request.user)
        request_count = FriendRequest.objects.filter(receiver=request.user, seen=False)
        friends = user_profile.friends.all()
        count_friends = friends.count()

        # notifications = Notification.objects.filter(receiver=request.user, sender__in=suggested_friends)
        notifications = request_count
        notifications_count = notifications.count()


        context['friends'] = friends
        context['s_friends'] = suggested_friends
        context['f_requests'] = friend_requests
        context['req_count'] = request_count.count()
        context['c_friends'] = count_friends
        context['notifications'] = notifications
        context['not_count'] = notifications_count

    except ObjectDoesNotExist:
        pass

    print("Suggested Friends:", suggested_friends)
    print("Request Count:", request_count)
    print("Context Request Count:", context['req_count'])
    print('notification_count:', context['not_count'])

    return render(request, 'interface.html', context)



def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'register.html', context)



def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    error_msg = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_msg = 'Invalid Credentials...!'
    context = {'msg': error_msg}
    return render(request, 'login.html', context)



@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def update_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # if request.user.username in profile:
            #     raise 
            form.save()
            return redirect('update')
    context = {'form': form, 'profile': profile}
    return render(request, 'update.html', context)



@login_required(login_url='login')
def friend_suggestions(request):
    context = {}

    try:
        user_profile = Profile.objects.get(user=request.user)
        context['user_profile'] = user_profile

        # Get the user objects of the user's friends
        user_friends = user_profile.friends.all()

        # Exclude users who are friends from suggested friends
        suggested_friends = get_user_model().objects.exclude(id__in=user_friends).exclude(id=request.user.id)

        friend_requests = FriendRequest.objects.filter(receiver__in=suggested_friends, sender=request.user)


        context['friends'] = user_friends
        context['s_friends'] = suggested_friends
        context['f_requests'] = friend_requests

    except ObjectDoesNotExist:
        pass

    return render(request, 'friend-suggestions.html', context)



@login_required(login_url='login')
def friend_request(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    friend_requests = FriendRequest.objects.filter(receiver = user)
    count_requests = friend_requests.count()
    context = {'f_requests': friend_requests, 'user_profile': user_profile, 'c_requests': count_requests}
    return render(request, 'friend-request.html', context)



@login_required(login_url='login')
def sent_friend_request(request):
    data = json.loads(request.body)
    user = get_user_model()
    receiver = user.objects.get(id = data)
    friend_request = FriendRequest.objects.create(sender=request.user, receiver=receiver)
    return JsonResponse("it is giving", safe=False)



@login_required(login_url='login')
def accept_friend_request(request):
    id = json.loads(request.body)
    user_id = id
    user = get_user_model()
    n_user = user.objects.get(id=user_id)
    profile = Profile.objects.get(user_id=request.user.id)
    profile2 = Profile.objects.get(user_id=user_id)
    f_request = FriendRequest.objects.get(sender=n_user, receiver=request.user)
    msg = None

    if profile:

        if profile.friends.filter(id=user_id).exists():
            profile.friends.remove(n_user)
            msg = "no"

        else:
            profile.friends.add(n_user)
            f_request.delete()
            notification = Notification.objects.create(sender=request.user, receiver=n_user, description=f"Hi, {request.user.username} accepted your friend request.")

            msg = "yes"

    if profile2:

        if profile2.friends.filter(id=request.user.id).exists():
            profile2.friends.remove(request.user)

        else:
            profile2.friends.add(request.user)

    return JsonResponse(msg, safe=False)

# @login_required(login_url='login')
# def detail(request, pk):
#     try:
#         friend = get_object_or_404(Friend, profile_id=pk)
#     except Http404:  # Use Http404 here
#         return render(request, 'error_template.html', {'error_message': 'Friend not found'})

#     # The rest of your code remains the same
#     user_profile = request.user.profile
#     context = {
#         "user_profile": user_profile,
#         "friend_profile": friend.profile,
#         "friend": friend,
#     }

#     # The rest of your code remains the same
#     chats = ChatMessage.objects.all()
#     rec_chats = ChatMessage.objects.filter(msg_sender=friend.profile, msg_receiver=user_profile, seen=False)
#     rec_chats.update(seen=True)

#     form = ChatMessageForm()

#     if request.method == "POST":
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             chat_message.msg_sender = user_profile
#             chat_message.msg_receiver = friend.profile
#             chat_message.save()
#             return redirect("detail", pk=friend.profile.id)

#     context["form"] = form
#     context["chats"] = chats
#     context["num"] = rec_chats.count()

#     return render(request, "chat.html", context)


from django.http import Http404

@login_required(login_url='login')
def detail(request, pk):
    try:
        # Attempt to retrieve the Profile object using the provided 'pk'
        user = request.user
        user_profile = Profile.objects.get(user=user)
        profile_to_add_as_friend = Profile.objects.get(id=pk)
        # correct_timezone = timezone.utc
        # ChatMessage.objects.all().update(created=correct_timezone)
    except Profile.DoesNotExist:
        # Handle the case where the Profile object does not exist
        raise Http404("Profile not found")

    # Get the user's Profile object
    

    # Check if the user is already friends with the profile_to_add_as_friend
    if not user_profile.friends.filter(id=profile_to_add_as_friend.user.id).exists():
        user_profile.friends.add(profile_to_add_as_friend.user)

    # Rest of your code to handle chat messages, etc.

    friend = profile_to_add_as_friend

    # Now, you can access the user's friends using user_profile.friends
    user_friends = user_profile.friends.all()

    chats = ChatMessage.objects.all()
    user = user_profile

    rec_chats = ChatMessage.objects.filter(msg_sender=friend, msg_receiver=user, seen=False)
    rec_chats.update(seen=True)

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = friend
            chat_message.save()
            return redirect('detail', pk=friend.id)

    form = ChatMessageForm()

    context = {
        'friend': profile_to_add_as_friend,
        'form': form,
        'user': user,
        'chats': chats,
        'user_friends': user_friends,  # Include user's friends in the context
    }
    return render(request, "chat.html", context)



def sendMessage(request, pk):
    user = Profile.objects.get(user=request.user)
    profile = Profile.objects.get(id=pk)
    friend = Profile.objects.get(id=profile.id)
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=friend, seen=False)
    print(new_chat)
    return JsonResponse(new_chat_message.body, safe=False)



def receiveMessage(request, pk):
    user = Profile.objects.get(user=request.user)
    profile = Profile.objects.get(id=pk)
    friend = Profile.objects.get(id=profile.id)
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=friend, msg_receiver=user)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)


@login_required(login_url='login')
def chatNotification(request):
    user = Profile.objects.get(user=request.user)
    # profiles = Profile.objects.get(user=user)
    friends = user.friends.all()
    arr = []
    for friend in friends:
        chats = ChatMessage.objects.filter(msg_sender=friend.profile.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)

