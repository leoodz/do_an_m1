from flask import Flask

app = Flask(__name__)
app.secret_key = 'do_an_m1_2020'

import project.app_khach_tham_quan
import project.app_nhan_vien_ban_hang
import project.app_nhan_vien_nhap_hang
import project.app_quan_ly_ban_hang
import project.app_quan_ly_cong_ty
import project.app_quan_ly_nhap_hang
