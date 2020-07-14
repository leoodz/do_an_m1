from project import app
from flask import render_template, request, Markup, url_for, redirect , session
from datetime import datetime

from project.xu_ly.xuLy_quan_ly_cong_ty import *

@app.route('/quan-ly-cong-ty/dang-nhap',methods = ['GET','POST'])
def qlct_dn():
    tendn = ''
    ketqua =''
    if request.method == 'POST':
        result = request.form
        tendn = result.get('TH_tenDN')
        mat_khau = result.get('TH_matkhau')
        nhanvien = Thong_tin_nhan_vien(tendn,mat_khau)
        if nhanvien == None:
            ketqua = "Dang nhap khong thanh cong"
        else:
            session['quan_ly_cong_ty'] = nhanvien
            return redirect('/quan-ly-cong-ty')

    return render_template("quan_ly_cong_ty/dang_nhap.html",tendn = tendn,ketqua = ketqua)

@app.route('/quan-ly-cong-ty',methods = ['GET','POST'])
def qlct():
    if session.get('quan_ly_cong_ty') == None:
        return redirect('/quan-ly-cong-ty/dang-nhap')
    chuoi_tim =''
    danh_sach_Tivi = Doc_danh_sach_Tivi()
    if request.method == 'POST':
        result = request.form
        chuoi_tim = result.get('TH_gt_tim')
        danh_sach_Tivi = Tra_cuu_Tivi(chuoi_tim,danh_sach_Tivi)

    return render_template("quan_ly_cong_ty/index.html",danh_sach_tivi = danh_sach_Tivi,chuoi_tim = chuoi_tim)

@app.route('/quan-ly-cong-ty/thong-ke-so-luong-ton',methods = ['GET','POST'])
def qlct_slt():
    if session.get('quan_ly_cong_ty') == None:
        return redirect('/quan-ly-cong-ty/dang-nhap')
    Nhom = Dem_LT_toan_bo_nhom()
    return render_template("quan_ly_cong_ty/so_luong_ton.html",Nhom = Nhom)

@app.route('/quan-ly-cong-ty/thong-ke-phieu-ban',methods = ['GET','POST'])
def qlct_dsb():
    if session.get('quan_ly_cong_ty') == None:
        return redirect('/quan-ly-cong-ty/dang-nhap')
    Ngay = datetime.now()
    nvdn = session.get('nhan_vien_ban_hang')
    danh_sach_tivi_nhap , tong_tien = Thong_Ke_Ban_Hang()
    
    return render_template("quan_ly_cong_ty/danh_sach_ban.html",danh_sach_tivi_nhap=danh_sach_tivi_nhap,tong_tien=tong_tien)