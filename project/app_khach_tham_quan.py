from project import app
from flask import Flask, render_template, request, Markup, url_for, request
from project.xu_ly.xuLy_khach_tham_quan import *

@app.route('/',methods = ['GET','POST'])
def index():
    chuoi_tim =''
    danh_sach_Tivi = Doc_danh_sach_Tivi()
    if request.method == 'POST':
        result = request.form
        chuoi_tim = result.get('TH_gt_tim')
        danh_sach_Tivi = Tra_cuu_Tivi(chuoi_tim,danh_sach_Tivi)

    return render_template("khach_tham_quan/index.html",danh_sach_tivi = danh_sach_Tivi,chuoi_tim = chuoi_tim)
