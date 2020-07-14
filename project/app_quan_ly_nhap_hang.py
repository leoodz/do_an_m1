from project import app
from flask import render_template, request, Markup, url_for, redirect , session
from datetime import datetime
from project.xu_ly.xuLy_quan_ly_nhap_hang import *


@app.route('/quan-ly-nhap-hang/dang-nhap',methods = ['GET','POST'])
def qlnh_dn():
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
            session['quan_ly_nhap_hang'] = nhanvien
            return redirect('/quan-ly-nhap-hang')

    return render_template("quan_ly_nhap_hang/dang_nhap.html",tendn = tendn,ketqua = ketqua)

@app.route('/quan-ly-nhap-hang',methods = ['GET','POST'])
def qlnh():
    if session.get('quan_ly_nhap_hang') == None:
        return redirect('/quan-ly-nhap-hang/dang-nhap')
    chuoi_tim =''
    danh_sach_Tivi = Doc_danh_sach_Tivi()
    if request.method == 'POST':
        result = request.form
        chuoi_tim = result.get('TH_gt_tim')
        danh_sach_Tivi = Tra_cuu_Tivi(chuoi_tim,danh_sach_Tivi)

    return render_template("quan_ly_nhap_hang/index.html",danh_sach_tivi = danh_sach_Tivi,chuoi_tim = chuoi_tim)

@app.route('/quan-ly-nhap-hang/cap-nhat/<string:Ma_so>/',methods = ['GET','POST'])
def qlnh_nh(Ma_so):
    if session.get('quan_ly_nhap_hang') == None:
        return redirect('/quan-ly-nhap-hang/dang-nhap')
    thong_bao = ''
    sl = 0
    tivi = Thong_tin_tivi(Ma_so)
    phieuban = ''
    dangxuat = ''
    if request.method == 'GET':
        result = request.form
        phieuban = request.values.get('TH_Phieu_Ban')
        dangxuat = request.values.get('TH_Dang_Xuat')
        if "phieuban" == phieuban:
            return redirect('/nhan-vien-ban-hang/thong-ke-phieu-ban')
        if 'dangxuat' == dangxuat:
            session.pop('quan_ly_nhap_hang')
            return redirect('/quan-ly-nhap-hang/dang-nhap')
    if tivi == None:
        thong_bao = Ma_so +' khong ton tai'
    elif request.method == 'POST':
        result = request.form
        sl = result.get('TH_GiaMoi')
        if int(sl) <= 0:
            thong_bao ='So luong ko hop le'
        else:
            tivi['Don_gia_Nhap'] = sl
        
            Danh_sach_slt = Dem_LT_toan_bo_nhom()

            session['Thong_tin_ton'] = Danh_sach_slt
            Ghi_Tivi(tivi)
            return redirect('/nhan-vien-ban-hang/thong-ke-so-luong-ton')
    return render_template("quan_ly_nhap_hang/ban_hang.html",tivi = tivi,thong_bao = thong_bao,sl = sl,phieuban=phieuban, dangxuat=dangxuat)

@app.route('/nhan-vien-ban-hang/thong-ke-so-luong-ton',methods = ['GET','POST'])
def qlnh_tkt():
    if session.get('quan_ly_nhap_hang') == None:
        return redirect('/nhan-vien-ban-hang/dang-nhap')
    Ngay = datetime.now()
    Nhom = session.get('Thong_tin_ton')
    
    return render_template("quan_ly_nhap_hang/phieu_slt.html",Nhom = Nhom)