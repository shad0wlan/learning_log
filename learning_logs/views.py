from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.
# the request is the request parmater from the user ex ../index.html. Django begins from urls.py and comes
# here and executes this function
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')  # It takes the request object and what to show to the user


@login_required  # When user is logged in the request we get, has a request.user attribute that has user info
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by(
        'date_added')  # We query the database table User Topic items
    context = {'topics': topics}  # We create a dictionary
    # print(context['topics'][0])
    return render(request, 'learning_logs/topics.html',
                  context)  # We render the template by sending the dictionary info and then html can use a for loop to iterate the topics key array


# When building a page that uses data, we call
# render() with the request object, the template we want to use, and the
# context dictionary
@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)  # Get specific topic
    # Make sure the topic belongs to the current user.
    if check_topic_owner(topic, request):
        entries = topic.entry_set.order_by(
            '-date_added')  # Get the entry lower case class object, minus in date means reversed
        context = {'topic': topic, 'entries': entries}
        return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic."""
    # We use get to read from server and post to submit information
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)  # Create a form object
        if form.is_valid():  # Validate it based on database, and check if all fields are completed
            new_topic_form = form.save(commit=False)  # Creating the topic with null owner
            new_topic_form.owner = request.user  # Add the owner
            new_topic_form.save()  # Save it (write the data to database directly. The mapping is auto

            return redirect('learning_logs:topics')  # redirect the user to the topics
    # Display a blank or invalid form if it is get request.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid() and request.user == topic.owner:
            new_entry_form = form.save(commit=False)  # save to a variable first
            new_entry_form.topic = topic  # connect it with the correct topic id since it doesnt have a topic id yet
            new_entry_form.save()  # save to database
            return redirect('learning_logs:topic', topic_id=topic_id)
    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)  # Take the id object from the post
    topic = entry.topic
    if check_topic_owner(topic, request):
        if request.method != 'POST':
            # Initial request; pre-fill form with the current entry.
            form = EntryForm(instance=entry)  # Prefill the form with the existing data
        else:
            # POST data submitted; process data.
            form = EntryForm(instance=entry, data=request.POST)
            if form.is_valid() and request.user == topic.owner:
                form.save()
                return redirect('learning_logs:topic', topic_id=topic.id)
        context = {'entry': entry, 'topic': topic, 'form': form}
        return render(request, 'learning_logs/edit_entry.html', context)


def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404
    return True
