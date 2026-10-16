import flet as ft

def main(page: ft.Page):
    page.title = "سچاج برو - Sajjaj Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    
    PRIMARY_COLOR = "#00ADB5"
    BG_COLOR = "#222831"
    SURFACE_COLOR = "#393E46"
    TEXT_COLOR = "#EEEEEE"

    page.bgcolor = BG_COLOR

    # --- خانة 1: الصفحة الرئيسية ---
    home_content = ft.Column(
        [
            ft.Container(
                content=ft.Text("📚 أهلاً بك في سچاج برو - السادس العلمي", size=20, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                padding=15,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("🔥 الإعلانات والملازم المميزة", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.BOOK, color=PRIMARY_COLOR),
                                    title=ft.Text("ملزمة الرياضيات - السادس العلمي 2026", color=TEXT_COLOR, weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text("شرح مفصل للأستاذ المتميز + الوزاريات", color="#AAAAAA"),
                                ),
                                ft.Row([
                                    ft.TextButton("تحميل الملزمة", icon=ft.Icons.DOWNLOAD, icon_color=PRIMARY_COLOR)
                                ], alignment=ft.MainAxisAlignment.END)
                            ]),
                            padding=10
                        ),
                        color=SURFACE_COLOR
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.BOOK, color=PRIMARY_COLOR),
                                    title=ft.Text("ملزمة الفيزياء - الجزء الأول", color=TEXT_COLOR, weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text("أحدث النسخ الوزارية مع المسائل المرشحة", color="#AAAAAA"),
                                ),
                                ft.Row([
                                    ft.TextButton("تحميل الملزمة", icon=ft.Icons.DOWNLOAD, icon_color=PRIMARY_COLOR)
                                ], alignment=ft.MainAxisAlignment.END)
                            ]),
                            padding=10
                        ),
                        color=SURFACE_COLOR
                    )
                ]),
                padding=10,
            )
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    # --- خانة 2: صفحة التحميلات ---
    downloads_content = ft.Column(
        [
            ft.Container(
                content=ft.Text("📥 الملازم المحفوظة وقيد التحميل", size=20, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                padding=15,
            ),
            ft.ListView(
                expand=True,
                padding=10,
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PICTURE_AS_PDF, color=ft.Colors.RED_400),
                        title=ft.Text("ملزمة الأحياء - الفصل الأول", color=TEXT_COLOR),
                        subtitle=ft.Text("جاهزة للقراءة (تم التحميل 100%)", color=PRIMARY_COLOR),
                        trailing=ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_300)
                    ),
                    ft.Divider(color=SURFACE_COLOR),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PICTURE_AS_PDF, color=ft.Colors.RED_400),
                        title=ft.Text("ملزمة الكيمياء - العضوية", color=TEXT_COLOR),
                        subtitle=ft.Text("قيد التحميل... (65%)", color=ft.Colors.YELLOW_400),
                        trailing=ft.ProgressRing(width=20, height=20, stroke_width=2, value=0.65, value_color=PRIMARY_COLOR)
                    ),
                ]
            )
        ],
        expand=True
    )

    # --- خانة 3: الحساب والإعدادات ---
    account_content = ft.Column(
        [
            ft.Container(
                content=ft.Column([
                    ft.CircleAvatar(radius=35, content=ft.Icon(ft.Icons.PERSON, size=35, color=TEXT_COLOR), bgcolor=PRIMARY_COLOR),
                    ft.Text("طالب سادس علمي متميز", size=18, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                    ft.Text("سچاج برو - النسخة الاحترافية", size=12, color="#AAAAAA"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                alignment=ft.alignment.center
            ),
            ft.Divider(color=SURFACE_COLOR),
            ft.ListView(
                expand=True,
                controls=[
                    ft.ListTile(leading=ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, color=PRIMARY_COLOR), title=ft.Text("إشعارات الملازم والوزاريات", color=TEXT_COLOR), trailing=ft.Switch(value=True, active_color=PRIMARY_COLOR)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.DARK_MODE_OUTLINED, color=PRIMARY_COLOR), title=ft.Text("الوضع الليلي الذكي", color=TEXT_COLOR)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.INFO_OUTLINE, color=PRIMARY_COLOR), title=ft.Text("عن تطبيق سچاج برو", color=TEXT_COLOR)),
                    ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED_400), title=ft.Text("إعادة ضبط التطبيق", color=ft.Colors.RED_400)),
                ]
            )
        ],
        expand=True
    )

    body_container = ft.Container(content=home_content, expand=True)

    def on_nav_change(e):
        index = e.control.selected_index
        if index == 0:
            body_container.content = home_content
        elif index == 1:
            body_container.content = downloads_content
        elif index == 2:
            body_container.content = account_content
        page.update()

    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_nav_change,
        bgcolor=SURFACE_COLOR,
        destinations=[
            ft.NavigationDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="الرئيسية"),
            ft.NavigationDestination(icon=ft.Icons.DOWNLOAD_OUTLINED, selected_icon=ft.Icons.DOWNLOAD, label="التحميلات"),
            ft.NavigationDestination(icon=ft.Icons.PERSON_OUTLINED, selected_icon=ft.Icons.PERSON, label="الحساب والإعدادات"),
        ]
    )

    page.add(body_container)

ft.app(target=main)
