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

    path('payment_pending_orders',views.payment_pending_orders, name='payment_pending_orders'),
    path('filter_payment_pending',views.filter_payment_pending, name='filter_payment_pending'),
    path('filter_payment_pending_id',views.filter_payment_pending_id, name='filter_payment_pending_id'),
    path('payment_completed_crm/<int:id>',views.payment_completed_crm, name='payment_completed_crm'),
    path('payment_completed_client/<int:id>',views.payment_completed_client, name='payment_completed_client'),

    path('pending_orders_mang',views.pending_orders_mang, name='pending_orders_mang'),
    path('filter_pending_orders',views.filter_pending_orders, name='filter_pending_orders'),
    path('filter_pending_orders_id',views.filter_pending_orders_id, name='filter_pending_orders_id'),

    path('designer_section',views.designer_section, name='designer_section'),
    path('filter_designing_orders',views.filter_designing_orders, name='filter_designing_orders'),
    path('filter_designing_orders_id',views.filter_designing_orders_id, name='filter_designing_orders_id'),

    path('cutting_section',views.cutting_section, name='cutting_section'),
    path('filter_cutting_orders',views.filter_cutting_orders, name='filter_cutting_orders'),
    path('filter_cutting_orders_id',views.filter_cutting_orders_id, name='filter_cutting_orders_id'),

    path('stiching_section',views.stiching_section, name='stiching_section'),
    path('filter_stiching_orders',views.filter_stiching_orders, name='filter_stiching_orders'),
    path('filter_stiching_orders_id',views.filter_stiching_orders_id, name='filter_stiching_orders_id'),
    
    
    path('printing_section',views.printing_section, name='printing_section'),
    path('filter_printing_orders',views.filter_printing_orders, name='filter_printing_orders'),
    path('filter_printing_orders_id',views.filter_printing_orders_id, name='filter_printing_orders_id'),
    
    path('testing_section',views.testing_section, name='testing_section'),
    path('filter_testing_orders',views.filter_testing_orders, name='filter_testing_orders'),
    path('filter_testing_orders_id',views.filter_testing_orders_id, name='filter_testing_orders_id'),

    path('packing_section',views.packing_section, name='packing_section'),
    path('filter_packing_orders',views.filter_packing_orders, name='filter_packing_orders'),
    path('filter_packing_orders_id',views.filter_packing_orders_id, name='filter_packing_orders_id'),

    path('despatch_section',views.despatch_section, name='despatch_section'),
    path('filter_despatch_orders',views.filter_despatch_orders, name='filter_despatch_orders'),
    path('filter_despatch_orders_id',views.filter_despatch_orders_id, name='filter_despatch_orders_id'),
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
     
    
    path('cutting_order_list',views.cutting_order_list, name='cutting_order_list'),
    path('cutting_filter_order_date',views.cutting_filter_order_date, name='cutting_filter_order_date'),
    path('cutting_filter_order_id',views.cutting_filter_order_id, name='cutting_filter_order_id'),
    path('cutting_complete_order',views.cutting_complete_order, name='cutting_complete_order'),
    path('cutting_filter_complete_order',views.cutting_filter_complete_order, name='cutting_filter_complete_order'),
    path('cutting_filter_complete_order_id',views.cutting_filter_complete_order_id, name='cutting_filter_complete_order_id'), 
    path('cutting_change_order_stage',views.cutting_change_order_stage, name='cutting_change_order_stage'),
    path('cutting_change_order_stage_client',views.cutting_change_order_stage_client, name='cutting_change_order_stage_client'),
    #? stiching
    path('stiching_order_list',views.stiching_order_list, name='stiching_order_list'),
    path('stiching_filter_order_date',views.stiching_filter_order_date, name='stiching_filter_order_date'),
    path('stiching_filter_order_id',views.stiching_filter_order_id, name='stiching_filter_order_id'),
    path('stiching_complete_order',views.stiching_complete_order, name='stiching_complete_order'),
    path('stiching_filter_complete_order',views.stiching_filter_complete_order, name='stiching_filter_complete_order'),
    path('stiching_filter_complete_order_id',views.stiching_filter_complete_order_id, name='stiching_filter_complete_order_id'),   

    path('stiching_change_order_stage',views.stiching_change_order_stage, name='stiching_change_order_stage'),

    path('stiching_change_order_stage_client',views.stiching_change_order_stage_client, name='stiching_change_order_stage_client'),

    #! Printing
    path('printing_order_list',views.printing_order_list, name='printing_order_list'),
    path('printing_filter_order_date',views.printing_filter_order_date, name='printing_filter_order_date'),
    path('printing_filter_order_id',views.printing_filter_order_id, name='printing_filter_order_id'),
    path('printing_complete_order',views.printing_complete_order, name='printing_complete_order'),
    path('printing_filter_complete_order',views.printing_filter_complete_order, name='printing_filter_complete_order'),
    path('printing_filter_complete_order_id',views.printing_filter_complete_order_id, name='printing_filter_complete_order_id'),
    path('printing_change_order_stage',views.printing_change_order_stage, name='printing_change_order_stage'),
    path('printing_change_order_stage_client',views.printing_change_order_stage_client, name='printing_change_order_stage_client'),

    #! testing
    path('testing_order_list',views.testing_order_list, name='testing_order_list'),
    path('testing_filter_order_date',views.testing_filter_order_date, name='testing_filter_order_date'),
    path('testing_filter_order_id',views.testing_filter_order_id, name='testing_filter_order_id'),
    path('testing_complete_order',views.testing_complete_order, name='testing_complete_order'),
    path('testing_filter_complete_order',views.testing_filter_complete_order, name='testing_filter_complete_order'),
    path('testing_filter_complete_order_id',views.testing_filter_complete_order_id, name='testing_filter_complete_order_id'),
    path('testing_change_order_stage',views.testing_change_order_stage, name='testing_change_order_stage'),
    path('testing_change_order_stage_client',views.testing_change_order_stage_client, name='testing_change_order_stage_client'),

    #! packing
    path('packing_order_list',views.packing_order_list, name='packing_order_list'),
    path('packing_filter_order_date',views.packing_filter_order_date, name='packing_filter_order_date'),
    path('packing_filter_order_id',views.packing_filter_order_id, name='packing_filter_order_id'),
    path('packing_complete_order',views.packing_complete_order, name='packing_complete_order'),
    path('packing_filter_complete_order',views.packing_filter_complete_order, name='packing_filter_complete_order'),
    path('packing_filter_complete_order_id',views.packing_filter_complete_order_id, name='packing_filter_complete_order_id'),
    path('packing_change_order_stage',views.packing_change_order_stage, name='packing_change_order_stage'),
    path('packing_change_order_stage_client',views.packing_change_order_stage_client, name='packing_change_order_stage_client'),

    #! despatch
    path('despatch_order_list',views.despatch_order_list, name='despatch_order_list'),
    path('despatch_filter_order_date',views.despatch_filter_order_date, name='despatch_filter_order_date'),
    path('despatch_filter_order_id',views.despatch_filter_order_id, name='despatch_filter_order_id'),
    path('despatch_complete_order',views.despatch_complete_order, name='despatch_complete_order'),
    path('despatch_filter_complete_order',views.despatch_filter_complete_order, name='despatch_filter_complete_order'),
    path('despatch_filter_complete_order_id',views.despatch_filter_complete_order_id, name='despatch_filter_complete_order_id'),
    path('despatch_change_order_stage',views.despatch_change_order_stage, name='despatch_change_order_stage'),
    path('despatch_change_order_stage_client',views.despatch_change_order_stage_client, name='despatch_change_order_stage_client'),

    ########################################################################USER MODULE
    
    
    ######################################################################################
    path('logout',views.logout, name='logout'),

]
