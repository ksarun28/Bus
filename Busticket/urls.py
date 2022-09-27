from django.urls import path
from  . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("userreg", views.userreg, name="userreg"),


    path("adminhome", views.adminhome, name="adminhome"),
    path("add_dist", views.add_dist, name="add_dist"),
    path("deletedist", views.deletedist, name="deletedist"),
    path("addlocation", views.addlocation, name="addlocation"),
    path("deletelocation", views.deletelocation, name="deletelocation"),
    path("addroute", views.addroute, name="addroute"),
    path("seatschedule", views.seatschedule, name="seatschedule"),
    path("ticketmanage", views.ticketmanage, name="ticketmanage"),

    path("addbus", views.addbus, name="addbus"),
    path("deletebus",views.deletebus, name="deletebus"),
    path("bus_schedule", views.bus_schedule, name="bus_schedule"),

    path("staffreg", views.staffreg, name="staffreg"),
    path("liststaff", views.liststaff, name="liststaff"),
    path("approve_user", views.approve_user, name="approve_user"),
    path("listuser", views.listuser, name="listuser"),
    path("allotstaff", views.allotstaff, name="allotstaff"),

    path('privacy',views.privacy,name='privacy'),


    path("userhome", views.userhome, name="userhome"),
    path('user_data',views.user_data,name='user_data'),
    path('user_update/<int:id>',views.user_update,name='user_update'),
    path('booked_history',views.booked_history,name='booked_history'),

    path("bus_search", views.bus_search, name="bus_search"),
    path("book_now", views.book_now, name="book_now"),
    path("booked", views.booked, name="booked"),
    path("pay", views.pay, name="pay"),
    path("paycomplete", views.paycomplete, name="paycomplete"),


    path("staffhome", views.staffhome, name="staffhome"),
    path("listlocation", views.listlocation, name="listlocation"),
    path("listroute", views.listroute, name="listroute"),
    path("listbus", views.listbus, name="listbus"),
    path("viewbus_schedule", views.viewbus_schedule, name="viewbus_schedule"),
    path("viewseat_schedule", views.viewseat_schedule, name="viewseat_schedule"),
    path("viewstaff_schedule", views.viewstaff_schedule, name="viewstaff_schedule"), 
    path("log_out", views.log_out, name="log_out"),


    # path(" ", views.view, name=" "),
    # path(" ", views.view, name=" "),
    # path(" ", views.view, name=" "),
]
