from django.urls import path
from . import views

urlpatterns = [
    path('',views.login, name='login'),
    path('forgotPassword/', views.forgotPassword,name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate,name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword,name='resetPassword'),
    path('dashboard',views.dashboard, name='dashboard'),

    path('staff_home',views.staff_home, name='staff_home'),
    
    path('add_staff',views.add_staff, name='add_staff'),
    path('edit_staff/<int:id>',views.edit_staff, name='edit_staff'),
    path('save_edit_staff/<int:id>',views.save_edit_staff, name='save_edit_staff'),
    path('delete_staff/<int:id>',views.delete_staff, name='delete_staff'),
    path('orders_dta',views.orders_dta, name='orders_dta'),

    
    path('get_date_event',views.get_date_event, name='get_date_event'),
    path('view_items_orders/<int:id>',views.view_items_orders, name='view_items_orders'),

    path('filter_date_event',views.filter_date_event, name='filter_date_event'),
    path('create_event',views.create_event, name='create_event'),
    path('add_user_order/<int:id>',views.add_user_order, name='add_user_order'),
    path('prouct_list',views.prouct_list, name='prouct_list'),

    path('cart_cust_size',views.cart_cust_size, name='cart_cust_size'),
    path('cart_change_color',views.cart_change_color, name='cart_change_color'),
    path('cart_change_meterial',views.cart_change_meterial, name='cart_change_meterial'),
    path('cart_change_model',views.cart_change_model, name='cart_change_model'),
    path('save_cart/<int:id>',views.save_cart, name='save_cart'),
    path('orders_list/<int:id>',views.orders_list, name='orders_list'),
    path('filter_order',views.filter_order, name='filter_order'),
    path('filter_order_id',views.filter_order_id, name='filter_order_id'),
    path('change_order_status',views.change_order_status, name='change_order_status'),
    path('change_order_stage',views.change_order_stage, name='change_order_stage'),
    path('pending_orders',views.pending_orders, name='pending_orders'),
    path('filter_pending',views.filter_pending, name='filter_pending'),
    path('filter_pending_id',views.filter_pending_id, name='filter_pending_id'),
    path('today_orders',views.today_orders, name='today_orders'),
    path('filter_today_id',views.filter_today_id, name='filter_today_id'),
    path('change_order_status_client',views.change_order_status_client, name='change_order_status_client'),
    path('change_order_stage_client',views.change_order_stage_client, name='change_order_stage_client'),
    path('orders_list_client/<int:id>',views.orders_list_client, name='orders_list_client'),
    path('up_expect',views.up_expect, name='up_expect'),
    path('up_expect_crm',views.up_expect_crm, name='up_expect_crm'),
    path('delivery_tomorrow',views.delivery_tomorrow, name='delivery_tomorrow'),
    path('delivery_today',views.delivery_today, name='delivery_today'),
    path('order_managements',views.order_managements, name='order_managements'),
    path('orders_list_designer/<int:id>',views.orders_list_designer, name='orders_list_designer'),
    path('orders_list_designer_client/<int:id>',views.orders_list_designer_client, name='orders_list_designer_client'),
    path('get_staff_list',views.get_staff_list, name='get_staff_list'),
    path('save_assign_stage/<int:id>',views.save_assign_stage, name='save_assign_stage'),
    path('save_assign_stage_crm/<int:id>',views.save_assign_stage_crm, name='save_assign_stage_crm'),
    path('designer_section',views.designer_section, name='designer_section'),
    
    
    #########################################################################Staff Module
    path('staff_index',views.staff_index, name='staff_index'),
    path('registrations',views.registrations, name='registrations'),
    path('icons',views.icons, name='icons'),
    path('profile',views.profile, name='profile'),
    path('order_staff_designer',views.order_staff_designer, name='order_staff_designer'),
    path('edit_user_profile/<int:id>',views.edit_user_profile, name='edit_user_profile'),
    path('filter_date_event_staff',views.filter_date_event_staff, name='filter_date_event_staff'),
    path('staff_filter_order_id',views.staff_filter_order_id, name='staff_filter_order_id'),
    path('staff_filter_order_design',views.staff_filter_order_design, name='staff_filter_order_design'),
    path('staff_orders_list_designer/<int:id>',views.staff_orders_list_designer, name='staff_orders_list_designer'),
    path('staff_orders_list_designer_client/<int:id>',views.staff_orders_list_designer_client, name='staff_orders_list_designer_client'),
    path('staff_change_order_stage',views.staff_change_order_stage, name='staff_change_order_stage'),
    path('staff_change_order_stage_client',views.staff_change_order_stage_client, name='staff_change_order_stage_client'),
    path('completed_work_designer',views.completed_work_designer, name='completed_work_designer'),
    path('staff_filter_complete_design',views.staff_filter_complete_design, name='staff_filter_complete_design'),
    path('staff_filter_complete_id',views.staff_filter_complete_id, name='staff_filter_complete_id'),

    #! */*/*/*/*//*/*/*//*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/* Cutting Section - Admin
     
    path('cutting_section',views.cutting_section, name='cutting_section'),
    path('cutting_order_list',views.cutting_order_list, name='cutting_order_list'),
    path('cutting_filter_order_date',views.cutting_filter_order_date, name='cutting_filter_order_date'),
    path('cutting_filter_order_id',views.cutting_filter_order_id, name='cutting_filter_order_id'),
    path('cutting_complete_order',views.cutting_complete_order, name='cutting_complete_order'),
    path('cutting_filter_complete_order',views.cutting_filter_complete_order, name='cutting_filter_complete_order'),
    path('cutting_filter_complete_order_id',views.cutting_filter_complete_order_id, name='cutting_filter_complete_order_id'),
    ########################################################################USER MODULE
    
    
    ######################################################################################
    path('logout',views.logout, name='logout'),

]
