from django.urls import path
from . import views

urlpatterns = [
    # ── Основное ──────────────────────────────────────────────────────────────
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/',           views.custom_login,    name='custom_login'),
    path('change-password/', views.change_password, name='change_password'),

    # ── Панель преподавателя ───────────────────────────────────────────────────
    path('teacher/', views.admin_panel, name='admin_panel'),
    path('teacher/approve/<int:user_id>/',    views.approve_user,    name='approve_user'),
    path('teacher/reject/<int:user_id>/',     views.reject_user,     name='reject_user'),
    path('teacher/deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('teacher/create-user/',              views.create_user,     name='create_user'),
    path('teacher/reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('teacher/rename-user/<int:user_id>/',   views.rename_user,    name='rename_user'),
    path('teacher/subject-access/<int:user_id>/', views.set_subject_access, name='set_subject_access'),
    path('teacher/bulk-subject-access/', views.bulk_subject_access, name='bulk_subject_access'),

    # ── Практические работы ───────────────────────────────────────────────────
    path('works/', views.work_list, name='work_list'),
    path('works/<int:work_id>/', views.work_detail, name='work_detail'),
    path('works/<int:work_id>/submit/', views.submission, name='work_submit'),
    path('submission/<int:work_id>/', views.submission, name='submission'),
    path('solution/<int:solution_id>/', views.solution_detail, name='solution_detail'),
    path('results/', views.results, name='results'),
    path('progress/', views.works_userprogress, name='works_userprogress'),

    # ── Профиль ───────────────────────────────────────────────────────────────
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/student/<int:user_id>/', views.student_profile, name='student_profile'),

    # ── Теория ────────────────────────────────────────────────────────────────
    path('theory/', views.theory_list, name='theory_list'),
    path('theory/lesson/<int:lesson_id>/', views.theory_lesson, name='theory_lesson'),
    path('theory/lesson/<int:lesson_id>/done/', views.mark_lesson_done, name='mark_lesson_done'),
    path('theory/lesson/<int:lesson_id>/notes/', views.save_notes, name='save_notes'),

    # ── Предметы ──────────────────────────────────────────────────────────────
    path('subject/<slug:slug>/', views.switch_subject, name='switch_subject'),

    # ── ПИД-симулятор (МДК 03.02) ────────────────────────────────────────────
    path('pid-simulator/', views.pid_simulator, name='pid_simulator'),

    # ── Симулятор схем (МПС) ───────────────────────────────────────────────────
    path('circuit/editor/',                  views.circuit_editor_free,       name='circuit_editor_free'),
    path('circuit/editor/<int:work_id>/',    views.circuit_editor,            name='circuit_editor'),
    path('circuit/save/<int:work_id>/',      views.circuit_save,              name='circuit_save'),
    path('circuit/submit/<int:work_id>/',    views.circuit_submit,            name='circuit_submit'),
    path('circuit/solution/<int:sol_id>/',   views.circuit_solution_detail,   name='circuit_solution_detail'),
    path('circuit/review/<int:sol_id>/',     views.circuit_review,            name='circuit_review'),
    path('circuit/solutions/',               views.circuit_solutions_list,    name='circuit_solutions_list'),

    # ── Объявления ────────────────────────────────────────────────────────────
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('announcements/<int:pk>/deactivate/', views.deactivate_announcement, name='deactivate_announcement'),

    # ── Тесты ─────────────────────────────────────────────────────────────────
    path('quiz/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('api/quiz/check-answer/<int:question_id>/', views.check_quiz_answer, name='check_quiz_answer'),
    path('teacher/reset-student/<int:user_id>/', views.reset_student_account, name='reset_student_account'),
    path('quiz/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('quiz/<int:quiz_id>/adaptive/', views.quiz_adaptive, name='quiz_adaptive'),
    path('quiz/<int:quiz_id>/history/', views.quiz_history, name='quiz_history'),


    # ── Уведомления ──────────────────────────────────────────────────────────────
    path('notifications/',               views.notifications_view,     name='notifications'),
    path('notifications/count/',         views.notifications_count,    name='notifications_count'),
    path('notifications/<int:notif_id>/read/', views.mark_notification_read, name='mark_notification_read'),

    # ── Рейтинг ───────────────────────────────────────────────────────────────────
    path('leaderboard/', views.leaderboard, name='leaderboard'),

    # ── Поиск по теории ───────────────────────────────────────────────────────────
    path('theory/search/', views.theory_search, name='theory_search'),

    # ── Курсовые работы ───────────────────────────────────────────────────────────
    path('teacher/coursework/',                    views.coursework_list,   name='coursework_list'),
    path('teacher/coursework/assign/',             views.coursework_assign, name='coursework_assign'),
    path('teacher/coursework/<int:cw_id>/edit/',   views.coursework_assign, name='coursework_edit'),
    path('teacher/coursework/<int:cw_id>/delete/', views.coursework_delete, name='coursework_delete'),

    # ── Журнал и ручная проверка (преподаватель) ──────────────────────────────────
    path('teacher/gradebook/',                    views.gradebook,          name='gradebook'),
    path('teacher/solutions/',                    views.teacher_solutions,  name='teacher_solutions'),
    path('teacher/grade/<int:solution_id>/',      views.manual_grade,       name='manual_grade'),

    # ── Аналитика и Excel ──────────────────────────────────────────────────────
    path('teacher/analytics/',         views.teacher_analytics,      name='teacher_analytics'),
    path('teacher/export/excel/',      views.export_gradebook_excel, name='export_gradebook_excel'),
    path('teacher/export/csv/',        views.export_gradebook_csv,   name='export_gradebook_csv'),

    # ── История решений и diff ───────────────────────────────────────────────────
    path('works/<int:work_id>/history/', views.solution_history, name='solution_history'),
    path('solutions/diff/<int:sol1_id>/<int:sol2_id>/', views.solution_diff, name='solution_diff'),

    # ── Плагиат ─────────────────────────────────────────────────────────────────
    path('teacher/plagiarism/<int:work_id>/', views.plagiarism_check, name='plagiarism_check'),

    # ── Комментарии к строкам ───────────────────────────────────────────────────
    path('teacher/line-comment/<int:solution_id>/', views.add_line_comment, name='add_line_comment'),

    # ── API ───────────────────────────────────────────────────────────────────
    path('api/session-time/', views.get_session_time, name='get_session_time'),
    path('api/activity-data/', views.get_activity_data, name='get_activity_data'),
    path('api/check-code/<int:solution_id>/', views.check_code, name='check_code'),
    path('api/check-status/<int:check_id>/', views.get_check_status, name='get_check_status'),
    path('api/test-code/<int:work_id>/', views.test_code_locally, name='test_code_locally'),
    path('api/run-code/', views.run_code_snippet, name='run_code_snippet'),
    path('api/plagiarism/<int:solution_id>/', views.check_plagiarism, name='check_plagiarism'),
    path('api/recheck-doc/<int:solution_id>/', views.recheck_doc, name='recheck_doc'),
    path('api/unlock-hint/<int:hint_id>/', views.unlock_hint, name='unlock_hint'),

    # ── Продление дедлайна ────────────────────────────────────────────────────
    path('works/<int:work_id>/request-extension/', views.request_deadline_extension, name='request_deadline_extension'),
    path('teacher/extension/<int:ext_id>/action/', views.approve_deadline_extension, name='approve_deadline_extension'),

    # ── Онлайн-песочница ──────────────────────────────────────────────────────
    path('playground/', views.playground, name='playground'),
    path('teacher/pygrid/', views.pygrid_game, name='pygrid_game'),
    path('pygrid/', views.pygrid_beta, name='pygrid_beta'),

    # ── Хранилище проектов ────────────────────────────────────────────────────
    path('projects/', views.project_list, name='project_list'),
    path('projects/new/', views.project_editor, name='project_new'),
    path('projects/<int:project_id>/', views.project_editor, name='project_editor'),
    path('api/projects/save/', views.project_save, name='project_save'),
    path('api/projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('teacher/projects/', views.teacher_projects, name='teacher_projects'),

    # ── Dev auto-reload (только при DEBUG=True) ───────────────────────────────
    path('dev-reload/', views.dev_reload, name='dev_reload'),

    # ── О проекте ─────────────────────────────────────────────────────────────
    path('about/', views.about, name='about'),

    # ── Алгоритм-визуализатор ─────────────────────────────────────────────────
    path('visualizer/', views.algo_visualizer, name='algo_visualizer'),

    # ── PyGrid лидерборд API ──────────────────────────────────────────────────
    path('api/pygrid/score/', views.pygrid_score_submit, name='pygrid_score_submit'),
    path('api/pygrid/leaderboard/', views.pygrid_leaderboard, name='pygrid_leaderboard'),

    # ── Запрос на проверку всех работ ────────────────────────────────────────
    path('api/submit-all-for-review/', views.submit_all_for_review, name='submit_all_for_review'),
    path('api/review-request/<int:rr_id>/done/', views.mark_review_done, name='mark_review_done'),
]
