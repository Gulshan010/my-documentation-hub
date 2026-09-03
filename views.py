from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, RegistrationForm
from .models import ModuleContent, UserProfile


HOME_CARDS = [
    {
        'title': 'Curriculum',
        'text': 'Semester-wise structure for programming, database, networking, maths, and practical lab planning.',
        'slug': ModuleContent.MODULE_CURRICULUM,
    },
    {
        'title': 'Study Material',
        'text': 'Notes, tutorials, coding practice sheets, and revision pointers prepared for BCA students.',
        'slug': ModuleContent.MODULE_STUDY_MATERIAL,
    },
    {
        'title': 'Notification',
        'text': 'Stay updated with class notices, submission reminders, workshops, and campus announcements.',
        'slug': ModuleContent.MODULE_NOTIFICATION,
    },
    {
        'title': 'Exam',
        'text': 'Exam schedules, important question areas, internal assessment support, and final preparation flow.',
        'slug': ModuleContent.MODULE_EXAM,
    },
]

TEACHER_CARD_TITLES = {'Curriculum', 'Study Material', 'Notification'}


def home(request):
    registration_form = RegistrationForm(prefix='register')
    login_form = LoginForm(prefix='login')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'register':
            registration_form = RegistrationForm(request.POST, prefix='register')
            if registration_form.is_valid():
                role = registration_form.cleaned_data['role']
                user = User.objects.create_user(
                    username=registration_form.cleaned_data['name'],
                    password=registration_form.cleaned_data['password'],
                )
                if role == UserProfile.ROLE_ADMIN:
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                UserProfile.objects.create(
                    user=user,
                    role=role,
                    class_name=registration_form.cleaned_data['class_name'],
                )
                messages.success(request, 'Account created successfully. Please log in from the login panel.')
                return redirect('home')

        if action == 'login':
            login_form = LoginForm(request.POST, prefix='login')
            if login_form.is_valid():
                user = authenticate(
                    request,
                    username=login_form.cleaned_data['name'],
                    password=login_form.cleaned_data['password'],
                )
                if not user:
                    login_form.add_error(None, 'Invalid name or password.')
                else:
                    selected_role = login_form.cleaned_data['role']
                    if selected_role == UserProfile.ROLE_ADMIN:
                        if not user.is_staff:
                            login_form.add_error('role', 'This account is not allowed to open the admin panel.')
                        else:
                            login(request, user)
                            return redirect('/admin/')
                        return render(
                            request,
                            'portal/home.html',
                            {
                                'registration_form': registration_form,
                                'login_form': login_form,
                                'home_cards': HOME_CARDS,
                            },
                        )

                    profile = UserProfile.objects.filter(user=user).first()
                    if not profile:
                        login_form.add_error(None, 'Profile details are missing for this account.')
                    elif profile.role != login_form.cleaned_data['role']:
                        login_form.add_error('role', 'Selected role does not match this account.')
                    elif profile.role == UserProfile.ROLE_STUDENT and profile.class_name != login_form.cleaned_data['class_name']:
                        login_form.add_error('class_name', 'Class does not match this student account.')
                    else:
                        login(request, user)
                        return redirect('dashboard')

    return render(
        request,
        'portal/home.html',
        {
            'registration_form': registration_form,
            'login_form': login_form,
            'home_cards': HOME_CARDS,
        },
    )


@login_required
def dashboard(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    home_cards = HOME_CARDS
    modules_heading = 'Curriculum, study material, notification, and exam'
    access_note = 'You can access all dashboard modules.'

    if profile and profile.role == UserProfile.ROLE_TEACHER:
        home_cards = [card for card in HOME_CARDS if card['title'] in TEACHER_CARD_TITLES]
        modules_heading = 'Curriculum, study material, and notification'
        access_note = 'Teacher access includes Curriculum, Study Material, and Notification.'

    context = {
        'profile': profile,
        'department_cards': [
            {
                'title': 'BCA Overview',
                'text': 'Bachelor of Computer Applications (BCA) is a professional undergraduate course focused on computer science, software development, programming languages, database management, networking, and web technologies. This course helps students build technical knowledge, logical thinking, and practical skills required for careers in IT, software, education, and digital services.',
            },
            {
                'title': 'Tutorial',
                'text': 'Access guided learning for Python, Java, DBMS, web development, projects, and exam preparation in one place.',
            },
        ],
        'home_cards': home_cards,
        'modules_heading': modules_heading,
        'access_note': access_note,
    }
    return render(request, 'portal/dashboard.html', context)


@login_required
def module_page(request, module_slug):
    profile = UserProfile.objects.filter(user=request.user).first()
    allowed_slugs = [card['slug'] for card in HOME_CARDS]

    if profile and profile.role == UserProfile.ROLE_TEACHER:
        allowed_slugs = [
            ModuleContent.MODULE_CURRICULUM,
            ModuleContent.MODULE_STUDY_MATERIAL,
            ModuleContent.MODULE_NOTIFICATION,
        ]

    if module_slug not in allowed_slugs:
        messages.error(request, 'You do not have access to this section.')
        return redirect('dashboard')

    module_meta = next((card for card in HOME_CARDS if card['slug'] == module_slug), None)
    module_items = ModuleContent.objects.filter(module_type=module_slug)

    context = {
        'profile': profile,
        'module_meta': module_meta,
        'module_items': module_items,
    }
    return render(request, 'portal/module_page.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# Create your views here.
